from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, UpdateView

from directory.forms import CounterpartyAdd, OrganizationAdd, CurrencyAdd, ProjectAdd, PaymentAccountAdd, \
    CurrenciesRatesAdd
from directory.models import Counterparties, Organization, Project, PaymentAccount, Currencies, CurrenciesRates


# Counterparties-------------------

def CounterpartiesView(request):
    counterparties = Counterparties.objects.all()
    context = {'counterparties': counterparties}
    return render(request, 'directory/counterparties.html', context=context)

class CounterpartyIdView(UpdateView):
    model = Counterparties
    template_name = 'directory/counterparty_id.html'
    form_class = CounterpartyAdd
    success_url = '/counterparties'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)


class CounterpartyDeleteView(DeleteView):
    error = ''
    model = Counterparties
    success_url = '/counterparties'
    template_name = 'directory/counterparty_delete.html'

    def post(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as error:
            self.object = self.get_object()
            context = self.get_context_data(
                object=self.object,
                error=f'Error: {error.protected_objects}'
            )
            return self.render_to_response(context)


# Organizations-------------------------

def OrganizationsView(request):
    organizations = Organization.objects.all()
    context = {'organizations': organizations}

    return render(request, 'directory/organizations.html', context=context)



def OrganizationAddView(request):
    if request.method == 'POST':
        form_org = OrganizationAdd(request.POST)
        if form_org.is_valid():
            try:
                form_org.save()
                return redirect('organizations')
            except:
                form_org.add_error(None, 'Data save error')
    else:
        form_org = OrganizationAdd()

    context = {'form_org': form_org}

    return render(request, 'directory/organization_add.html', context=context)


def OrganizationIdView(request):
    if request.method == 'POST':
        form_org = OrganizationAdd(request.POST)
        if form_org.is_valid():
            try:
                form_org.save()
                return redirect('organizations')
            except:
                form_org.add_error(None, 'Data save error')
    else:
        form_org = OrganizationAdd()

    context = {'form_org': form_org}

    return render(request, 'directory/organization_id.html', context=context)


class OrganizationDeleteView(DeleteView):
    error = ''
    model = Organization
    success_url = '/organizations'
    template_name = 'directory/organization_delete.html'

    def post(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as error:
            self.object = self.get_object()
            context = self.get_context_data(
                object=self.object,
                error=f'Error: {error.protected_objects}'
            )
            return self.render_to_response(context)


# Currencies-----------------------

def CurrenciesView(request):
    currencies = Currencies.objects.all()
    context = {'currencies': currencies}

    return render(request, 'directory/currencies.html', context=context)


class CurrenciesIdView(UpdateView):
    model = Currencies
    template_name = 'directory/currency_id.html'
    form_class = CurrencyAdd

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

    def form_valid(self, form):
        try:
            form.save()
            return redirect('currencies')
        except:
            form.add_error(None, 'Data save error')


class CurrencyDeleteView(DeleteView):
    error = ''
    model = Currencies
    success_url = '/currencies'
    template_name = 'directory/currency_delete.html'

    def post(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as error:
            self.object = self.get_object()
            context = self.get_context_data(
                object=self.object,
                error=f'Error: {error.protected_objects}'
            )
            return self.render_to_response(context)


# Projects-------------------------------------------

def ProjectsView(request):
    projects = Project.objects.all()
    context = {'projects': projects}

    return render(request, 'directory/projects.html', context=context)


class ProjectsIdView(UpdateView):
    model = Project
    template_name = 'directory/project_id.html'
    form_class = ProjectAdd

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

    def form_valid(self, form):
        try:
            form.save()
            return redirect('projects')
        except:
            form.add_error(None, 'Data save error')


class ProjectDeleteView(DeleteView):
    error = ''
    model = Project
    success_url = '/projects'
    template_name = 'directory/project_delete.html'

    def post(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as error:
            self.object = self.get_object()
            context = self.get_context_data(
                object=self.object,
                error=f'Error: {error.protected_objects}'
            )
            return self.render_to_response(context)


# Payment_accounts----------------------------------

def PaymentAccountsView(request):
    accounts = PaymentAccount.objects.all()
    context = {'accounts': accounts}

    return render(request, 'directory/payment_accounts.html', context=context)

class PaymentAccountIdView(UpdateView):
    model = PaymentAccount
    template_name = 'directory/payment_account_id.html'
    form_class = PaymentAccountAdd

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

    def form_valid(self, form):
        try:
            form.save()
            return redirect('payment_accounts')
        except:
            form.add_error(None, 'Data save error')


class PaymentAccountDeleteView(DeleteView):
    error = ''
    model = PaymentAccount
    success_url = '/payment_accounts'
    template_name = 'directory/payment_account_delete.html'

    def post(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as error:
            self.object = self.get_object()
            context = self.get_context_data(
                object=self.object,
                error=f'Error: {error.protected_objects}'
            )
            return self.render_to_response(context)


def RatesView(request):
    rates = CurrenciesRates.objects.all()
    context = {'rates': rates}

    return render(request, 'directory/rates.html', context=context)


class RatesIdView(UpdateView):
    model = CurrenciesRates
    template_name = 'directory/rate_id.html'
    form_class = CurrenciesRatesAdd

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

    def form_valid(self, form):
        try:
            form.save()
            return redirect('rates')
        except:
            form.add_error(None, 'Data save error')


class RatesDeleteView(DeleteView):
    error = ''
    model = CurrenciesRates
    success_url = '/rates'
    template_name = 'directory/rate_delete.html'

    def post(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as error:
            self.object = self.get_object()
            context = self.get_context_data(
                object=self.object,
                error=f'Error: {error.protected_objects}'
            )
            return self.render_to_response(context)