from django.shortcuts import render, redirect
from django.views.generic import UpdateView, ListView

from directory.models import PaymentAccount, CurrenciesRates
from payments.models import Payments
from receipts.models import Receipts
from registers.forms import AccountSettingsSet, AccountBalancesFilter
from registers.models import AccountSettings

from itertools import chain


class AccountSettingsView(UpdateView):
    model = AccountSettings
    template_name = 'registers/settings.html'
    form_class = AccountSettingsSet
    success_url = '/settings'

    def get_object(self):
        return self.model.load()


def AccountBalancesView(request):
    form = AccountBalancesFilter(request.GET)
    accounts = PaymentAccount.objects.all()
    income = Receipts.objects.all()
    payments = Payments.objects.all()
    object_list = {}

    if form.is_valid():
        if form.cleaned_data['organization']:
            accounts = accounts.filter(organization=form.cleaned_data['organization'])
        if form.cleaned_data['currency']:
            accounts = accounts.filter(currency=form.cleaned_data['currency'])
        if form.cleaned_data['is_cash']:
            accounts = accounts.filter(is_cash=form.cleaned_data['is_cash'])
        for i in accounts:
            object_list[i.account] = [i.organization, i.currency, i.is_cash]

        # gte after, lte before
        # for i in accounts:
        #     if form.cleaned_data['date_start']:
        #         pay_before_start = payments.filter(account=accounts, date__lte=form.cleaned_data['date'])
        #         pay_sum_before_start = pay_before_start.aggregate(sum=sum('amount'))['amount']
        #         income_before_start = income.filter(account=accounts, date__lte=form.cleaned_data['date'])
        #         income_sum_before_start = income_before_start.aggregate(sum=sum('amount'))['amount']
        #         pay_after_start = payments.filter(account=accounts, date__gte=form.cleaned_data['date'])
        #         income_after_start = income.filter(account=accounts, date__gte=form.cleaned_data['date'])
        #     if form.cleaned_data['date_end']:
        #         pay_in_period = pay_after_start.filter(date__lte=form.cleaned_data['date'])
        #         pay_sum_in_period = pay_in_period.aggregate(sum=sum('amount'))['amount']
        #         income_in_period = income_after_start.filter(date__lte=form.cleaned_data['date'])
        #         income_sum_in_period = income_in_period.aggregate(sum=sum('amount'))['amount']
        #
        #     object_list = {}
        #     balance_open =
        #     balance_start = balance_open + income_sum_before_start - pay_sum_before_start
        #     balance_end = balance_start + income_sum_in_period - pay_sum_in_period

        # if form.cleaned_data['conversion_currency']:
        #     accounts = accounts.filter(conversion_currency=form.cleaned_data['conversion_currency'])


    context = {'object_list': object_list,
               'accounts': accounts,
               'form': AccountBalancesFilter(),
               }

    return render(request, 'registers/account_balances.html', context=context)



def HomeView(request):
    return render(request, 'registers/home.html')


def ReportsView(request):
    return render(request, 'registers/reports.html')


def DashboardView(request):
    return render(request, 'registers/dashboard.html')


def CfStatementView(request):
    return render(request, 'registers/cf_statement.html')


def CfBudgetView(request):
    return render(request, 'registers/cf_budget.html')


def PlanFactAnalysisView(request):
    return render(request, 'registers/plan_fact_analysis.html')






