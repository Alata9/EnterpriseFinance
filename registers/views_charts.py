import decimal
from datetime import datetime

from django.db.models import Sum, F, Value, ExpressionWrapper, Q, Subquery, OuterRef, FloatField
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import UpdateView, ListView, View
from directory.models import PaymentAccount, CurrenciesRates, Counterparties, InitialDebts
from payments.models import PaymentDocuments

from registers.forms import AccountSettingsSet, AccountBalancesFilter, DashboardFilter
from registers.models import AccountSettings
from registers.views_reports import AccountBalancesView


def htmx_projects(request):
    form = DashboardFilter(request.GET)
    return HttpResponse(form["project"])


class DashboardView(View):
    def get(self, request):
        main_currency = AccountSettings.load().currency()
        form = DashboardFilter(request.GET)
        accounts = PaymentAccount.objects.all()

        paydocs = PaymentDocuments.objects.all().annotate(
            amount=F('inflow_amount') + F('outflow_amount'),
            amount_convert=((F('inflow_amount') + F('outflow_amount')) /
                            CurrenciesRates.objects.filter(
                                accounting_currency=main_currency,
                                currency=F('currency__id'), date__lte=datetime.now())
                            .order_by('-date')[:1].first().rate
                            )
        )

        # for i in paydocs:
        #     print(i.date, i.amount, i.currency, i.amount_convert)

        paydocs_before = paydocs

        if form.is_valid():
            if form.cleaned_data['organization']:
                accounts = accounts.filter(organization=form.cleaned_data['organization'])
                paydocs = paydocs.filter(organization=form.cleaned_data['organization'])
                paydocs_before = paydocs_before.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['date_start']:
                paydocs = paydocs.filter(date__gte=form.cleaned_data['date_start'])
            if form.cleaned_data['date_end']:
                paydocs = paydocs.filter(date__lte=form.cleaned_data['date_end'])
                paydocs_before = paydocs_before.filter(date__lte=form.cleaned_data['date_start'])

        cf_table, cf_bar = self.get_cf_table(paydocs)

        context = {
            'form': form,
            'today': datetime.today(),
            'main_currency': main_currency,
            'account_balances': self.get_balances(accounts, paydocs_before),
            'cf_table': cf_table,
            'cf_bar': cf_bar,
            'cf_dynamics': self.get_cf_dynamics(paydocs),
        }

        return render(request, 'registers/dashboard.html', context=context)

    # chart 1: account balances
    @staticmethod
    def get_balances(accounts, paydocs_before):
        account_balances = {}
        accounts = accounts.values_list('account', flat=True).distinct()

        for acc in accounts:
            currency = PaymentAccount.objects.filter(account=acc).values_list('currency__code', flat=True)[0]

            receipts = paydocs_before.filter(account__account=acc)
            receipts_sum = receipts.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
            if receipts_sum is None:
                receipts_sum = 0

            payments = paydocs_before.filter(account__account=acc)
            payments_sum = payments.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
            if payments_sum is None:
                payments_sum = 0

            final_balance = receipts_sum - payments_sum
            account_balances[acc] = [int(final_balance), currency]

        account_balances = [[k, *v] for k, v in account_balances.items()]

        return account_balances

    @staticmethod
    def get_amount_sum(paydocs):
        amount_sum = paydocs.aggregate(Sum("amount_convert")).get('amount_convert__sum', 0.00)
        if amount_sum is None:
            amount_sum = 0
        return amount_sum

    # chart 2, 3 cf table and cf bar
    def get_cf_table(self, paydocs):
        cf_table = {}

        receipts_total = paydocs.filter(flow='Receipts')
        payments_total = paydocs.filter(flow='Payments')
        receipts_oper = paydocs.filter(item__activity='operating', flow='Receipts')
        payments_oper = paydocs.filter(item__activity='operating', flow='Payments')
        receipts_invest = paydocs.filter(item__activity='investing', flow='Receipts')
        payments_invest = paydocs.filter(item__activity='investing', flow='Payments')
        receipts_fin = paydocs.filter(item__activity='financing', flow='Receipts')
        payments_fin = paydocs.filter(item__activity='financing', flow='Payments')

        receipts_sum = self.get_amount_sum(receipts_total)
        payments_sum = self.get_amount_sum(payments_total)
        receipts_oper_sum = self.get_amount_sum(receipts_oper)
        payments_oper_sum = self.get_amount_sum(payments_oper)
        receipts_invest_sum = self.get_amount_sum(receipts_invest)
        payments_invest_sum = self.get_amount_sum(payments_invest)
        receipts_fin_sum = self.get_amount_sum(receipts_fin)
        payments_fin_sum = self.get_amount_sum(payments_fin)

        cf = receipts_sum - payments_sum
        cf_oper = receipts_oper_sum - payments_oper_sum
        cf_invest = receipts_invest_sum - payments_invest_sum
        cf_fin = receipts_fin_sum - payments_fin_sum

        cf_table['receipts'] = [int(receipts_oper_sum), int(receipts_invest_sum), int(receipts_fin_sum),
                                int(receipts_sum)]
        cf_table['payments'] = [int(payments_oper_sum), int(payments_invest_sum), int(payments_fin_sum),
                                int(payments_sum)]
        cf_table['cash flow'] = [int(cf_oper), int(cf_invest), int(cf_fin), int(cf)]

        cf_table = [[k, *v] for k, v in cf_table.items()]

        cf_total = cf_table[2][1] + cf_table[2][2] + cf_table[2][3]

        cf_bar = [['Operating', cf_table[2][1]], ['Investment', cf_table[2][2]],
                  ['Financing', cf_table[2][3]], ['Total', cf_total]]

        return cf_table, cf_bar

    # function for getting full data
    @staticmethod
    def get_dynamics(paydocs):
        dynamics = {}
        for paydoc in paydocs:
            month = str(paydoc.date.month).rjust(2, '0')
            period = f'{str(paydoc.date.year)}/{month}'
            amount = float(paydoc.amount_convert)
            if period not in dynamics:
                dynamics[period] = amount
            else:
                dynamics[period] += amount

        return dynamics

    # get dynamics of receipts and payments
    def get_cf_dynamics(self, paydocs):
        payments = paydocs.filter(flow='Payments')
        receipts = paydocs.filter(flow='Receipts')
        receipts_dynamics = self.get_dynamics(receipts)
        for k, v in receipts_dynamics.items():
            receipts_dynamics[k] = int(v)
        payments_dynamics = self.get_dynamics(payments)
        for k, v in payments_dynamics.items():
            payments_dynamics[k] = int(v * (-1))

        total_cf = {k: [receipts_dynamics.get(k, 0), payments_dynamics.get(k, 0)]
                    for k in set(receipts_dynamics) | set(payments_dynamics)}
        total_cf = sorted(total_cf.items(), key=lambda x: x[0])
        total_cf = dict(total_cf)

        cf_dynamics = []
        for k, v in total_cf.items():
            cf_dynamics.append([k, *v, v[0] + v[1]])

        return cf_dynamics


class ChartsOperView(View):
    def get(self, request):
        main_currency = AccountSettings.load().currency()
        form = DashboardFilter(request.GET)
        receipts = PaymentDocuments.objects.filter(flow='Receipts', item__activity='operating')
        payments = PaymentDocuments.objects.filter(flow='Payments', item__activity='operating')

        if form.is_valid():
            if form.cleaned_data['organization']:
                receipts = receipts.filter(organization=form.cleaned_data['organization'])
                payments = payments.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['project']:
                receipts = receipts.filter(project=form.cleaned_data['project'])
                payments = payments.filter(project=form.cleaned_data['project'])
            if form.cleaned_data['date_start']:
                receipts = receipts.filter(date__gte=form.cleaned_data['date_start'])
                payments = payments.filter(date__gte=form.cleaned_data['date_start'])
            if form.cleaned_data['date_end']:
                receipts = receipts.filter(date__lte=form.cleaned_data['date_end'])
                payments = payments.filter(date__lte=form.cleaned_data['date_end'])

        rp_dynamics = self.get_rp_dynamics(receipts, payments)

        context = {
            'form': form,
            'today': datetime.today(),
            'main_currency': main_currency,
            'payments_bar': self.get_bar_payments(payments),
            'receipts_structure': self.get_structure(receipts),
            'payments_structure': self.get_structure(payments),
            'rp_dynamics': rp_dynamics,
            'top_customers': self.get_bar_top10(receipts, 'Receipts'),
            'top_suppliers': self.get_bar_top10(payments, 'Payments'),
        }

        return render(request, 'registers/charts_oper.html', context=context)

    # charts 1, 2, 4
    def get_structure(self, doc):
        main_currency = AccountSettings.load().currency()
        data = {}
        for i in doc:
            rate = float(AccountBalancesView.get_rate(i.currency, main_currency))
            item = str(i.item)
            amount = float(i.inflow_amount) / rate if i.inflow_amount != 0 else float(i.outflow_amount) / rate

            if item not in data:
                data[item] = int(amount)
            else:
                data[item] += int(amount)

        data_sort = sorted(data.items(), key=lambda x: x[1], reverse=True)
        data_sort = dict(data_sort)
        structure = [[k, v] for k, v in data_sort.items()]

        return structure

    # function for data payments and payments
    @staticmethod
    def get_dynamics(doc):
        main_currency = AccountSettings.load().currency()
        dynamics = {}
        for i in doc:
            rate = float(AccountBalancesView.get_rate(i.currency, main_currency))
            month = str(i.date.month).rjust(2, '0')
            period = f'{str(i.date.year)}/{month}'
            amount = float(i.inflow_amount) / rate if i.inflow_amount != 0 else float(i.outflow_amount) / rate
            if period not in dynamics:
                dynamics[period] = int(amount)
            else:
                dynamics[period] += int(amount)

        return dynamics

    # get data payments and payments for chart 3
    def get_total_cf(self, receipts, payments):
        payments_dynamics = self.get_dynamics(payments)
        receipts_dynamics = self.get_dynamics(receipts)

        total_cf = {k: [receipts_dynamics.get(k, 0), payments_dynamics.get(k, 0)]
                    for k in set(receipts_dynamics) | set(payments_dynamics)}
        total_cf = sorted(total_cf.items(), key=lambda x: x[0])
        total_cf = dict(total_cf)

        return total_cf

    # chart 3 Dynamics of payments and payments
    def get_rp_dynamics(self, receipts, payments):
        total_cf = self.get_total_cf(receipts, payments)
        rp_dynamics = []
        for k, v in total_cf.items():
            rp_dynamics.append([k, *v])

        return rp_dynamics

    # chart 5 Payments bar by group
    @staticmethod
    def get_bar_payments(paydocs):
        main_currency = AccountSettings.load().currency()
        data = {}
        for i in paydocs:
            rate = float(AccountBalancesView.get_rate(i.currency, main_currency))
            items_group = str(i.item.group)
            amount = float(i.inflow_amount) / rate if i.inflow_amount != 0 else float(i.outflow_amount) / rate
            if items_group not in data:
                data[items_group] = amount
            else:
                data[items_group] += amount
        data_sort = sorted(data.items(), key=lambda x: x[1], reverse=True)
        structure = dict(data_sort)

        return [[k, v] for k, v in structure.items()]

    # chart 6, 7 TOP-10 counterparty
    @staticmethod
    def get_bar_top10(paydocs, flow):
        main_currency = AccountSettings.load().currency()
        if flow == 'Receipts':
            counterparties = Counterparties.objects.filter(customer=True).values_list('id', flat=True)
        else:
            counterparties = Counterparties.objects.filter(suppliers=True).values_list('id', flat=True)
        data = {}
        paydocs_sum = (
            paydocs
            .filter(counterparty__in=counterparties)
            .annotate(amount_sum=Sum("inflow_amount") + Sum("outflow_amount"))
            .order_by('counterparty', 'currency', 'amount_sum')
            .values('counterparty__counterparty', 'currency', 'amount_sum')
        )
        counterparty = None
        for doc_sum in paydocs_sum:
            cp = doc_sum['counterparty__counterparty']
            if counterparty != cp:
                counterparty = cp
                data[cp] = 0.0
            rate = AccountBalancesView.get_rate(doc_sum['currency'], main_currency)
            data[cp] += int(float(doc_sum['amount_sum']) / (float(rate) or 1.0))

        data_sort = sorted(data.items(), key=lambda x: x[1], reverse=True)
        top10 = dict(data_sort)

        return [[k, v] for k, v in top10.items()][:10]


class ChartsFinView(View):
    main_currency = AccountSettings.load().currency()

    def get(self, request):
        form = DashboardFilter(request.GET)
        agents = Counterparties.objects.all()
        initial_debts = InitialDebts.objects.all()
        paydocs = PaymentDocuments.objects.filter(item__activity='financing') \
            .annotate(amount=F('inflow_amount') + F('outflow_amount'),
                      rate=Value(AccountBalancesView.get_rate(F('currecy__id'), self.main_currency)),
                      amount_convert=(F('amount') / F('rate')))

        # for i in paydocs:
        #     print(i.date, i.currency, i.rate, i.amount_convert)

        paydocs_before = paydocs

        if form.is_valid():
            if form.cleaned_data['organization']:
                paydocs = paydocs.filter(organization=form.cleaned_data['organization'])
                paydocs_before = paydocs_before.filter(organization=form.cleaned_data['organization'])
                initial_debts = initial_debts.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['date_start']:
                paydocs = paydocs.filter(date__gte=form.cleaned_data['date_start'])
                paydocs_before = paydocs_before.filter(date__gte=form.cleaned_data['date_start'])
            else:
                paydocs_before = PaymentDocuments.objects.none()
            if form.cleaned_data['date_end']:
                paydocs = paydocs.filter(date__lte=form.cleaned_data['date_end'])
                paydocs_before = paydocs_before.filter(date__lte=form.cleaned_data['date_end'])

        # credit_portfolio = self.get_loan_portfolio(agents, paydocs, initial_debts)
        # debit_portfolio = self.get_loan_portfolio(agents, paydocs, initial_debts)
        loans_table = self.get_loan_tables(agents, paydocs, paydocs_before, initial_debts)

        context = {
            'form': form,
            'today': datetime.today(),
            'loans_table': loans_table,
            # 'credit_portfolio': credit_portfolio,
            # 'debit_portfolio': debit_portfolio,
            # 'cf_fin_dynamics': self.get_cf_dynamics(paydocs),
        }

        return render(request, 'registers/charts_fin.html', context=context)

    # chart loans_table
    def get_loan_tables(self, agents, paydocs, paydocs_before, initial_debts):
        loans_table = []
        print(initial_debts)
        for agent in agents:
            initial_debt = initial_debts.filter(counterparty=agent)
            print(initial_debt)
            debit = initial_debt.aggregate(Sum("debit")).get('debit__sum', 0.00)
            if debit is None:
                debit = 0.0
            credit = initial_debt.aggregate(Sum("credit")).get('credit__sum', 0.00)
            if credit is None:
                credit = 0.0
            initial_debt = debit - credit

            # print(f'initial - {agent.counterparty}: {initial_debt}')

            receipts = paydocs.filter(counterparty=agent, flow='Receipts')
            receipts_sum = receipts.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
            if receipts_sum is None:
                receipts_sum = 0

            receipts_before = paydocs_before.filter(counterparty=agent, flow='Receipts')
            receipts_before_sum = receipts_before.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
            if receipts_before_sum is None:
                receipts_before_sum = 0

            payments = paydocs.filter(counterparty=agent, flow='Payments')
            payments_sum = payments.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
            if payments_sum is None:
                payments_sum = 0

            payments_before = paydocs_before.filter(counterparty=agent, flow='Payments')
            payments_before_sum = payments_before.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
            if payments_before_sum is None:
                payments_before_sum = 0

            start_balance = int(initial_debt) + int(receipts_before_sum) - int(payments_before_sum)
            start_debit = abs(start_balance) if start_balance > 0 else 0
            start_credit = abs(start_balance) if start_balance < 0 else 0

            final_balance = int(initial_debt) - int(payments_sum) + int(receipts_sum)
            final_debit = abs(final_balance) if final_balance > 0 else 0
            final_credit = abs(final_balance) if final_balance < 0 else 0
            agent = str(agent.counterparty)
            currency = 'RUB'

            loans_table.append([agent, int(start_debit), int(start_credit), int(receipts_sum),
                                int(payments_sum), int(final_debit), int(final_credit), currency])

        print(f'table - {loans_table}')
        return loans_table

    # charts portfolios
    def get_loan_portfolio(self, agents, paydocs, initial_debts):
        portfolio = []
        for agent in agents:
            initial_debts = initial_debts.filter(counterparty=agent)
            print(f' the {initial_debts}')
            if initial_debts is None:
                initial_debts.credit = 0
                initial_debts.debit = 0
            # if initial_debts.debit is None:

            receipts = paydocs.filter(counterparty=agent)
            receipts_sum = receipts.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
            if receipts_sum is None:
                receipts_sum = 0
            payments = paydocs.filter(counterparty=agent)
            payments_sum = payments.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
            if payments_sum is None:
                payments_sum = 0

            open_balance = 0  # agent.credit - agent.debit
            final_balance = abs(open_balance + receipts_sum - payments_sum)
            agent = str(agent)

            portfolio.append([agent, int(final_balance)])

        return portfolio

    # function for getting full data
    @staticmethod
    def get_dynamics(paydocs):
        dynamics = {}
        for paydoc in paydocs:
            month = str(paydoc.date.month).rjust(2, '0')
            period = f'{str(paydoc.date.year)}/{month}'
            amount = float(paydoc.inflow_amount) if paydoc.inflow_amount != 0 else float(paydoc.outflow_amount)
            if period not in dynamics:
                dynamics[period] = amount
            else:
                dynamics[period] += amount

        return dynamics

    # get data payments and payments
    def get_total_cf(self, paydocs):
        payments_dynamics = self.get_dynamics(paydocs)
        receipts_dynamics = self.get_dynamics(paydocs)

        total_cf = {k: [receipts_dynamics.get(k, 0), payments_dynamics.get(k, 0)]
                    for k in set(receipts_dynamics) | set(payments_dynamics)}
        total_cf = sorted(total_cf.items(), key=lambda x: x[0])
        total_cf = dict(total_cf)

        return total_cf

    # chart 4 total cash flow
    def get_cf_dynamics(self, paydocs):
        total_cf = self.get_total_cf(paydocs)
        cf_dynamics = []
        for k, v in total_cf.items():
            cf_dynamics.append([k, *v, v[0] - v[1]])

        return cf_dynamics


def ChartsInvestView(request):
    pass


class ChartsFinView1(View):
    def get(self, request):
        form = DashboardFilter(request.GET)

        lenders = InitialDebts.objects.filter(type_debt='Lender')
        borrowers = InitialDebts.objects.filter(type_debt='Borrower')

        receipts = PaymentDocuments.objects.filter(flow='Receipts', item__activity='financing')
        payments = PaymentDocuments.objects.filter(flow='Payments', item__activity='financing')
        receipts_before = receipts
        payments_before = payments

        if form.is_valid():
            if form.cleaned_data['organization']:
                receipts = receipts.filter(organization=form.cleaned_data['organization'])
                payments = payments.filter(organization=form.cleaned_data['organization'])
                lenders = lenders.filter(organization=form.cleaned_data['organization'])
                borrowers = borrowers.filter(organization=form.cleaned_data['organization'])

            if form.cleaned_data['date_start']:
                receipts = receipts.filter(date__gte=form.cleaned_data['date_start'])
                payments = payments.filter(date__gte=form.cleaned_data['date_start'])
                receipts_before = receipts_before.filter(date__lte=form.cleaned_data['date_start'])
                payments_before = payments_before.filter(date__lte=form.cleaned_data['date_start'])
            else:
                receipts_before = PaymentDocuments.objects.none()
                payments_before = PaymentDocuments.objects.none()
            if form.cleaned_data['date_end']:
                receipts = receipts.filter(date__lte=form.cleaned_data['date_end'])
                payments = payments.filter(date__lte=form.cleaned_data['date_end'])

        loan_portfolio = self.get_loan_portfolio(lenders, receipts, payments)
        debit_portfolio = self.get_loan_portfolio(borrowers, receipts, payments)
        lenders_table = self.get_tables(lenders, receipts, payments, receipts_before, payments_before)
        borrowers_table = self.get_tables(borrowers, receipts, payments, receipts_before, payments_before)

        context = {
            'form': form,
            'today': datetime.today(),
            'loan_portfolio': loan_portfolio,
            'debit_portfolio': debit_portfolio,
            'cf_fin_dynamics': self.get_cf_dynamics(receipts, payments),
            'lenders_table': lenders_table,
            'borrowers_table': borrowers_table,
        }

        return render(request, 'registers/charts_fin.html', context=context)

        # charts 1, 2 portfolios

    def get_loan_portfolio(self, agents, receipts, payments):
        portfolio = []
        for agent in agents:
            if agent.credit is None:
                agent.credit = 0
            if agent.debit is None:
                agent.debit = 0
            receipts = receipts.filter(counterparty=agent.counterparty)
            receipts_sum = receipts.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
            if receipts_sum is None:
                receipts_sum = 0
            payments = payments.filter(counterparty=agent.counterparty)
            payments_sum = payments.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
            if payments_sum is None:
                payments_sum = 0

            open_balance = agent.credit - agent.debit
            final_balance = abs(open_balance + receipts_sum - payments_sum)
            agent = str(agent.counterparty)

            portfolio.append([agent, int(final_balance)])
        print(agents)
        print(portfolio)
        return portfolio

    # chart 4, 5: agents_table
    def get_tables(self, agents, receipts, payments, receipts_before, payments_before):
        agents_table = []

        for agent in agents:
            receipts = receipts.filter(counterparty=agent.counterparty)
            receipts_sum = receipts.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
            if receipts_sum == None: receipts_sum = 0

            receipts_before = receipts_before.filter(counterparty=agent.counterparty)
            receipts_before_sum = receipts_before.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
            if receipts_before_sum == None: receipts_before_sum = 0

            payments = payments.filter(counterparty=agent.counterparty)
            payments_sum = payments.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
            if payments_sum == None: payments_sum = 0

            payments_before = payments_before.filter(counterparty=agent.counterparty)
            payments_before_sum = payments_before.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
            if payments_before_sum == None: payments_before_sum = 0

            start_balance = agent.debit - agent.credit + receipts_before_sum - payments_before_sum
            start_debit = abs(start_balance) if start_balance > 0 else 0
            start_credit = abs(start_balance) if start_balance < 0 else 0

            final_balance = agent.debit - agent.credit - receipts_sum + payments_sum
            final_debit = abs(final_balance) if final_balance > 0 else 0
            final_credit = abs(final_balance) if final_balance < 0 else 0
            agent = str(agent.counterparty)

            agents_table.append([agent, int(start_debit), int(start_credit), int(receipts_sum),
                                 int(payments_sum), int(final_debit), int(final_credit)])

        print(agents_table)
        return agents_table

    # function for getting full data
    @staticmethod
    def get_dynamics(flow):
        dynamics = {}
        for i in flow:
            month = str(i.date.month).rjust(2, '0')
            period = f'{str(i.date.year)}/{month}'
            amount = float(i.inflow_amount) if i.inflow_amount != 0 else float(i.outflow_amount)
            if period not in dynamics:
                dynamics[period] = amount
            else:
                dynamics[period] += amount

        return dynamics

    # get data payments and payments
    def get_total_cf(self, payments, receipts):
        payments_dynamics = self.get_dynamics(payments)
        receipts_dynamics = self.get_dynamics(receipts)

        total_cf = {k: [receipts_dynamics.get(k, 0), payments_dynamics.get(k, 0)]
                    for k in set(receipts_dynamics) | set(payments_dynamics)}
        total_cf = sorted(total_cf.items(), key=lambda x: x[0])
        total_cf = dict(total_cf)

        return total_cf

    # chart 4 total cash flow
    def get_cf_dynamics(self, payments, receipts):
        total_cf = self.get_total_cf(payments, receipts)
        cf_dynamics = []
        for k, v in total_cf.items():
            cf_dynamics.append([k, *v, v[0] - v[1]])

        return cf_dynamics
