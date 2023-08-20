from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.views.generic import DeleteView

from directory.forms import CounterpartyAdd, OrganizationAdd, CurrencyAdd, ProjectAdd, PaymentAccountAdd
from directory.models import Counterparties, Organization, Project, PaymentAccount, Currencies


# Counterparties-------------------

def CounterpartiesView(request):
    counterparties = Counterparties.objects.all()
    context = {'counterparties': counterparties}
    return render(request, 'directory/counterparties.html', context=context)


def CounterpartyIdView(request):
    if request.method == 'POST':
        form = CounterpartyAdd(request.POST)
        if form.is_valid():
            try:
                c = form.save(commit=False)
                type_counterparty = [c.suppliers, c.customer, c.employee, c.other]
                if any(type_counterparty):
                    c.save()
                    return redirect('counterparties')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = CounterpartyAdd()

    context = {'form': form}

    return render(request, 'directory/counterparty_id.html', context=context)


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


def OrganizationIdView(request):
    projects = Project.objects.all()
    accounts = PaymentAccount.objects.all()

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

    # org = ''
    # project = project.filter(organization=org)
    # accounts = accounts.filter(organization=org)

    context = {'form_org': form_org,
               'projects': projects,
               'accounts': accounts}

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


def CurrenciesIdView(request):
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

    context = {'form': form}

    return render(request, 'directory/currency_id.html', context=context)


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


def ProjectsIdView(request):
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

    context = {'form': form}

    return render(request, 'directory/projects_id.html', context=context)


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


def PaymentAccountIdView(request):
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

    context = {'form': form}

    return render(request, 'directory/payment_account_id.html', context=context)


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
