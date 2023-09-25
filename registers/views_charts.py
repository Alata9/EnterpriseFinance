from datetime import datetime
import numpy as np


from django.db.models import Sum, Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, ListView

from directory.models import PaymentAccount, CurrenciesRates, TypeCF, Counterparties
from payments.models import Payments
from receipts.models import Receipts, IncomeItem
from registers.forms import AccountSettingsSet, AccountBalancesFilter, DashboardFilter
from registers.models import AccountSettings



def DashboardView(request):
    form = DashboardFilter(request.GET)

    receipts = Receipts.objects.all()
    receipts_oper = Receipts.objects.filter(item__income_group__type_cf=1)
    receipts_invest = Receipts.objects.filter(item__income_group__type_cf=2)
    receipts_fin = Receipts.objects.filter(item__income_group__type_cf=3)

    payments = Payments.objects.all()
    payments_oper = Payments.objects.filter(item__expense_group__type_cf=1)
    payments_invest = Payments.objects.filter(item__expense_group__type_cf=2)
    payments_fin = Payments.objects.filter(item__expense_group__type_cf=3)


    if form.is_valid():
        if form.cleaned_data['organization']:
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


    # chatr 1: account balanses
    def get_balances():
        account_balances = {}
        accounts = PaymentAccount.objects.values_list('account', flat=True).distinct()

        for i in accounts:
            currency = PaymentAccount.objects.filter(account=i).values_list('currency__code', flat=True)[0]
            open_balance = PaymentAccount.objects.filter(account=i).values_list('open_balance', flat=True)[0]
            receipts = Receipts.objects.filter(account__account=i)
            receipts_sum = receipts.aggregate(Sum("amount")).get('amount__sum', 0.00)
            if receipts_sum == None: receipts_sum = 0
            payments = Payments.objects.filter(account__account=i)
            payments_sum = payments.aggregate(Sum("amount")).get('amount__sum', 0.00)
            if payments_sum == None: payments_sum = 0
            final_balance = open_balance + receipts_sum - payments_sum
            account_balances[i] = [int(final_balance), currency]

        return [[k, *v] for k, v in account_balances.items()]

    # chart 2, 3 cf table and cf bar
    def get_cf_table():
        nonlocal receipts, payments, receipts_oper, payments_oper, \
            receipts_invest, payments_invest, receipts_fin, payments_fin

        cf_table = {}
        receipts_sum = receipts.aggregate(Sum("amount")).get('amount__sum', 0.00)
        if receipts_sum is None:
            receipts_sum = 0
        payments_sum = payments.aggregate(Sum("amount")).get('amount__sum', 0.00)
        if payments_sum is None:
            payments_sum = 0
        receipts_oper = receipts_oper.aggregate(Sum("amount")).get('amount__sum', 0.00)
        if receipts_oper is None:
            receipts_oper = 0
        payments_oper = payments_oper.aggregate(Sum("amount")).get('amount__sum', 0.00)
        if payments_oper is None:
            payments_oper = 0
        receipts_invest = receipts_invest.aggregate(Sum("amount")).get('amount__sum', 0.00)
        if receipts_invest is None:
            receipts_invest = 0
        payments_invest = payments_invest.aggregate(Sum("amount")).get('amount__sum', 0.00)
        if payments_invest is None:
            payments_invest = 0
        receipts_fin = receipts_fin.aggregate(Sum("amount")).get('amount__sum', 0.00)
        if receipts_fin is None:
            receipts_fin = 0
        payments_fin = payments_fin.aggregate(Sum("amount")).get('amount__sum', 0.00)
        if payments_fin is None:
            payments_fin = 0

        cf = receipts_sum - payments_sum
        cf_oper = receipts_oper - payments_oper
        cf_invest = receipts_invest - payments_invest
        cf_fin = receipts_fin - payments_fin

        cf_table['receipts'] = [int(receipts_oper), int(receipts_invest), int(receipts_fin), int(receipts_sum)]
        cf_table['payments'] = [int(payments_oper), int(payments_invest), int(payments_fin), int(payments_sum)]
        cf_table['cash flow'] = [int(cf_oper), int(cf_invest), int(cf_fin), int(cf)]

        cf_table = [[k, *v] for k, v in cf_table.items()]
        cf_bar = [['Operating', cf_table[2][1]], ['Investment', cf_table[2][2]], ['Financing', cf_table[2][3]]]

        return cf_table, cf_bar

    cf_table, cf_bar = get_cf_table()

    # function for getting full data
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

    # get data payments and receipts
    def get_total_cf():
        payments_dynamics = get_dynamics(payments)
        receipts_dynamics = get_dynamics(receipts)

        total_cf = {k: [receipts_dynamics.get(k, 0), payments_dynamics.get(k, 0)]
                    for k in set(receipts_dynamics) | set(payments_dynamics)}
        total_cf = sorted(total_cf.items(), key=lambda x: x[0])
        total_cf = dict(total_cf)

        return total_cf

    # chart 4 total cash flow
    def get_cf_dynamics():
        total_cf = get_total_cf()
        cf_dynamics = []
        for k, v in total_cf.items():
            cf_dynamics.append([k, *v, v[0] - v[1]])

        return cf_dynamics


    context = {
               'form': form,
               'today': datetime.today(),
               'account_balances': get_balances(),
               'cf_table': cf_table,
               'cf_bar': cf_bar,
               'cf_dynamics': get_cf_dynamics(),
               }

    return render(request, 'registers/dashboard.html', context=context)


def ChartsOperView(request):
    form = DashboardFilter(request.GET)
    receipts = Receipts.objects.filter(item__income_group__type_cf=1)
    payments = Payments.objects.filter(item__expense_group__type_cf=1)

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

# charts 1, 2, 4
    def get_structure(flow):
        structure = {}
        for i in flow:
            item = str(i.item)
            amount = float(i.amount)
            if item not in structure:
                structure[item] = amount
            else:
                structure[item] += amount

        structure = sorted(structure.items(), key=lambda x: x[1], reverse=True)
        structure = dict(structure)

        return [[k, v] for k, v in structure.items()]



# function for data payments and receipts
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


# get data payments and receipts for chart 3
    def get_total_cf():
        payments_dynamics = get_dynamics(payments)
        receipts_dynamics = get_dynamics(receipts)

        total_cf = {k: [receipts_dynamics.get(k, 0), payments_dynamics.get(k, 0)]
                    for k in set(receipts_dynamics) | set(payments_dynamics)}
        total_cf = sorted(total_cf.items(), key=lambda x: x[0])
        total_cf = dict(total_cf)

        return total_cf


# chart 3 Dynamics of receipts and payments
    def get_rp_dynamics():
        total_cf = get_total_cf()
        rp_dynamics = []
        for k, v in total_cf.items():
            rp_dynamics.append([k, *v])

        return rp_dynamics


# chart 5 Payments bar by group
    def get_bar_payments(flow):
        structure = {}
        for i in flow:
            items_group = str(i.item.expense_group)
            amount = float(i.amount)
            if items_group not in structure:
                structure[items_group] = amount
            else:
                structure[items_group] += amount
        structure = sorted(structure.items(), key=lambda x: x[1], reverse=True)
        structure = dict(structure)

        return [[k, v] for k, v in structure.items()]


# chart 6 TOP-10 customers
    def get_bar_customers(flow):
        flow = flow.filter(counterparty__customer=True)
        structure = {}
        for i in flow:
            group = str(i.counterparty)
            amount = float(i.amount)
            if flow not in structure:
                structure[group] = amount
            else:
                structure[group] += amount

        top = sorted(structure.items(), key=lambda x: x[1], reverse=True)
        top = dict(top)

        return [[k, v] for k, v in top.items()][:10]


# chart 7 TOP-10 suppliers
    def get_bar_suppliers(flow):
        flow = flow.filter(counterparty__suppliers=True)
        structure = {}
        for i in flow:
            group = str(i.counterparty)
            amount = float(i.amount)
            if flow not in structure:
                structure[group] = amount
            else:
                structure[group] += amount

        top = sorted(structure.items(), key=lambda x: x[1], reverse=True)
        top = dict(top)

        return [[k, v] for k, v in top.items()][:10]


    context = {
               'form': form,
               'today': datetime.today(),
               'payments_bar': get_bar_payments(payments),
               'receipts_structure': get_structure(receipts),
               'payments_structure': get_structure(payments),
               'rp_dynamics': get_rp_dynamics(),
               'top_customers': get_bar_customers(receipts),
               'top_suppliers': get_bar_suppliers(payments),
               }

    return render(request, 'registers/charts_oper.html', context=context)


def htmx_projects(request):
    form = DashboardFilter(request.GET)
    return HttpResponse(form["project"])


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

    return render(request, 'registers/charts_invest.html', context=context)


def ChartsFinView(request):
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

    return render(request, 'registers/charts_fin.html', context=context)












