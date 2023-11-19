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
from registers.forms import (AccountSettingsSet, AccountBalancesFilter, AccountFlowsFilter
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

            receipts_sum = receipts.filter(account=account).aggregate(Sum("inflow_amount")).get('inflow_amount__sum', 0.00)
            if receipts_sum is None:
                receipts_sum = 0

            payments_sum = payments.filter(account=account).aggregate(Sum("outflow_amount")).get('outflow_amount__sum', 0.00)
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

    @staticmethod                                       # add a condition for the absence of a pair of currencies
    def get_rate(cur, main_currency):
        if cur == main_currency:
            return decimal.Decimal(1)
        try:
            rate = CurrenciesRates.objects.filter(accounting_currency=main_currency, currency=cur,
                                                  date__lte=datetime.datetime.now()).order_by('-date')[:1].first().rate
        except:
            rate = decimal.Decimal(1)

        return rate


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

# class CfStatementView(ListView):
#     model = Payments
#     template_name = 'registers/cf_statement.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         ctx = {'object_list': CfStatementView.cf_statement_queryset(self.request),
#                'form': CFStatementFilter()}
#         return ctx
#
#     @staticmethod
#     def cf_statement_queryset(request):
#         receipts = Receipts.objects.all()
#         payments = Payments.objects.all()
#         form = CFStatementFilter(request.GET)
#         if form.is_valid():
#             if form.cleaned_data['activities']:
#                 receipts = receipts.filter(item__income_group__type_cf__type=form.cleaned_data['activities'])
#                 payments = payments.filter(item__expense_group__type_cf__type=form.cleaned_data['activities'])
#             if form.cleaned_data['organization']:
#                 receipts = receipts.filter(organization=form.cleaned_data['organization'])
#                 payments = payments.filter(organization=form.cleaned_data['organization'])
#             if form.cleaned_data['project']:
#                 receipts = receipts.filter(project=form.cleaned_data['project'])
#                 payments = payments.filter(project=form.cleaned_data['project'])
#             if form.cleaned_data['date_start']:
#                 receipts = receipts.filter(date__gte=form.cleaned_data['date_start'])
#                 payments = payments.filter(date__gte=form.cleaned_data['date_start'])
#             if form.cleaned_data['date_end']:
#                 receipts = receipts.filter(date__lte=form.cleaned_data['date_end'])
#                 payments = payments.filter(date__lte=form.cleaned_data['date_end'])
#         # print(payments)
#
#         payments = payments.values('date', 'item__expense_group__expense_group', 'item__expense_item', 'amount')
#         data_payments = pd.DataFrame(payments)
#         data_payments = data_payments.rename(
#             columns={'month': 'Month', 'item__expense_item': 'Items', 'item__expense_group__expense_group': 'Groups'})
#         if not data_payments.empty:
#             data_payments['amount'] = data_payments['amount'].apply(lambda x: x * -1)
#
#         receipts = receipts.values('date', 'item__income_group__income_group', 'item__income_item', 'amount')
#         data_receipts = pd.DataFrame(receipts)
#         data_receipts = data_receipts.rename(
#             columns={'month': 'Month', 'item__income_item': 'Items', 'item__income_group__income_group': 'Groups'})
#
#         data = pd.concat([data_receipts, data_payments], ignore_index=True)
#
#         data['Month'] = pd.DatetimeIndex(data['date']).month
#         data['amount'] = data['amount'].astype(int)
#
#         data = pd.pivot_table(data, index=['Items'], columns='Month', values='amount',
#                               aggfunc='sum', margins=True, margins_name='Total', fill_value=0)
#         items = data.index.tolist()
#         data = data.values.tolist()
#
#         # data = list(zip(items, *data))
#         # data = list(map(list, data))
#
#         return data
#
#     @staticmethod
#     def htmx_list(request):
#         context = {'object_list': CfStatementView.cf_statement_queryset(request)}
#
#         return render(request, 'registers/cf_statement_list.html', context=context)


def CfBudgetView(request):
    return render(request, 'registers/cf_budget.html')


def PlanFactAnalysisView(request):
    return render(request, 'registers/plan_fact_analysis.html')
