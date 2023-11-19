import datetime
import requests
import lxml
from bs4 import BeautifulSoup as bs

from django.db.models import ProtectedError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, UpdateView, ListView
from registers.models import AccountSettings

from directory.forms import (
    OrganizationAdd, ProjectAdd, PaymentAccountAdd,
    CurrencyAdd, CurrenciesRatesAdd, RatesFilter, RatesParser,
    CounterpartyAdd, InitialDebtsAdd, InitialDebtsFilter, ItemAdd, ItemFilter, AnyItemAdd,
)
from directory.models import (
    Organization, Project, PaymentAccount,
    Currencies, CurrenciesRates,
    Counterparties, InitialDebts, Items,
)


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
                return redirect('/organizations')
            except:
                form_org.add_error(None, 'Data save error')
    else:
        form_org = OrganizationAdd()

    context = {'form_org': form_org}

    return render(request, 'directory/organizations.html', context=context)


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
                error=f'Error! The object cannot be deleted, it is included in the following entries:'
                      f'{error.protected_objects}'
            )
            return self.render_to_response(context)


# InitialDebts-------------------

class InitialDebtsView(ListView):
    model = InitialDebts
    template_name = 'directory/initial_debts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        ctx['form'] = InitialDebtsFilter()
        return ctx

    @staticmethod
    def debts_queryset(request):
        debts = InitialDebts.objects.all()

        form = InitialDebtsFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['organization']:
                debts = debts.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['counterparty']:
                debts = debts.filter(counterparty=form.cleaned_data['counterparty'])
            if form.cleaned_data['type_debt']:
                debts = debts.filter(type_debt=form.cleaned_data['type_debt'])

        return debts

    @staticmethod
    def htmx_list(request):
        context = {'object_list': InitialDebtsView.debts_queryset(request)}

        return render(request, 'directory/initial_debts_list.html', context=context)


class InitialDebtIdView(UpdateView):
    model = InitialDebts
    template_name = 'directory/initial_debt_id.html'
    form_class = InitialDebtsAdd
    success_url = '/initial_debts'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

    def form_valid(self, form):
        try:
            form.save()
            return redirect('initial_debts')
        except:
            form.add_error(None, 'Data save error')


class InitialDebtDeleteView(DeleteView):
    error = ''
    model = InitialDebts
    success_url = '/initial_debts'
    template_name = 'directory/initial_debt_delete.html'

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


# Rates----------------------------------

class RatesView(ListView):
    model = CurrenciesRates
    template_name = 'directory/rates.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        ctx['form'] = RatesFilter()
        return ctx

    @staticmethod
    def rates_queryset(request):
        rates = CurrenciesRates.objects.all()

        form = RatesFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['date']:
                rates = rates.filter(date__gte=form.cleaned_data['date'])
            if form.cleaned_data['date_end']:
                rates = rates.filter(date__lte=form.cleaned_data['date_end'])
            if form.cleaned_data['currency']:
                rates = rates.filter(currency=form.cleaned_data['currency'])
            if form.cleaned_data['accounting_currency']:
                rates = rates.filter(accounting_currency=form.cleaned_data['accounting_currency'])

        return rates

    @staticmethod
    def htmx_list(request):
        context = {'object_list': RatesView.rates_queryset(request)}

        return render(request, 'directory/rates_list.html', context=context)


class RatesIdView(UpdateView):
    model = CurrenciesRates
    template_name = 'directory/rate_id.html'
    form_class = CurrenciesRatesAdd

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

        if 'from_pk' in self.kwargs:
            obj = self.model.objects.get(pk=self.kwargs['from_pk'])
            obj.id = None
            return obj


        cur = AccountSettings.load().currency()
        return self.model(accounting_currency=cur)

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


class RatesParsingView(UpdateView):
    model = CurrenciesRates
    template_name = 'directory/rates_parsing.html'
    success_url = '/rates'
    form_class = RatesParser


    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

        cur = AccountSettings.load().currency()

        return self.model(accounting_currency=cur, date=datetime.datetime.today())


    def form_valid(self, form):
        if not form.cleaned_data['accounting_currency'] or not form.cleaned_data['currency']:
            return HttpResponse(status=400, reason="Both currencies should be specified")

        cur_1 = Currencies.objects.get(code=form.cleaned_data['accounting_currency'])
        cur_2 = Currencies.objects.get(code=form.cleaned_data['currency'])

        url = f'https://www.currency.me.uk/convert/{cur_1.code.lower()}/{cur_2.code.lower()}'

        r = requests.get(url)
        soup = bs(r.text, 'lxml')
        rate = soup.find('span', {'class': 'mini ccyrate'}).text
        parts = [x.strip() for x in rate.split('=')]
        parts1 = [x.strip() for x in parts[1].split()]
        cur_rate = float(parts1[0])

        cur = self.model.objects.filter(accounting_currency=cur_1, currency=cur_2, date=datetime.datetime.today())[:1]
        if not cur:
            cur = [
                self.model(
                    accounting_currency=cur_1,
                    currency=cur_2,
                    date=datetime.datetime.today(),
                )
            ]

        cur[0].rate = cur_rate
        cur[0].save()

        return HttpResponseRedirect(self.get_success_url())


class ItemsView(ListView):
    model = Items
    template_name = 'directory/items.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        ctx['form'] = ItemFilter()
        return ctx

    @staticmethod
    def items_queryset(request):
        items = Items.objects.all()

        form = ItemFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['group']:
                items = items.filter(group=form.cleaned_data['group'])
            if form.cleaned_data['flow']:
                items = items.filter(flow=form.cleaned_data['flow'])
            if form.cleaned_data['ordering']:
                items = items.order_by(form.cleaned_data['ordering'])

        return items

    @staticmethod
    def htmx_list(request):
        context = {'object_list': ItemsView.items_queryset(request)}

        return render(request, 'directory/items_list.html', context=context)


class ItemIdView(UpdateView):
    model = Items
    template_name = 'directory/item_id.html'
    form_class = AnyItemAdd
    success_url = '/items'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

    def form_valid(self, form):
        activities = {
            Items.ItemGroups[0][0]: 'operating',
            Items.ItemGroups[1][0]: 'operating',
            Items.ItemGroups[2][0]: 'operating',
            Items.ItemGroups[3][0]: 'operating',
            Items.ItemGroups[4][0]: 'operating',
            Items.ItemGroups[5][0]: 'operating',
            Items.ItemGroups[6][0]: 'financing',
            Items.ItemGroups[7][0]: 'investing',
            Items.ItemGroups[8][0]: 'investing',
        }

        form = form.save(commit=False)
        form.activity = activities.get(form.group)
        if form.system_field is False:
            form.item = form.item_user
        try:
            form.save()
            return redirect('items')
        except:
            form.add_error(None, 'Data save error')


class ItemDeleteView(DeleteView):
    error = ''
    model = Items
    success_url = '/items'
    template_name = 'directory/item_delete.html'

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


def ExpensesItemView(request):
    expense_items = Items.objects.filter(flow='Payments')
    context = {'expense_items': expense_items}


    return render(request, 'directory/expenses_items.html', context=context)


class ExpensesItemIdView(UpdateView):
    model = Items
    template_name = 'directory/expenses_item_id.html'
    form_class = ItemAdd
    success_url = '/expenses_items'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

    def form_valid(self, form):
        activities = {
            Items.ItemGroups[0][0]: 'operating',
            Items.ItemGroups[1][0]: 'operating',
            Items.ItemGroups[2][0]: 'operating',
            Items.ItemGroups[3][0]: 'operating',
            Items.ItemGroups[4][0]: 'operating',
            Items.ItemGroups[5][0]: 'operating',
            Items.ItemGroups[6][0]: 'financing',
            Items.ItemGroups[7][0]: 'investing',
            Items.ItemGroups[8][0]: 'investing',
        }

        form = form.save(commit=False)
        form.activity = activities.get(form.group)
        if form.system_field == False:
            form.item = form.item_user
        form.flow = 'Payments'
        try:
            form.save()
            return redirect('expenses_items')
        except:
            form.add_error(None, 'Data save error')


class ExpensesItemDeleteView(DeleteView):
    error = ''
    model = Items
    success_url = '/expenses_items'
    template_name = 'directory/expenses_item_delete.html'

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


def IncomeItemView(request):
    income_items = Items.objects.filter(flow='Receipts')
    context = {'income_items': income_items}

    return render(request, 'directory/income_items.html', context=context)


class IncomeItemIdView(UpdateView):
    model = Items
    template_name = 'directory/income_item_id.html'
    form_class = ItemAdd
    success_url = 'income_items'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

    def form_valid(self, form):
        activities = {
            Items.ItemGroups[0][0]: 'operating',
            Items.ItemGroups[1][0]: 'operating',
            Items.ItemGroups[2][0]: 'operating',
            Items.ItemGroups[3][0]: 'operating',
            Items.ItemGroups[4][0]: 'operating',
            Items.ItemGroups[5][0]: 'operating',
            Items.ItemGroups[6][0]: 'financing',
            Items.ItemGroups[7][0]: 'investing',
            Items.ItemGroups[8][0]: 'investing',
        }

        form = form.save(commit=False)
        form.activity = activities.get(form.group)
        if form.system_field == False:
            form.item = form.item_user
        form.flow = 'Receipts'
        try:
            form.save()
            return redirect('income_items')
        except:
            form.add_error(None, 'Data save error')


class IncomeItemDeleteView(DeleteView):
    error = ''
    model = Items
    success_url = '/income_items'
    template_name = 'directory/income_item_delete.html'

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

