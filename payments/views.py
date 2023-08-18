import csv
import datetime

from django.db.models import ProtectedError
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView, ListView

from payments.forms import ExpenseGroupAdd, ExpenseItemAdd, PaymentsFilter, PaymentsAdd
from payments.models import ExpenseGroup, ExpensesItem, Payments
from registers.models import AccountSettings


def ExpensesGroupView(request):
    expense_groups = ExpenseGroup.objects.all()

    if request.method == 'POST':
        form = ExpenseGroupAdd(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('expenses_group')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = ExpenseGroupAdd()

    context = {'form': form,
               'expense_groups': expense_groups}

    return render(request, 'payments/expenses_group.html', context=context)


def ExpensesItemView(request):
    expense_items = ExpensesItem.objects.all()

    if request.method == 'POST':
        form = ExpenseItemAdd(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('expenses_item')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = ExpenseItemAdd()

    context = {'form': form,
               'expense_items': expense_items}

    return render(request, 'payments/expenses_item.html', context=context)

# -----------------------------------

class PaymentsView(ListView):
    model = Payments
    template_name = 'payments/payments.html'
    #-------------

    def get(self, request, *args, **kwargs):
        if 'btn_to_file' in request.GET:
            return self.to_file(request)
        return super().get(request, *args, **kwargs)

    def to_file(self, request):
        my_data = [["Organization", "Account", "Date", "Amount", "Currency", "Counterparty", "Item", "Project", "Comments"]]
        payments = self.payments_queryset(request)
        for i in payments:
            my_data.append([i.organization, i.account, i.date, i.amount, i.currency, i.counterparty, i.item, i.project, i.comments])

        t = str(datetime.datetime.today().strftime('%d-%m-%Y-%H%M%S'))
        name_file = 'payments' + t + '.csv'
        my_file = open(name_file, 'w',  newline='')
        with my_file:
            writer = csv.writer(my_file)
            writer.writerows(my_data)

        f = open(name_file, 'rb')

        return FileResponse(f)
    #-------------

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        ctx['form'] = PaymentsFilter()
        return ctx

    @staticmethod
    def payments_queryset(request):
        payments = Payments.objects.all()

        form = PaymentsFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['date']:
                payments = payments.filter(date__gte=form.cleaned_data['date'])
            if form.cleaned_data['date_end']:
                payments = payments.filter(date__lte=form.cleaned_data['date_end'])
            if form.cleaned_data['counterparty']:
                payments = payments.filter(counterparty=form.cleaned_data['counterparty'])
            if form.cleaned_data['item']:
                payments = payments.filter(item=form.cleaned_data['item'])
            if form.cleaned_data['organization']:
                payments = payments.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['project']:
                payments = payments.filter(project=form.cleaned_data['project'])
            if form.cleaned_data['account']:
                payments = payments.filter(account=form.cleaned_data['account'])

        return payments

    @staticmethod
    def htmx_list(request):
        context = {'object_list': PaymentsView.payments_queryset(request)}

        return render(request, 'payments/payments_list.html', context=context)


class PaymentsIdView(UpdateView):
    model = Payments
    template_name = 'payments/payments_id.html'
    form_class = PaymentsAdd

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

        if 'from_pk' in self.kwargs:
            obj = self.model.objects.get(pk=self.kwargs['from_pk'])
            obj.id = None
            return obj

        org = AccountSettings.load().organization()
        return self.model(organization=org)

    def form_valid(self, form):
        try:
            payment = form.save(commit=False)
            payment.currency = payment.account.currency
            payment.save()
            return redirect('payments')
        except:
            form.add_error(None, 'Data save error')

    @staticmethod
    def htmx_accounts(request):
        form = PaymentsAdd(request.GET)
        return HttpResponse(form["account"])

    @staticmethod
    def htmx_projects(request):
        form = PaymentsAdd(request.GET)
        return HttpResponse(form["project"])


class PaymentsDeleteView(DeleteView):
    error = ''
    model = Payments
    success_url = '/payments'
    template_name = 'payments/payments_delete.html'


class ExpensesItemDeleteView(DeleteView):
    error = ''
    model = ExpensesItem
    success_url = '/expenses_item'
    template_name = 'payments/expenses_item_delete.html'

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


def PaymentsPlanView(request):
    return render(request, 'payments/payments_plan.html')
