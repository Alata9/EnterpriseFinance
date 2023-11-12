import csv
import datetime
from decimal import Decimal
from io import TextIOWrapper, StringIO, BytesIO

from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView, ListView, FormView

from directory.models import (Organization, PaymentAccount, Currencies, Counterparties, Project, Items,
    # IncomeItem, ExpensesItem
                              )
from registers.models import AccountSettings
from payments.models import ( ChangePayAccount, PaymentDocuments,
                             # Receipts, Payments,
                             )
from payments.forms import (
    ReceiptsAdd, ReceiptsFilter, PaymentsFilter, PaymentsAdd,
    ChangePayAccountAdd, ChangePayAccountFilter, UploadFile
)


class ReceiptsView(ListView):
    model = PaymentDocuments
    template_name = 'payments/receipts.html'

    def get_queryset(self):
        return PaymentDocuments.objects.filter(flow='Receipts')

    def get(self, request, *args, **kwargs):
        if 'btn_to_file' in request.GET:
            return self.to_file(request)
        return super().get(request, *args, **kwargs)

    def to_file(self, request):
        my_data = [["Organization", "Account", "Date", "Amount", "Currency", "Counterparty", "Item", "Project", "Comments"]]
        receipts = self.receipts_queryset(request)
        for i in receipts:
            my_data.append([i.organization, i.account, i.date, i.inflow_amount, i.currency, i.counterparty,
                            i.item, i.project, i.comments])

        t = str(datetime.datetime.today().strftime('%d-%m-%Y-%H%M%S'))
        file_name = 'receipts_' + t + '.csv'
        file_buffer = StringIO()

        writer = csv.writer(file_buffer, delimiter=';')
        writer.writerows(my_data)
        file_bytes = BytesIO(file_buffer.getvalue().encode('cp1251'))
        file_bytes.seek(0)

        response = FileResponse(file_bytes, filename=file_name, as_attachment=True)

        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        ctx['form'] = ReceiptsFilter()
        return ctx

    @staticmethod
    def receipts_queryset(request):
        receipts = PaymentDocuments.objects.filter(flow='Receipts')
        print(receipts)
        form = ReceiptsFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['date']:
                receipts = receipts.filter(date__gte=form.cleaned_data['date'])
            if form.cleaned_data['date_end']:
                receipts = receipts.filter(date__lte=form.cleaned_data['date_end'])
            if form.cleaned_data['counterparty']:
                receipts = receipts.filter(counterparty=form.cleaned_data['counterparty'])
            if form.cleaned_data['item']:
                receipts = receipts.filter(item=form.cleaned_data['item'])
            if form.cleaned_data['organization']:
                receipts = receipts.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['project']:
                receipts = receipts.filter(project=form.cleaned_data['project'])
            if form.cleaned_data['account']:
                receipts = receipts.filter(account=form.cleaned_data['account'])
            if form.cleaned_data['ordering']:
                receipts = receipts.order_by(form.cleaned_data['ordering'])

        return receipts

    @staticmethod
    def htmx_list(request):
        context = {'object_list': ReceiptsView.receipts_queryset(request)}

        return render(request, 'payments/receipts_list.html', context=context)


class ReceiptsIdView(UpdateView):
    model = PaymentDocuments
    template_name = 'payments/receipts_id.html'
    form_class = ReceiptsAdd
    success_url = '/receipts'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

        if 'from_pk' in self.kwargs:
            obj = self.model.objects.get(pk=self.kwargs['from_pk'])
            obj.id = None
            return obj

        if 'plan_id' in self.kwargs:
            return self.model.from_plan(self.kwargs['plan_id'])

        org = AccountSettings.load().organization()
        return self.model(organization=org)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.flow = 'Receipts'
        try:
            form.save()
            return redirect('receipts')
        except:
            form.add_error(None, 'Data save error')

    @staticmethod
    def htmx_accounts(request):
        form = ReceiptsAdd(request.GET)
        return HttpResponse(form["account"])

    @staticmethod
    def htmx_projects(request):
        form = ReceiptsAdd(request.GET)
        return HttpResponse(form["project"])


class ReceiptsDeleteView(DeleteView):
    error = ''
    model = PaymentDocuments
    success_url = '/payments'
    template_name = 'payments/receipts_delete.html'


class UploadFileReceiptView(FormView):
    form_class = UploadFile
    template_name = 'payments/receipts_upload_file.html'
    success_url = '/payments'

    def form_valid(self, form):
        csvfile = form.cleaned_data['file']
        f = TextIOWrapper(csvfile.file)
        reader = csv.DictReader(f, delimiter=';')
        for _, item in enumerate(reader, start=1):
            receipt = PaymentDocuments()
            try:
                receipt.organization = Organization.objects.get(organization=item.get('organization'))
                receipt.account = PaymentAccount.objects.get(account=item.get('account'))
                if item.get('project'):
                    receipt.project = Project.objects.get(project=item.get('project'))
                receipt.date = datetime.datetime.strptime(item.get('date'), '%d.%m.%Y').date()
                receipt.amount = Decimal(item.get('inflow_amount'))
                receipt.currency = Currencies.objects.get(code=item.get('currency'))
                receipt.counterparty = Counterparties.objects.get(counterparty=item.get('counterparty'))
                receipt.item = Items.objects.get(income_item=item.get('item'))
                receipt.comments = item.get('comments')
                receipt.save()
            except Exception as e:
                print(e)

        return super().form_valid(form)


class PaymentsView(ListView):
    model = PaymentDocuments
    template_name = 'payments/payments.html'

    def get_queryset(self):
        return PaymentDocuments.objects.filter(flow='Payments')

    def get(self, request, *args, **kwargs):
        if 'btn_to_file' in request.GET:
            return self.to_file(request)
        return super().get(request, *args, **kwargs)

    def to_file(self, request):
        my_data = [
            ["Organization", "Account", "Date", "Amount", "Currency", "Counterparty", "Item", "Project", "Comments"]]
        payments = self.payments_queryset(request)
        for i in payments:
            my_data.append([i.organization, i.account, i.date, i.outflow_amount, i.currency, i.counterparty, i.item, i.project,
                            i.comments])

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
        payments = PaymentDocuments.objects.filter(flow='Payments')

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
    model = PaymentDocuments
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

        if 'plan_id' in self.kwargs:
            return self.model.from_plan(self.kwargs['plan_id'])

        org = AccountSettings.load().organization()
        return self.model(organization=org)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.flow = 'Payments'
        try:
            form.save()
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
    model = PaymentDocuments
    success_url = '/payments'
    template_name = 'payments/payments_delete.html'


class UploadFilePaymentView(FormView):
    form_class = UploadFile
    template_name = 'payments/payments_upload_file.html'
    success_url = '/payments'

    def form_valid(self, form):
        csvfile = form.cleaned_data['file']
        f = TextIOWrapper(csvfile.file)
        reader = csv.DictReader(f, delimiter=';')
        for _, item in enumerate(reader, start=1):
            payment = PaymentDocuments()
            try:
                payment.organization = Organization.objects.get(organization=item.get('organization'))
                payment.account = PaymentAccount.objects.get(account=item.get('account'))
                if item.get('project'):
                    payment.project = Project.objects.get(project=item.get('project'))
                payment.date = datetime.datetime.strptime(item.get('date'), '%d.%m.%Y').date()
                payment.amount = Decimal(item.get('outflow_amount'))
                payment.currency = Currencies.objects.get(code=item.get('currency'))
                payment.counterparty = Counterparties.objects.get(counterparty=item.get('counterparty'))
                payment.item = Items.objects.get(expense_item=item.get('item'))
                payment.comments = item.get('comments')
                payment.save()
            except Exception as e:
                print(e)

        return super().form_valid(form)


class ChangePayAccountView(ListView):
    model = ChangePayAccount
    template_name = 'payments/change_payaccounts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        ctx['form'] = ChangePayAccountFilter()
        return ctx

    @staticmethod
    def changes_queryset(request):
        changes = ChangePayAccount.objects.all()

        form = ChangePayAccountFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['date']:
                changes = changes.filter(date__gte=form.cleaned_data['date'])
            if form.cleaned_data['date_end']:
                changes = changes.filter(date__lte=form.cleaned_data['date_end'])
            if form.cleaned_data['pay_account_from']:
                changes = changes.filter(pay_account_from=form.cleaned_data['pay_account_from'])
            if form.cleaned_data['pay_account_to']:
                changes = changes.filter(pay_account_to=form.cleaned_data['pay_account_to'])

        return changes

    @staticmethod
    def htmx_list(request):
        context = {'object_list': ChangePayAccountView.changes_queryset(request)}

        return render(request, 'payments/change_payaccount_list.html', context=context)


class ChangePayAccountIdView(UpdateView):                       #  edit - auto-add currency by account
    template_name = 'payments/change_payaccount_id.html'
    form_class = ChangePayAccountAdd
    success_url = '/change_payaccounts'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

        if 'from_pk' in self.kwargs:
            obj = self.model.objects.get(pk=self.kwargs['from_pk'])
            obj.id = None
            return obj


class ChangePayAccountDeleteView(DeleteView):
    error = ''
    model = ChangePayAccount
    success_url = '/change_payaccounts'
    template_name = 'payments/change_payaccount_delete.html'

