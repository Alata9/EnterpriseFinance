import decimal
from datetime import datetime

from django.db.models import Sum
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
        form = DashboardFilter(request.GET)

        accounts = PaymentAccount.objects.all()
        receipts = PaymentDocuments.objects.filter(flow='Receipts')
        receipts_oper = PaymentDocuments.objects.filter(item__activity='operating')
        receipts_invest = PaymentDocuments.objects.filter(item__activity='investing')
        receipts_fin = PaymentDocuments.objects.filter(item__activity='financing')

        payments = PaymentDocuments.objects.filter(flow='Payments')
        payments_oper = PaymentDocuments.objects.filter(item__activity='operating')
        payments_invest = PaymentDocuments.objects.filter(item__activity='investing')
        payments_fin = PaymentDocuments.objects.filter(item__activity='financing')

        if form.is_valid():
            if form.cleaned_data['organization']:
                accounts = accounts.filter(organization=form.cleaned_data['organization'])
                receipts = receipts.filter(organization=form.cleaned_data['organization'])
                receipts_oper = receipts_oper.filter(organization=form.cleaned_data['organization'])
                receipts_invest = receipts_invest.filter(organization=form.cleaned_data['organization'])
                receipts_fin = receipts_fin.filter(organization=form.cleaned_data['organization'])
                payments = payments.filter(organization=form.cleaned_data['organization'])
                payments_oper = payments_oper.filter(organization=form.cleaned_data['organization'])
                payments_invest = payments_invest.filter(organization=form.cleaned_data['organization'])
                payments_fin = payments_fin.filter(organization=form.cleaned_data['organization'])

            if form.cleaned_data['date_start']:
                receipts = receipts.filter(date__gte=form.cleaned_data['date_start'])
                receipts_oper = receipts_oper.filter(date__gte=form.cleaned_data['date_start'])
                receipts_invest = receipts_invest.filter(date__gte=form.cleaned_data['date_start'])
                receipts_fin = receipts_fin.filter(date__gte=form.cleaned_data['date_start'])
                payments = payments.filter(date__gte=form.cleaned_data['date_start'])
                payments_oper = payments_oper.filter(date__gte=form.cleaned_data['date_start'])
                payments_invest = payments_invest.filter(date__gte=form.cleaned_data['date_start'])
                payments_fin = payments_fin.filter(date__gte=form.cleaned_data['date_start'])

            if form.cleaned_data['date_end']:
                receipts = receipts.filter(date__lte=form.cleaned_data['date_end'])
                receipts_oper = receipts_oper.filter(date__lte=form.cleaned_data['date_end'])
                receipts_invest = receipts_invest.filter(date__lte=form.cleaned_data['date_end'])
                receipts_fin = receipts_fin.filter(date__lte=form.cleaned_data['date_end'])
                payments = payments.filter(date__lte=form.cleaned_data['date_end'])
                payments_oper = payments_oper.filter(date__lte=form.cleaned_data['date_end'])
                payments_invest = payments_invest.filter(date__lte=form.cleaned_data['date_end'])
                payments_fin = payments_fin.filter(date__lte=form.cleaned_data['date_end'])

        cf_table, cf_bar = self.get_cf_table(
            receipts, payments, receipts_oper, payments_oper,
            receipts_invest, payments_invest, receipts_fin, payments_fin)

        account_balances = self.get_balances(accounts, receipts, payments)

        context = {
            'form': form,
            'today': datetime.today(),
            'account_balances': account_balances,
            'cf_table': cf_table,
            'cf_bar': cf_bar,
            'cf_dynamics': self.get_cf_dynamics(payments, receipts),
        }

        return render(request, 'registers/dashboard.html', context=context)

    # chart 1: account balances
    @staticmethod
    def get_balances(accounts, receipts, payments):
        account_balances = {}
        accounts = accounts.values_list('account', flat=True).distinct()

        for i in accounts:
            currency = PaymentAccount.objects.filter(account=i).values_list('currency__code', flat=True)[0]

            receipts = PaymentDocuments.objects.filter(account__account=i)
            receipts_sum = receipts.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
            if receipts_sum is None:
                receipts_sum = 0

            payments = PaymentDocuments.objects.filter(account__account=i)
            payments_sum = payments.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
            if payments_sum is None:
                payments_sum = 0

            final_balance = receipts_sum - payments_sum
            account_balances[i] = [int(final_balance), currency]

        account_balances = [[k, *v] for k, v in account_balances.items()]

        return account_balances

    # chart 2, 3 cf table and cf bar
    @staticmethod
    def get_cf_table(
            receipts, payments, receipts_oper, payments_oper,
            receipts_invest, payments_invest, receipts_fin, payments_fin):

        cf_table = {}
        receipts_sum = receipts.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
        if receipts_sum is None:
            receipts_sum = 0
        payments_sum = payments.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
        if payments_sum is None:
            payments_sum = 0
        receipts_oper = receipts_oper.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
        if receipts_oper is None:
            receipts_oper = 0
        payments_oper = payments_oper.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
        if payments_oper is None:
            payments_oper = 0
        receipts_invest = receipts_invest.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
        if receipts_invest is None:
            receipts_invest = 0
        payments_invest = payments_invest.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
        if payments_invest is None:
            payments_invest = 0
        receipts_fin = receipts_fin.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
        if receipts_fin is None:
            receipts_fin = 0
        payments_fin = payments_fin.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
        if payments_fin is None:
            payments_fin = 0

        cf = receipts_sum - payments_sum
        cf_oper = receipts_oper - payments_oper
        cf_invest = receipts_invest - payments_invest
        cf_fin = receipts_fin - payments_fin

        cf_table['payments'] = [int(receipts_oper), int(receipts_invest), int(receipts_fin), int(receipts_sum)]
        cf_table['payments'] = [int(payments_oper), int(payments_invest), int(payments_fin), int(payments_sum)]
        cf_table['cash flow'] = [int(cf_oper), int(cf_invest), int(cf_fin), int(cf)]

        cf_table = [[k, *v] for k, v in cf_table.items()]
        cf_bar = [['Operating', cf_table[2][1]], ['Investment', cf_table[2][2]], ['Financing', cf_table[2][3]]]

        return cf_table, cf_bar

    # function for getting full data
    @staticmethod
    def get_dynamics(flow):
        dynamics = {}
        for i in flow:
            month = str(i.date.month).rjust(2, '0')
            period = f'{str(i.date.year)}/{month}'
            amount = float(i.amount)
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


class ChartsOperView(View):
    main_currency = AccountSettings.load().currency()

    def get(self, request):
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
            'payments_bar': self.get_bar_payments(payments),
            'receipts_structure': self.get_structure(receipts),
            'payments_structure': self.get_structure(payments),
            'rp_dynamics': rp_dynamics,
            'top_customers': self.get_bar_top10customers(receipts),
            'top_suppliers': self.get_bar_top10suppliers(payments),
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
                data[item] = amount
            else:
                data[item] += amount

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
                dynamics[period] = amount
            else:
                dynamics[period] += amount

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
    def get_bar_payments(doc):
        main_currency = AccountSettings.load().currency()
        data = {}
        for i in doc:
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

    # chart 6 TOP-10 customers
    @staticmethod
    def get_bar_top10customers(doc):
        main_currency = AccountSettings.load().currency()
        customers = Counterparties.objects.filter(customer=True)
        data = {}
        for customer in customers:
            doc_counter = doc.filter(counterparty=customer)
            # for doc in doc_counter:
            # rate = 1
            # rate = AccountBalancesView.get_rate(doc.currency, main_currency)
            amount_sum = doc_counter.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
            if amount_sum is None:
                amount_sum = 0
            if amount_sum != 0:
                data[str(customer)] = float(amount_sum)

        data_sort = sorted(data.items(), key=lambda x: x[1], reverse=True)
        top10 = dict(data_sort)

        return [[k, v] for k, v in top10.items()][:10]

    # chart 7 TOP-10 suppliers
    @staticmethod
    def get_bar_top10suppliers(doc):
        main_currency = AccountSettings.load().currency()
        suppliers = Counterparties.objects.filter(suppliers=True)
        doc_suppliers = doc.filter(counterparty=suppliers)
        data = {}
        for doc in doc_suppliers:
            rate = float(AccountBalancesView.get_rate(doc.currency, main_currency))
            supplier = str(doc.counterparty)
            amount = float(doc.inflow_amount) / rate if doc.inflow_amount != 0 else float(doc.outflow_amount) / rate
            if supplier not in data:
                data[supplier] = amount
            else:
                data[supplier] += amount

        data_sort = sorted(data.items(), key=lambda x: x[1], reverse=True)
        top10 = dict(data_sort)

        return [[k, v] for k, v in top10.items()][:10]


    @staticmethod
    def get_rate(cur, main_currency):
        if cur == main_currency:
            return decimal.Decimal(1)
        try:
            rate = CurrenciesRates.objects.filter(accounting_currency=main_currency, currency=cur,
                                                  date__lte=datetime.datetime.now()).order_by('-date')[:1].first().rate
        except:
            rate = decimal.Decimal(1)

        return rate


class ChartsFinView(View):
    def get(self, request):
        form = DashboardFilter(request.GET)

        lenders = InitialDebts.objects.filter(type_debt='Lender')
        borrowers = InitialDebts.objects.filter(type_debt='Borrower')

        receipts = Receipts.objects.filter(item__income_group__type_cf=3)
        payments = Payments.objects.filter(item__expense_group__type_cf=3)
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
                receipts_before = Receipts.objects.none()
                payments_before = Payments.objects.none()
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
            receipts_sum = receipts.aggregate(Sum("amount")).get('amount__sum', 0.00)
            if receipts_sum is None:
                receipts_sum = 0
            payments = payments.filter(counterparty=agent.counterparty)
            payments_sum = payments.aggregate(Sum("amount")).get('amount__sum', 0.00)
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
            receipts_sum = receipts.aggregate(Sum("amount")).get('amount__sum', 0.00)
            if receipts_sum == None: receipts_sum = 0

            receipts_before = receipts_before.filter(counterparty=agent.counterparty)
            receipts_before_sum = receipts_before.aggregate(Sum("amount")).get('amount__sum', 0.00)
            if receipts_before_sum == None: receipts_before_sum = 0

            payments = payments.filter(counterparty=agent.counterparty)
            payments_sum = payments.aggregate(Sum("amount")).get('amount__sum', 0.00)
            if payments_sum == None: payments_sum = 0

            payments_before = payments_before.filter(counterparty=agent.counterparty)
            payments_before_sum = payments_before.aggregate(Sum("amount")).get('amount__sum', 0.00)
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
            amount = float(i.amount)
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


def ChartsInvestView(request):
    form = DashboardFilter(request.GET)
    receipts = Receipts.objects.all()
    payments = Payments.objects.all()

    if form.is_valid():

        if form.cleaned_data['organization']:
            receipts = receipts.filter(organization=form.cleaned_data['organization'])
            payments = payments.filter(organization=form.cleaned_data['organization'])
        if form.cleaned_data['date_start']:
            receipts = receipts.filter(date__gte=form.cleaned_data['date_start'])
            payments = payments.filter(date__gte=form.cleaned_data['date_start'])
        if form.cleaned_data['date_end']:
            receipts = receipts.filter(date__lte=form.cleaned_data['date_end'])
            payments = payments.filter(date__lte=form.cleaned_data['date_end'])

        # if form.cleaned_data['conversion_currency']:
        #     payments = payments
        #     payments = payments
        # for i in payments:
        #     i.amount = i.amount * get_currency_rate(i.currency, form.cleaned_data['conversion_currency'], i.date)
        #     print(i)
        # for i in payments:
        #     i.amount = i.amount * get_currency_rate(i.currency, form.cleaned_data['conversion_currency'], i.date)
        #     print(i)

    def get_structure(flow):
        structure = {}
        for i in flow:
            item = str(i.item)
            amount = float(i.amount)
            if item not in structure:
                structure[item] = amount
            else:
                structure[item] += amount
        return list(map(list, list(zip(list(structure), list(structure.values())))))

    # print('rec_struc:', get_structure(payments))
    # print('pay_struc:', get_structure(payments))

    def get_dynamics(flow):
        dynamics = {}
        for i in flow:
            month = str(i.date.month).rjust(2, '0')
            period = f'{str(i.date.year)}/{month}'
            amount = float(i.amount)
            if period not in dynamics:
                dynamics[period] = amount
            else:
                dynamics[period] += amount

        return dynamics

    # print('rec_dyn:', get_dynamics(payments))
    # print('pay_dyn:', get_dynamics(payments))

    # data payments and payments
    def get_total_cf():
        payments_dynamics = get_dynamics(payments)
        receipts_dynamics = get_dynamics(receipts)

        total_cf = {k: [receipts_dynamics.get(k, 0), payments_dynamics.get(k, 0)]
                    for k in set(receipts_dynamics) | set(payments_dynamics)}
        total_cf = sorted(total_cf.items(), key=lambda x: x[0])
        total_cf = dict(total_cf)

        return total_cf

    # print('total_cf:', get_total_cf())

    # diagr 2 total cash flow
    def get_cf_dynamics():
        total_cf = get_total_cf()
        cf_dynamics = []
        for k, v in total_cf.items():
            cf_dynamics.append([k, *v, v[0] - v[1]])

        return cf_dynamics

    # print('cf_dynamics:', get_cf_dynamics())

    # diagr 3 cf table
    def get_cf_table():
        cf_table = {}
        receipts_sum = receipts.aggregate(Sum("amount")).get('amount__sum', 0.00)
        payments_sum = payments.aggregate(Sum("amount")).get('amount__sum', 0.00)
        if receipts_sum == None:
            receipts_sum = 0
        if payments_sum == None:
            payments_sum = 0
        cf = receipts_sum - payments_sum

        cf_table['total payments'] = int(receipts_sum)
        cf_table['total payments'] = int(payments_sum)
        cf_table['total cf'] = int(cf)

        return list(map(list, list(zip(list(cf_table), list(cf_table.values())))))

    # print('cf_table:', get_cf_table())

    # diagr 6 payments and payments dynamics
    def get_rp_dynamics():
        total_cf = get_total_cf()
        rp_dynamics = []
        for k, v in total_cf.items():
            rp_dynamics.append([k, *v])

        return rp_dynamics

    # print('rp_dynamics:', get_rp_dynamics())

    context = {
        'form': form,
        'today': datetime.today(),
        # 'balances': balances,
        'cf_dynamics': get_cf_dynamics(),
        'cf_table': get_cf_table(),
        'receipts_structure': get_structure(receipts),
        'payments_structure': get_structure(payments),
        'rp_dynamics': get_rp_dynamics(),
    }

    return render(request, 'registers/charts_fin.html', context=context)
