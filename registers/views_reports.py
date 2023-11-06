import datetime
import decimal

import numpy as np
import pandas as pd

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, UpdateView

from directory.models import PaymentAccount, Currencies, CurrenciesRates
from payments.models import Payments
from receipts.models import Receipts, ChangePayAccount
from registers.forms import AccountBalancesFilter, AccountSettingsSet, DashboardFilter, CFStatementFilter
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
        receipts = Receipts.objects.all()
        receipts_before = Receipts.objects.all()
        payments = Payments.objects.all()
        payments_before = Payments.objects.all()
        change_account = ChangePayAccount.objects.all()
        change_account_before = ChangePayAccount.objects.all()

        form = AccountBalancesFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['organization']:
                accounts = accounts.filter(organization=form.cleaned_data['organization'])
                change_account = change_account.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['currency']:
                accounts = accounts.filter(currency=form.cleaned_data['currency'])
                change_account = change_account.filter(currency=form.cleaned_data['currency'])
            if form.cleaned_data['is_cash']:
                accounts = accounts.filter(is_cash=True)
                change_account = change_account.filter(is_cash=True)
            if form.cleaned_data['date_start']:
                receipts = receipts.filter(date__gte=form.cleaned_data['date_start'])
                payments = payments.filter(date__gte=form.cleaned_data['date_start'])
                change_account = change_account.filter(date__gte=form.cleaned_data['date_start'])
                receipts_before = receipts_before.filter(date__lte=form.cleaned_data['date_start'])
                payments_before = payments_before.filter(date__lte=form.cleaned_data['date_start'])
                change_account_before = change_account_before.filter(date__lte=form.cleaned_data['date_start'])
            else:
                receipts_before = Receipts.objects.none()
                payments_before = Payments.objects.none()
                change_account_before = Payments.objects.none()

            if form.cleaned_data['date_end']:
                receipts = receipts.filter(date__lte=form.cleaned_data['date_end'])
                payments = payments.filter(date__lte=form.cleaned_data['date_end'])
                change_account = change_account.filter(date__lte=form.cleaned_data['date_end'])

        account_balances, balances_convert = AccountBalancesView.get_balances(
            accounts, receipts, payments, receipts_before, payments_before, change_account, change_account_before)
        return {
            "account_balances": account_balances,
            "balances_convert": balances_convert,
        }

    @staticmethod
    def htmx_list(request):
        context = {'object_list': AccountBalancesView.account_balances_queryset(request)}

        return render(request, 'registers/account_balances_list.html', context=context)

    @staticmethod
    def get_balances(accounts, receipts, payments, receipts_before, payments_before, change_account,
                     change_account_before):

        main_currency = AccountSettings.load().currency()
        account_balances = []
        balances_convert = []
        receipts_before_sum_convert = 0
        payments_before_sum_convert = 0
        receipts_sum_convert = 0
        payments_sum_convert = 0

        for account in accounts:
            rate = AccountBalancesView.get_rate(account.currency, main_currency)

            receipts_sum = receipts.filter(account=account).aggregate(Sum("amount")).get('amount__sum', 0.00)
            if receipts_sum is None:
                receipts_sum = 0

            payments_sum = payments.filter(account=account).aggregate(Sum("amount")).get('amount__sum', 0.00)
            if payments_sum is None:
                payments_sum = 0

            receipts_before_sum = receipts_before.filter(account=account).aggregate(Sum("amount")).get(
                'amount__sum', 0.00)
            if receipts_before_sum is None:
                receipts_before_sum = 0

            payments_before_sum = payments_before.filter(account=account).aggregate(Sum("amount")).get(
                'amount__sum', 0.00)
            if payments_before_sum is None:
                payments_before_sum = 0

            change_pay_sum = change_account.filter(pay_account_from=account).aggregate(Sum("amount")).get(
                'amount__sum', 0.00)
            if change_pay_sum is None:
                change_pay_sum = 0

            change_rec_sum = change_account.filter(pay_account_to=account).aggregate(Sum("amount")).get(
                'amount__sum', 0.00)
            if change_rec_sum is None:
                change_rec_sum = 0

            change_pay_before_sum = change_account_before.filter(pay_account_from=account).aggregate(
                Sum("amount")).get('amount__sum', 0.00)
            if change_pay_before_sum is None:
                change_pay_before_sum = 0

            change_rec_before_sum = change_account_before.filter(pay_account_to=account).aggregate(
                Sum("amount")).get('amount__sum', 0.00)
            if change_rec_before_sum is None:
                change_rec_before_sum = 0

            start_balance = receipts_before_sum + change_rec_before_sum - payments_before_sum - change_pay_before_sum
            final_balance = start_balance + receipts_sum + change_rec_sum - payments_sum - change_pay_sum

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


class AccountBalancesView1(ListView):
    model = PaymentAccount
    template_name = 'registers/account_balances.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = {
            'object_list': self.balances_queryset(self.request),
            'form': AccountBalancesFilter()}
        return ctx

    @staticmethod
    def balances_queryset(request):
        receipts = Receipts.objects.all()
        payments = Payments.objects.all()
        change_account = ChangePayAccount.objects.all()

        pool_before = []
        pool = []

        pool.append({'account': receipts.account, 'date': receipts.date,
                     'amount': receipts.amount, 'organization': receipts.organization,
                     'currency': receipts.currency, 'is_cash': receipts.account__is_cash})

        pool.append({'account': payments.account, 'date': payments.date,
                     'amount': -payments.amount, 'organization': payments.organization,
                     'currency': payments.currency, 'is_cash': payments.account__is_cash})

        pool.append({'account': change_account.pay_account_from, 'date': change_account.date,
                     'amount': -change_account.amount, 'organization': change_account.organization,
                     'currency': change_account.currency, 'is_cash': change_account.account__is_cash})

        pool.append({'account': change_account.pay_account_to, 'date': change_account.date,
                     'amount': change_account.amount, 'organization': change_account.organization,
                     'currency': change_account.currency, 'is_cash': change_account.account__is_cash})


        form = AccountBalancesFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['organization']:
                pool = pool.filter(organization=form.cleaned_data['organization'])
                receipts = receipts.filter(organization=form.cleaned_data['organization'])
                payments = payments.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['currency']:
                pool = pool.filter(currency=form.cleaned_data['currency'])
                receipts = receipts.filter(currency=form.cleaned_data['currency'])
                payments = payments.filter(currency=form.cleaned_data['currency'])
            if form.cleaned_data['is_cash']:
                pool = pool.filter(is_cash=True)
                receipts = receipts.filter(is_cash=True)
                payments = payments.filter(is_cash=True)
            if form.cleaned_data['date_start']:
                pool = pool.filter(date__gte=form.cleaned_data['date_start'])
                receipts = receipts.filter(date__gte=form.cleaned_data['date_start'])
                payments = payments.filter(date__gte=form.cleaned_data['date_start'])
                pool_before = pool.filter(date__lte=form.cleaned_data['date_start'])
            else:
                pool_before = []
            if form.cleaned_data['date_end']:
                pool = pool.filter(date__lte=form.cleaned_data['date_end'])
                receipts = receipts.filter(date__lte=form.cleaned_data['date_end'])
                payments = payments.filter(date__lte=form.cleaned_data['date_end'])

        account_balances, balances_convert = AccountBalancesView.get_balances(pool, pool_before, receipts, payments)

        return {
            "account_balances": account_balances,
            "balances_convert": balances_convert,
        }

    @staticmethod
    def htmx_list(request):
        context = {'object_list': AccountBalancesView.balances_queryset(request)}

        return render(request, 'registers/account_balances_list.html', context=context)

    @staticmethod
    def get_balances(pool, pool_before, receipts, payments):
        accounts = PaymentAccount.objects.all()
        main_currency = AccountSettings.load().currency()
        account_balances = []
        balances_convert = []
        sum_convert = 0
        sum_before_convert = 0
        receipts_sum_convert = 0
        payments_sum_convert = 0

        for account in accounts:
            rate = AccountBalancesView.get_rate(account.currency, main_currency)

            sum = pool.filter(account=account).aggregate(Sum("amount")).get('amount__sum', 0.00)
            if sum is None:
                sum = 0

            sum_before = pool_before.filter(account=account).aggregate(Sum("amount")).get('amount__sum', 0.00)
            if sum_before is None:
                sum_before = 0

            receipts_sum = receipts.filter(account=account).aggregate(Sum("amount")).get('amount__sum', 0.00)
            if receipts_sum is None:
                receipts_sum = 0

            payments_sum = receipts.filter(account=account).aggregate(Sum("amount")).get('amount__sum', 0.00)
            if payments_sum is None:
                payments_sum = 0

            start_balance = sum_before
            final_balance = start_balance + sum

            account_balances.append({'account': account.account, 'organization': account.organization.organization,
                                     'currency': account.currency.code, 'is_cash': account.is_cash,
                                     'start_balance': int(start_balance), 'receipts_sum': int(receipts_sum),
                                     'payments_sum': int(payments_sum), 'final_balance': int(final_balance)})

            receipts_sum_convert += receipts_sum / rate
            payments_sum_convert += payments_sum / rate
            sum_convert += sum_before / rate
            sum_before_convert += sum / rate

        start_balance_convert = sum_before_convert
        final_balance_convert = start_balance_convert + sum_convert

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


class CfStatementView(ListView):
    model = Payments
    template_name = 'registers/cf_statement.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = {'object_list': CfStatementView.cf_statement_queryset(self.request),
               'form': CFStatementFilter()}
        return ctx

    @staticmethod
    def cf_statement_queryset(request):
        receipts = Receipts.objects.all()
        payments = Payments.objects.all()
        form = CFStatementFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['activities']:
                receipts = receipts.filter(item__income_group__type_cf__type=form.cleaned_data['activities'])
                payments = payments.filter(item__expense_group__type_cf__type=form.cleaned_data['activities'])
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
        # print(payments)

        payments = payments.values('date', 'item__expense_group__expense_group', 'item__expense_item', 'amount')
        data_payments = pd.DataFrame(payments)
        data_payments = data_payments.rename(
            columns={'month': 'Month', 'item__expense_item': 'Items', 'item__expense_group__expense_group': 'Groups'})
        if not data_payments.empty:
            data_payments['amount'] = data_payments['amount'].apply(lambda x: x * -1)

        receipts = receipts.values('date', 'item__income_group__income_group', 'item__income_item', 'amount')
        data_receipts = pd.DataFrame(receipts)
        data_receipts = data_receipts.rename(
            columns={'month': 'Month', 'item__income_item': 'Items', 'item__income_group__income_group': 'Groups'})

        data = pd.concat([data_receipts, data_payments], ignore_index=True)

        data['Month'] = pd.DatetimeIndex(data['date']).month
        data['amount'] = data['amount'].astype(int)

        data = pd.pivot_table(data, index=['Items'], columns='Month', values='amount',
                              aggfunc='sum', margins=True, margins_name='Total', fill_value=0)
        items = data.index.tolist()
        data = data.values.tolist()

        # data = list(zip(items, *data))
        # data = list(map(list, data))

        return data

    @staticmethod
    def htmx_list(request):
        context = {'object_list': CfStatementView.cf_statement_queryset(request)}

        return render(request, 'registers/cf_statement_list.html', context=context)


def CfBudgetView(request):
    return render(request, 'registers/cf_budget.html')


def PlanFactAnalysisView(request):
    return render(request, 'registers/plan_fact_analysis.html')
