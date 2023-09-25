import datetime
import pandas as pd

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, UpdateView

from directory.models import PaymentAccount
from payments.models import Payments
from receipts.models import Receipts
from registers.forms import AccountBalancesFilter, AccountSettingsSet, DashboardFilter
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
        ctx = {'object_list': AccountBalancesView.account_balances_queryset(self.request),
               'form': AccountBalancesFilter()}
        return ctx

    @staticmethod
    def account_balances_queryset(request):
        accounts = PaymentAccount.objects.all()
        receipts = Receipts.objects.all()
        receipts_before = Receipts.objects.all()
        payments = Payments.objects.all()
        payments_before = Payments.objects.all()

        form = AccountBalancesFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['organization']:
                accounts = accounts.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['currency']:
                accounts = accounts.filter(currency=form.cleaned_data['currency'])
            if form.cleaned_data['is_cash']:
                accounts = accounts.filter(is_cash=form.cleaned_data['is_cash'])
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

            account_balances = []

            for i in accounts:
                receipts_sum = receipts.filter(account=i).aggregate(Sum("amount")).get('amount__sum', 0.00)
                if receipts_sum is None:
                    receipts_sum = 0

                payments_sum = payments.filter(account=i).aggregate(Sum("amount")).get('amount__sum', 0.00)
                if payments_sum is None:
                    payments_sum = 0

                receipts_before_sum = receipts_before.filter(account=i).aggregate(Sum("amount")).get('amount__sum',
                                                                                                     0.00)
                if receipts_before_sum is None:
                    receipts_before_sum = 0

                payments_before_sum = payments_before.filter(account=i).aggregate(Sum("amount")).get('amount__sum',
                                                                                                     0.00)
                if payments_before_sum is None:
                    payments_before_sum = 0

                start_balance = i.open_balance + receipts_before_sum - payments_before_sum
                final_balance = start_balance + receipts_sum - payments_sum

                account_balances.append({'account': i.account, 'organization': i.organization.organization,
                                         'currency': i.currency.code, 'is_cash': i.is_cash,
                                         'start_balance': int(start_balance), 'receipts_sum': int(receipts_sum),
                                         'payments_sum': int(payments_sum), 'final_balance': int(final_balance)})

            return account_balances

    @staticmethod
    def htmx_list(request):
        context = {'object_list': AccountBalancesView.account_balances_queryset(request)}

        return render(request, 'registers/account_balances_list.html', context=context)



class CfStatementView(ListView):
    model = Payments
    template_name = 'registers/cf_statement.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = {'object_list': CfStatementView.cf_statement_queryset(self.request),
               'form': DashboardFilter()}
        return ctx

    @staticmethod
    def cf_statement_queryset(request):
        receipts = Receipts.objects.filter(item__income_group__type_cf=1)
        payments = Payments.objects.filter(item__expense_group__type_cf=1)

        form = DashboardFilter(request.GET)
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

        data = []

        payments = payments.values('date', 'item__expense_group', 'item', 'amount')
        receipts = receipts.values('date', 'item__income_group', 'item', 'amount')

        print(data)
        return data

    @staticmethod
    def htmx_list(request):
        context = {'object_list': CfStatementView.cf_statement_queryset(request)}

        return render(request, 'registers/cf_statement_list.html', context=context)


def htmx_projects(request):
    form = DashboardFilter(request.GET)
    return HttpResponse(form["project"])


def CfBudgetView(request):
    return render(request, 'registers/cf_budget.html')


def PlanFactAnalysisView(request):
    return render(request, 'registers/plan_fact_analysis.html')
