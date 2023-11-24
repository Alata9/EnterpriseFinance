import csv
import datetime
import decimal
from io import BytesIO, StringIO

import numpy as np
import pandas as pd

from django.db.models import Sum
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.views.generic import ListView, UpdateView

from directory.models import PaymentAccount, Currencies, CurrenciesRates
# from payments.models import Payments
# from payments.models import Receipts, ChangePayAccount
from payments.models import PaymentDocuments
from planning.models import PaymentDocumentPlan
from registers.forms import (AccountSettingsSet, AccountBalancesFilter, AccountFlowsFilter, CFStatementFilter,
                             CounterpartyFlowsFilter
    # ,  DashboardFilter, CFStatementFilter
                             )
from registers.models import AccountSettings


def HomeView(request):
    return render(request, 'registers/home.html')


class AccountSettingsView(UpdateView):
    model = AccountSettings
    template_name = 'registers/settings.html'
    form_class = AccountSettingsSet
    success_url = '/settings'

    def get_object(self):
        return self.model.load()


class AccountBalancesView(ListView):
    model = PaymentAccount
    template_name = 'registers/account_balances.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = {
            'object_list': self.account_balances_queryset(self.request),
            'form': AccountBalancesFilter()}
        return ctx

    @staticmethod
    def account_balances_queryset(request):
        accounts = PaymentAccount.objects.all()
        receipts = PaymentDocuments.objects.all()
        receipts_before = PaymentDocuments.objects.all()
        payments = PaymentDocuments.objects.all()
        payments_before = PaymentDocuments.objects.all()

        form = AccountBalancesFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['organization']:
                accounts = accounts.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['currency']:
                accounts = accounts.filter(currency=form.cleaned_data['currency'])
            if form.cleaned_data['is_cash']:
                accounts = accounts.filter(is_cash=True)
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

        account_balances, balances_convert = AccountBalancesView.get_balances(
            accounts, receipts, payments, receipts_before, payments_before)
        return {
            "account_balances": account_balances,
            "balances_convert": balances_convert,
        }

    @staticmethod
    def htmx_list(request):
        context = {'object_list': AccountBalancesView.account_balances_queryset(request)}

        return render(request, 'registers/account_balances_list.html', context=context)

    @staticmethod
    def get_balances(accounts, receipts, payments, receipts_before, payments_before):

        main_currency = AccountSettings.load().currency()
        account_balances = []
        balances_convert = []
        receipts_before_sum_convert = 0
        payments_before_sum_convert = 0
        receipts_sum_convert = 0
        payments_sum_convert = 0

        for account in accounts:
            rate = AccountBalancesView.get_rate(account.currency, main_currency)

            receipts_sum = receipts.filter(account=account).aggregate(Sum("inflow_amount")).get('inflow_amount__sum',
                                                                                                0.00)
            if receipts_sum is None:
                receipts_sum = 0

            payments_sum = payments.filter(account=account).aggregate(Sum("outflow_amount")).get('outflow_amount__sum',
                                                                                                 0.00)
            if payments_sum is None:
                payments_sum = 0

            receipts_before_sum = receipts_before.filter(account=account).aggregate(Sum("inflow_amount")).get(
                'inflow_amount__sum', 0.00)
            if receipts_before_sum is None:
                receipts_before_sum = 0

            payments_before_sum = payments_before.filter(account=account).aggregate(Sum("outflow_amount")).get(
                'outflow_amount__sum', 0.00)
            if payments_before_sum is None:
                payments_before_sum = 0

            start_balance = receipts_before_sum - payments_before_sum
            final_balance = start_balance + receipts_sum - payments_sum

            account_balances.append({'account': account.account, 'organization': account.organization.organization,
                                     'currency': account.currency.code, 'is_cash': account.is_cash,
                                     'start_balance': int(start_balance), 'receipts_sum': int(receipts_sum),
                                     'payments_sum': int(payments_sum), 'final_balance': int(final_balance)})

            receipts_sum_convert += receipts_sum / rate
            payments_sum_convert += payments_sum / rate
            receipts_before_sum_convert += receipts_before_sum / rate
            payments_before_sum_convert += payments_before_sum / rate

        start_balance_convert = receipts_before_sum_convert - payments_before_sum_convert
        final_balance_convert = start_balance_convert + receipts_sum_convert - payments_sum_convert

        balances_convert.append({'currency': main_currency,
                                 'start_balance': int(start_balance_convert),
                                 'receipts_sum': int(receipts_sum_convert),
                                 'payments_sum': int(payments_sum_convert),
                                 'final_balance': int(final_balance_convert)})

        return account_balances, balances_convert

    @staticmethod  # add a condition for the absence of a pair of currencies
    def get_rate(cur, main_currency):
        if cur == main_currency:
            return decimal.Decimal(1)
        try:
            rate = CurrenciesRates.objects.filter(accounting_currency=main_currency, currency=cur,
                                                  date__lte=datetime.datetime.now()).order_by('-date')[:1].first().rate
        except:
            rate = decimal.Decimal(1)

        return rate


class CounterpartyFlowsView(ListView):
    model = PaymentDocuments
    template_name = 'registers/counterparty_flows.html'

    def get_queryset(self):
        return PaymentDocuments.objects.all().order_by('date')

    def get(self, request, *args, **kwargs):
        if 'btn_to_file' in request.GET:
            return self.to_file(request)
        return super().get(request, *args, **kwargs)

    def to_file(self, request):
        my_data = [['header'],
                   ["Date", "Counterparty", "Inflow", "Outflow", "Currency", "Item", "Project", "Comments"]]

        flows = self.flows_queryset(request)
        for i in flows:
            my_data.append([i.date, i.counterparty, i.inflow_amount, i.inflow_amount, i.currency,
                            i.item, i.project, i.comments])

        t = str(datetime.datetime.today().strftime('%d-%m-%Y-%H%M%S'))
        file_name = 'account_flows_' + t + '.csv'
        file_buffer = StringIO()

        writer = csv.writer(file_buffer, delimiter=';')
        writer.writerows(my_data)
        file_bytes = BytesIO(file_buffer.getvalue().encode('cp1251'))
        file_bytes.seek(0)

        response = FileResponse(file_bytes, filename=file_name, as_attachment=True)

        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = {
            'object_list': self.flows_queryset(self.request),
            'form': CounterpartyFlowsFilter()}
        return ctx

    @staticmethod
    def flows_queryset(request):
        flows = PaymentDocuments.objects.all().order_by('date')
        form = CounterpartyFlowsFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['date']:
                flows = flows.filter(date__gte=form.cleaned_data['date'])
            if form.cleaned_data['date_end']:
                flows = flows.filter(date__lte=form.cleaned_data['date_end'])
            if form.cleaned_data['counterparty']:
                flows = flows.filter(counterparty=form.cleaned_data['counterparty'])

        total = AccountFlowsView.get_total(flows)
        return {
            'flows': flows,
            'total': total,
        }

    @staticmethod
    def htmx_list(request):
        context = {'object_list': CounterpartyFlowsView.flows_queryset(request)}

        return render(request, 'registers/counterparty_flow_list.html', context=context)

    @staticmethod
    def get_total(flows):
        total = []
        inflow_sum = flows.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
        if inflow_sum is None:
            inflow_sum = 0

        outflow_sum = flows.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
        if outflow_sum is None:
            outflow_sum = 0

        total.append({'inflow_total': inflow_sum, 'outflow_total': outflow_sum})

        return total


class AccountFlowsView(ListView):
    model = PaymentDocuments
    template_name = 'registers/general_flows.html'

    def get_queryset(self):
        return PaymentDocuments.objects.all().order_by('date')

    def get(self, request, *args, **kwargs):
        if 'btn_to_file' in request.GET:
            return self.to_file(request)
        return super().get(request, *args, **kwargs)

    def to_file(self, request):
        my_data = [['header'],
                   ["Date", "Counterparty", "Inflow", "Outflow", "Currency", "Item", "Project", "Comments"]]

        flows = self.flows_queryset(request)
        for i in flows:
            my_data.append([i.date, i.counterparty, i.inflow_amount, i.inflow_amount, i.currency,
                            i.item, i.project, i.comments])

        t = str(datetime.datetime.today().strftime('%d-%m-%Y-%H%M%S'))
        file_name = 'account_flows_' + t + '.csv'
        file_buffer = StringIO()

        writer = csv.writer(file_buffer, delimiter=';')
        writer.writerows(my_data)
        file_bytes = BytesIO(file_buffer.getvalue().encode('cp1251'))
        file_bytes.seek(0)

        response = FileResponse(file_bytes, filename=file_name, as_attachment=True)

        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = {
            'object_list': self.flows_queryset(self.request),
            'form': AccountFlowsFilter()}
        return ctx

    @staticmethod
    def flows_queryset(request):
        flows = PaymentDocuments.objects.all().order_by('date')
        form = AccountFlowsFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['date']:
                flows = flows.filter(date__gte=form.cleaned_data['date'])
            if form.cleaned_data['date_end']:
                flows = flows.filter(date__lte=form.cleaned_data['date_end'])
            if form.cleaned_data['account']:
                flows = flows.filter(account=form.cleaned_data['account'])

        total = AccountFlowsView.get_total(flows)
        return {
            'flows': flows,
            'total': total,
        }

    @staticmethod
    def htmx_list(request):
        context = {'object_list': AccountFlowsView.flows_queryset(request)}

        return render(request, 'registers/general_flow_list.html', context=context)

    @staticmethod
    def get_total(flows):
        total = []
        inflow_sum = flows.aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
        if inflow_sum is None:
            inflow_sum = 0

        outflow_sum = flows.aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
        if outflow_sum is None:
            outflow_sum = 0

        total.append({'inflow_total': inflow_sum, 'outflow_total': outflow_sum})

        return total


def CfStatementView(request):
    return render(request, 'registers/cf_statement_list.html')


class CfBudgetView(ListView):
    model = PaymentDocumentPlan
    template_name = 'registers/cf_budget.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = {'object_list': CfBudgetView.cf_budget_queryset(self.request),
               'form': CFStatementFilter()}
        return ctx

    @staticmethod
    def cf_budget_queryset(request):
        frequency = 'by_month'
        organization = AccountSettings.load().organization()
        date_start = datetime.datetime.today()
        date_end = datetime.datetime.today()
        project = ''

        receipts = PaymentDocumentPlan.objects.filter(flow="Receipts")
        fin_receipts_loans = receipts.filter(item__group='Loans')
        invest_receipts_assets = receipts.filter(item__group='Fixed_assets')
        invest_receipts_project = receipts.filter(item__group='New_projects')
        oper_receipts_sales = receipts.filter(item__group='Sales_income')
        oper_receipts_other = receipts.filter(item__group='Other')

        payments = PaymentDocumentPlan.objects.filter(flow="Payments")
        fin_payments_loans = payments.filter(item__group='Loans')
        invest_payments_assets = payments.filter(item__group='Fixed_assets')
        invest_payments_project = payments.filter(item__group='New_projects')
        oper_payments_other = payments.filter(item__group='Other')
        oper_payments_adm = payments.filter(item__group='Administrative_expenses')
        oper_payments_direct = payments.filter(item__group='Direct_expenses')
        oper_payment_commer = payments.filter(item__group='Commercial_expenses')
        oper_payment_product = payments.filter(item__group='Production_costs')

        form = CFStatementFilter(request.GET)
        if form.is_valid():
            # if form.cleaned_data['frequency']:
            #     frequency = form.cleaned_data['frequency']
            if form.cleaned_data['organization']:
                organization = form.cleaned_data['organization']
                fin_receipts_loans = fin_receipts_loans.filter(organization=form.cleaned_data['organization'])
                fin_payments_loans = fin_payments_loans.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['project']:
                fin_receipts_loans = fin_receipts_loans.filter(project=form.cleaned_data['project'])
                fin_payments_loans = fin_payments_loans.filter(project=form.cleaned_data['project'])
            if form.cleaned_data['date_start']:
                date_start = form.cleaned_data['date_start']
                fin_receipts_loans = fin_receipts_loans.filter(date__gte=form.cleaned_data['date_start'])
                fin_payments_loans = fin_payments_loans.filter(date__gte=form.cleaned_data['date_start'])
            if form.cleaned_data['date_end']:
                date_end = form.cleaned_data['date_end']
                fin_receipts_loans = fin_receipts_loans.filter(date__lte=form.cleaned_data['date_end'])
                fin_payments_loans = fin_payments_loans.filter(date__lte=form.cleaned_data['date_end'])

            data_fin_payments_loans = CfBudgetView.get_data_pivot(fin_payments_loans, frequency)

            return {
                    'today': datetime.datetime.today(),
                    'organization': organization,
                    'project': project,
                    'date_start': date_start,
                    'date_end': date_end,
                    'measuring': 'kUSD',
                    'fin_payments_loans': fin_payments_loans,
                    'data_fin_payments_loans': data_fin_payments_loans,
                    }

    @staticmethod
    def htmx_list(request):
        context = {'object_list': CfStatementView.cf_budget_queryset(request)}

        return render(request, 'registers/cf_budget.html', context=context)

    @staticmethod
    def get_data_pivot(doc, frequency):
        if doc.first().flow == "Payments":
            doc = doc.values('date', 'item__name', 'outflow_amount')
            data = pd.DataFrame(doc)
            data = data.rename(columns={'outflow_amount': 'amount', 'item__name': 'item'})
        else:
            doc = doc.values('date', 'item', 'inflow_amount')
            data = pd.DataFrame(doc)
            data = data.rename(columns={'inflow_amount': 'amount'})

        data['amount'] = data['amount'].astype(int)

        if frequency == 'by_month':
            data['month'] = data['date'].apply(lambda x: f'{x.month}/{x.year}')


        data_pivot = pd.pivot_table(data, index=['item'], columns='month', values='amount',
                                    aggfunc='sum', margins=True, margins_name='Total', fill_value=0)
        print(data_pivot)
        items = data_pivot.index.tolist()
        values = data_pivot.values.tolist()
        data = list(zip(items, values))
        print(data)
        return data


def PlanFactAnalysisView(request):
    return render(request, 'registers/plan_fact_analysis.html')
