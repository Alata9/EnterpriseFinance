import csv
import datetime
from decimal import Decimal
from io import TextIOWrapper, BytesIO, StringIO

from django.db.models import ProtectedError
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView, ListView, FormView

from directory.models import Organization, Project, Currencies, Counterparties, PaymentAccount
from payments.forms import ExpenseGroupAdd, ExpenseItemAdd, PaymentsFilter, PaymentsAdd, UploadFile
from payments.models import ExpenseGroup, ExpensesItem, Payments
from registers.models import AccountSettings


# Expenses Groups----------------------------------------

def ExpensesGroupView(request):
    expense_groups = ExpenseGroup.objects.all()
    context = {'expense_groups': expense_groups}

    return render(request, 'payments/expenses_groups.html', context=context)

class ExpensesGroupIdView(UpdateView):
    model = ExpenseGroup
    template_name = 'payments/expenses_group_id.html'
    form_class = ExpenseGroupAdd
    success_url = '/expenses_groups'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)


class ExpensesGroupDeleteView(DeleteView):
    error = ''
    model = ExpenseGroup
    success_url = '/expenses_groups'
    template_name = 'payments/expenses_group_delete.html'

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

# Expenses Item----------------------------------------

def ExpensesItemView(request):
    expense_items = ExpensesItem.objects.all()
    context = {'expense_items': expense_items}


    return render(request, 'payments/expenses_items.html', context=context)


class ExpensesItemIdView(UpdateView):
    model = ExpensesItem
    template_name = 'payments/expenses_item_id.html'
    form_class = ExpenseItemAdd
    success_url = '/expenses_items'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)


class ExpensesItemDeleteView(DeleteView):
    error = ''
    model = ExpensesItem
    success_url = '/expenses_items'
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


# Payments-----------------------------------

class PaymentsView(ListView):
    model = Payments
    template_name = 'payments/payments.html'

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
        file_name = 'payments' + t + '.csv'
        file_buffer = StringIO()

        writer = csv.writer(file_buffer, delimiter=';')
        writer.writerows(my_data)
        file_bytes = BytesIO(file_buffer.getvalue().encode('cp1251'))
        file_bytes.seek(0)

        response = FileResponse(file_bytes, filename=file_name, as_attachment=True)

        return response


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
            if form.cleaned_data['ordering']:
                payments = payments.order_by(form.cleaned_data['ordering'])

        return payments

    @staticmethod
    def htmx_list(request):
        context = {'object_list': PaymentsView.payments_queryset(request)}

        return render(request, 'payments/payments_list.html', context=context)


class PaymentsIdView(UpdateView):
    model = Payments
    template_name = 'payments/payments_id.html'
    form_class = PaymentsAdd
    success_url = '/payments'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

        if 'from_pk' in self.kwargs:
            obj = self.model.objects.get(pk=self.kwargs['from_pk'])
            obj.id = None
            return obj

        org = AccountSettings.load().organization()
        return self.model(organization=org)


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




def PaymentsPlanView(request):
    return render(request, 'payments/payments_plan.html')


class UploadFileView(FormView):
    form_class = UploadFile
    template_name = 'payments/payments_upload_file.html'
    success_url = '/payments'

    def form_valid(self, form):
        csvfile = form.cleaned_data['file']
        f = TextIOWrapper(csvfile.file)
        reader = csv.DictReader(f, delimiter=';')
        for _, item in enumerate(reader, start=1):
            payment = Payments()
            try:
                payment.organization = Organization.objects.get(organization=item.get('organization'))
                payment.account = PaymentAccount.objects.get(account=item.get('account'))
                if item.get('project'):
                    payment.project = Project.objects.get(project=item.get('project'))
                payment.date = datetime.datetime.strptime(item.get('date'), '%d.%m.%Y').date()
                payment.amount = Decimal(item.get('amount'))
                payment.currency = Currencies.objects.get(code=item.get('currency'))
                payment.counterparty = Counterparties.objects.get(counterparty=item.get('counterparty'))
                payment.item = ExpensesItem.objects.get(expense_item=item.get('item'))
                payment.comments = item.get('comments')
                payment.save()
            except Exception as e:
                print(e)

        return super().form_valid(form)