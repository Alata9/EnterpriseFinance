from django.shortcuts import render, redirect

from directory.forms import *
from directory.models import *


def CounterpartiesView(request):
    counterparties = Сounterparties.objects.all()

    if request.method == 'POST':
        form = CounterpartyAdd(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('counterparties')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = CounterpartyAdd()

    context = {'form': form,
               'counterparties': counterparties}

    return render(request, 'directory/counterparties.html', context=context)


def OrganizationsView(request):
    organizations = Organization.objects.all()

    if request.method == 'POST':
        form = OrganizationAdd(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('organizations')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = OrganizationAdd()

    context = {'form': form,
               'organizations': organizations}

    return render(request, 'directory/organizations.html', context=context)


def CurrenciesView(request):
    currencies = Currenсies.objects.all()

    if request.method == 'POST':
        form = CurrencyAdd(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('currencies')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = CurrencyAdd()

    context = {'form': form,
               'currencies': currencies}

    return render(request, 'directory/currencies.html', context=context)


def ProjectsView(request):
    projects = Project.objects.all()

    if request.method == 'POST':
        form = ProjectAdd(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('projects')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = ProjectAdd()

    context = {'form': form,
               'projects': projects}

    return render(request, 'directory/projects.html', context=context)


def PaymentAccountsView(request):
    accounts = Payment_account.objects.all()

    if request.method == 'POST':
        form = PaymentAccountAdd(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('payment_accounts')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = PaymentAccountAdd()

    context = {'form': form,
               'accounts': accounts}

    return render(request, 'directory/payment_accounts.html', context=context)