from datetime import datetime
from collections import defaultdict
from itertools import chain

from django.db.models import Sum, Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, ListView

from directory.models import PaymentAccount, CurrenciesRates
from payments.models import Payments
from receipts.models import Receipts
from registers.forms import AccountSettingsSet, AccountBalancesFilter, DashboardFilter
from registers.models import AccountSettings
import pandas as pd



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


    context = {'object_list': object_list,
               'accounts': accounts,
               'form': AccountBalancesFilter(),
               }

    return render(request, 'registers/account_balances.html', context=context)


def DashboardView(request):
    form = DashboardFilter(request.GET)
    receipts = Receipts.objects.all()
    payments = Payments.objects.all()

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

        if form.cleaned_data['conversion_currency']:
            receipts = receipts.filter(currency=form.cleaned_data['conversion_currency'])
            payments = payments.filter(currency=form.cleaned_data['conversion_currency'])


    receipts_structure = {}
    for d in receipts:
        item = str(d.item)
        amount = float(d.amount)
        if item not in receipts_structure:
            receipts_structure[item] = amount
        else:
            receipts_structure[item] += amount
    receipts_structure = list(map(list, list(zip(list(receipts_structure), list(receipts_structure.values())))))

    payments_structure = {}
    for d in payments:
        item = str(d.item)
        amount = float(d.amount)
        if item not in payments_structure:
            payments_structure[item] = amount
        else:
            payments_structure[item] += amount
    payments_structure = list(map(list, list(zip(list(payments_structure), list(payments_structure.values())))))


    payments_dynamics = {}
    for i in payments:
        period = f'{str(i.date.year)}/{str(i.date.month)}'
        amount = float(i.amount)
        if period not in payments_dynamics:
            payments_dynamics[period] = amount
        else:
            payments_dynamics[period] += amount
    print(payments_dynamics)
    payments_dynamics = list(map(list, list(zip(list(payments_dynamics), list(payments_dynamics.values())))))


    receipts_dynamics = {}
    for i in receipts:
        period = f'{str(i.date.year)}/{str(i.date.month)}'
        amount = float(i.amount)
        if period not in receipts_dynamics:
            receipts_dynamics[period] = amount
        else:
            receipts_dynamics[period] += amount
    print(receipts_dynamics)
    receipts_dynamics = list(map(list, list(zip(list(receipts_dynamics), list(receipts_dynamics.values())))))

    # rp_dynamics = {}
    # rp_dynamics = defaultdict(list)
    #
    # for key in set(list(receipts_dynamics.keys()) + list(payments_dynamics.keys())):
    #     if key in receipts_dynamics:
    #         rp_dynamics[key].append(receipts_dynamics[key])
    #     if key in payments_dynamics:
    #         rp_dynamics[key].append(payments_dynamics[key])
    #
    # rp_dynamics = list(map(list, list(zip(list(rp_dynamics), list(rp_dynamics.values())))))
    # rp_dynamics = sorted(rp_dynamics)
    #
    # print(rp_dynamics)


    total_cf = {}
    receipts_sum = receipts.aggregate(Sum("amount")).get('amount__sum', 0.00)
    payments_sum = payments.aggregate(Sum("amount")).get('amount__sum', 0.00)
    cf = receipts_sum - payments_sum

    total_cf['total receipts'] = int(receipts_sum)
    total_cf['total payments'] = int(payments_sum)
    total_cf['total cf'] = int(cf)

    total_cf = list(map(list, list(zip(list(total_cf), list(total_cf.values())))))



    context = {'receipts_structure': receipts_structure,
               'payments_structure': payments_structure,
               'receipts_dynamics': receipts_dynamics,
               # 'rp_dynamics': rp_dynamics,
               'total_cf': total_cf,
               # 'cf_dynamics': cf_dynamics,
               'form': form,
               'today': datetime.today()
               }

    return render(request, 'registers/dashboard.html', context=context)


def HomeView(request):
    return render(request, 'registers/home.html')


def ReportsView(request):
    return render(request, 'registers/reports.html')


def CfStatementView(request):
    return render(request, 'registers/cf_statement.html')


def CfBudgetView(request):
    return render(request, 'registers/cf_budget.html')


def PlanFactAnalysisView(request):
    return render(request, 'registers/plan_fact_analysis.html')






