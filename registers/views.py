from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from directory.models import PaymentAccount
from payments.models import Payments
from receipts.models import Receipts
from registers.forms import AccountSettingsSet, AccountBalancesFilter
from registers.models import AccountSettings

class AccountSettingsView(UpdateView):
    model = AccountSettings
    template_name = 'registers/settings.html'
    form_class = AccountSettingsSet
    success_url = '/settings'

    def get_object(self):
        return self.model.load()



def HomeView(request):
    return render(request, 'registers/home.html')

def RatesView(request):
    return render(request, 'registers/rates.html')

def ReportsView(request):
    return render(request, 'registers/reports.html')

def DashboardView(request):
    return render(request, 'registers/dashboard.html')


def AccountBalancesView(request):

    if request.method == 'POST':
        form = AccountBalancesFilter(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('account_balances')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = AccountBalancesFilter()

    def payments_queryset(request):
        payments = Payments.objects.all()
        income = Receipts.objects.all()

        form = AccountBalancesFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['date']:
                payments = payments.filter(date__gte=form.cleaned_data['date'])
                income = income.filter(date__gte=form.cleaned_data['date'])
            if form.cleaned_data['date_end']:
                payments = payments.filter(date__lte=form.cleaned_data['date_end'])
                income = income.filter(date__lte=form.cleaned_data['date_end'])
            if form.cleaned_data['organization']:
                payments = payments.filter(organization=form.cleaned_data['organization'])
                income = income.filter(organization=form.cleaned_data['organization'])

            sum_payment = [i.aggregate(sum('amount')) for i in payments.account]
            sum_income = [i.aggregate(sum('amount')) for i in income.account]

        return payments_queryset

    context = {'form': form,
               'payments_queryset': payments_queryset}

    @staticmethod
    def htmx_list(request):
        context = {'object_list': AccountBalancesView.payments_queryset(request)}

        return render(request, 'payments/payments_list.html', context=context)

    return render(request, 'registers/account_balances.html', context=context)



def CfStatementView(request):
    return render(request, 'registers/cf_statement.html')

def CfBudgetView(request):
    return render(request, 'registers/cf_budget.html')

def PlanFactAnalysisView(request):
    return render(request, 'registers/plan_fact_analysis.html')






