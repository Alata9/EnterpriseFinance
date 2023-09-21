from datetime import datetime
from collections import defaultdict
from itertools import chain

from django.db.models import Sum, Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, ListView

from directory.models import PaymentAccount, CurrenciesRates, TypeCF
from payments.models import Payments
from receipts.models import Receipts, IncomeItem
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
        if form.cleaned_data['type_cf']:
            receipts = receipts.filter(item__income_group_type=form.cleaned_data['type_cf'])
            payments = payments.filter(item__expense_group_type=form.cleaned_data['type_cf'])
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

        # if form.cleaned_data['conversion_currency']:
        #     receipts = receipts
        #     payments = payments
            # for i in receipts:
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
    # print('rec_struc:', get_structure(receipts))
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

    # print('rec_dyn:', get_dynamics(receipts))
    # print('pay_dyn:', get_dynamics(payments))


    # data payments and receipts
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

        cf_table['total receipts'] = int(receipts_sum)
        cf_table['total payments'] = int(payments_sum)
        cf_table['total cf'] = int(cf)

        return list(map(list, list(zip(list(cf_table), list(cf_table.values())))))
    # print('cf_table:', get_cf_table())

    # diagr 6 receipts and payments dynamics
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






