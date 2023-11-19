import csv
import datetime
from decimal import Decimal
from io import TextIOWrapper, StringIO, BytesIO

from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, FormView, ListView, UpdateView
from directory.models import Organization, Project, Currencies, Counterparties, PaymentAccount, Items
from registers.models import AccountSettings
from payments.forms import UploadFile
from planning.models import Calculations, PaymentDocumentPlan

from planning.forms import (
    ReceiptsPlanFilter, ReceiptsPlanAdd,
    PaymentsPlanFilter, PaymentsPlanAdd,
    CalculationsFilter, CalculationAdd
)


class ReceiptsPlanView(ListView):
    model = PaymentDocumentPlan
    template_name = 'planning/receipts_plan.html'

    def get_queryset(self):
        return PaymentDocumentPlan.objects.filter(flow='Receipts')

    def get(self, request, *args, **kwargs):
        if 'btn_to_file' in request.GET:
            return self.to_file(request)
        return super().get(request, *args, **kwargs)

    def to_file(self, request):
        time_report = str(datetime.datetime.today().strftime('%d-%m-%Y, %H:%M:%S'))

        my_data = [[f'List of planned receipts from {time_report}'], [],
            ["Organization", "Date", "Amount", "Currency", "is_cash", "Counterparty", "Item", "Project", "Comments"]]
        payments = self.receipts_queryset(request)
        for i in payments:
            if i.is_cash is False:
                i.is_cash = ''
            else:
                i.is_cash = 'cash'
            my_data.append([i.organization, i.date, i.inflow_amount, i.currency, i.is_cash, i.counterparty, i.item, i.project,
                            i.comments])

        t = str(datetime.datetime.today().strftime('%d-%m-%Y-%H%M%S'))
        file_name = 'receipts_plan ' + t + '.csv'
        file_buffer = StringIO()

        writer = csv.writer(file_buffer, delimiter=';')
        writer.writerows(my_data)
        file_bytes = BytesIO(file_buffer.getvalue().encode('cp1251'))
        file_bytes.seek(0)

        response = FileResponse(file_bytes, filename=file_name, as_attachment=True)

        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        ctx['form'] = ReceiptsPlanFilter()
        return ctx

    @staticmethod
    def receipts_queryset(request):
        receipts_pl = PaymentDocumentPlan.objects.filter(flow='Receipts')

        form = ReceiptsPlanFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['date']:
                receipts_pl = receipts_pl.filter(date__gte=form.cleaned_data['date'])
            if form.cleaned_data['date_end']:
                receipts_pl = receipts_pl.filter(date__lte=form.cleaned_data['date_end'])
            if form.cleaned_data['counterparty']:
                receipts_pl = receipts_pl.filter(counterparty=form.cleaned_data['counterparty'])
            if form.cleaned_data['item']:
                receipts_pl = receipts_pl.filter(item=form.cleaned_data['item'])
            if form.cleaned_data['organization']:
                receipts_pl = receipts_pl.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['project']:
                receipts_pl = receipts_pl.filter(project=form.cleaned_data['project'])
            if form.cleaned_data['is_cash']:
                receipts_pl = receipts_pl.filter(is_cash=True)
            if form.cleaned_data['currency']:
                receipts_pl = receipts_pl.filter(currency=form.cleaned_data['currency'])
            if form.cleaned_data['ordering']:
                receipts_pl = receipts_pl.order_by(form.cleaned_data['ordering'])

        return receipts_pl

    @staticmethod
    def htmx_list(request):
        context = {'object_list': ReceiptsPlanView.receipts_queryset(request)}

        return render(request, 'planning/receipts_plan_list.html', context=context)


class ReceiptsPlanIdView(UpdateView):
    model = PaymentDocumentPlan
    template_name = 'planning/receipts_plan_id.html'
    form_class = ReceiptsPlanAdd
    success_url = '/receipts_plan'

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
        form = form.save(commit=False)
        form.flow = 'Receipts'
        try:
            form.save()
            return redirect('receipts_plan')
        except:
            form.add_error(None, 'Data save error')

    @staticmethod
    def htmx_projects(request):
        form = ReceiptsPlanAdd(request.GET)
        return HttpResponse(form["project"])


class ReceiptsPlanDeleteView(DeleteView):
    error = ''
    model = PaymentDocumentPlan
    success_url = '/receipts_plan'
    template_name = 'planning/receipts_plan_delete.html'


class ReceiptsPlanUploadFileView(FormView):
    form_class = UploadFile
    template_name = 'planning/receipts_plan_upload_file.html'
    success_url = '/receipts_plan'

    def form_valid(self, form):
        csvfile = form.cleaned_data['file']
        f = TextIOWrapper(csvfile.file)
        reader = csv.DictReader(f, delimiter=';')
        for _, item in enumerate(reader, start=1):
            receipts_pl = PaymentDocumentPlan()
            try:
                receipts_pl.organization = Organization.objects.get(organization=item.get('organization'))
                receipts_pl.is_cash = PaymentAccount.objects.get(is_cash=item.get('is_cash'))
                if item.get('project'):
                    receipts_pl.project = Project.objects.get(project=item.get('project'))
                receipts_pl.date = datetime.datetime.strptime(item.get('date'), '%d.%m.%Y').date()
                receipts_pl.amount = Decimal(item.get('amount'))
                receipts_pl.currency = Currencies.objects.get(code=item.get('currency'))
                receipts_pl.counterparty = Counterparties.objects.get(counterparty=item.get('counterparty'))
                receipts_pl.item = Items.objects.get(expense_item=item.get('item'))
                receipts_pl.comments = item.get('comments')
                receipts_pl.save()
            except Exception as e:
                print(e)

        return super().form_valid(form)


class PaymentsPlanView(ListView):
    model = PaymentDocumentPlan
    template_name = 'planning/payments_plan.html'

    def get_queryset(self):
        return PaymentDocumentPlan.objects.filter(flow='Payments')

    def get(self, request, *args, **kwargs):
        if 'btn_to_file' in request.GET:
            return self.to_file(request)
        return super().get(request, *args, **kwargs)

    def to_file(self, request):
        time_report = str(datetime.datetime.today().strftime('%d-%m-%Y, %H:%M:%S'))

        my_data = [[f'List of payment requests from {time_report}'], [],
            ["Organization", "Date", "Amount", "Currency", "is_cash", "Counterparty", "Item", "Project", "Comments"]]
        payments = self.payments_queryset(request)
        for i in payments:
            if i.is_cash is False:
                i.is_cash = ''
            else:
                i.is_cash = 'cash'
            my_data.append([i.organization, i.date, i.outflow_amount, i.currency, i.is_cash, i.counterparty, i.item, i.project,
                            i.comments])

        t = str(datetime.datetime.today().strftime('%d-%m-%Y-%H%M%S'))
        file_name = 'payments_plan' + t + '.csv'
        file_buffer = StringIO()

        writer = csv.writer(file_buffer, delimiter=';')
        writer.writerows(my_data)
        file_bytes = BytesIO(file_buffer.getvalue().encode('cp1251'))
        file_bytes.seek(0)

        response = FileResponse(file_bytes, filename=file_name, as_attachment=True)

        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        ctx['form'] = PaymentsPlanFilter()
        return ctx

    @staticmethod
    def payments_queryset(request):
        payments_pl = PaymentDocumentPlan.objects.filter(flow='Payments')

        form = PaymentsPlanFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['date']:
                payments_pl = payments_pl.filter(date__gte=form.cleaned_data['date'])
            if form.cleaned_data['date_end']:
                payments_pl = payments_pl.filter(date__lte=form.cleaned_data['date_end'])
            if form.cleaned_data['counterparty']:
                payments_pl = payments_pl.filter(counterparty=form.cleaned_data['counterparty'])
            if form.cleaned_data['item']:
                payments_pl = payments_pl.filter(item=form.cleaned_data['item'])
            if form.cleaned_data['organization']:
                payments_pl = payments_pl.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['project']:
                payments_pl = payments_pl.filter(project=form.cleaned_data['project'])
            if form.cleaned_data['is_cash']:
                payments_pl = payments_pl.filter(is_cash=True)
            if form.cleaned_data['currency']:
                payments_pl = payments_pl.filter(currency=form.cleaned_data['currency'])
            if form.cleaned_data['calculation']:
                payments_pl = payments_pl.filter(calculation=form.cleaned_data['calculation'])
            if form.cleaned_data['ordering']:
                payments_pl = payments_pl.order_by(form.cleaned_data['ordering'])

        return payments_pl

    @staticmethod
    def htmx_list(request):
        context = {'object_list': PaymentsPlanView.payments_queryset(request)}

        return render(request, 'planning/payments_plan_list.html', context=context)


class PaymentsPlanIdView(UpdateView):
    model = PaymentDocumentPlan
    template_name = 'planning/payments_plan_id.html'
    form_class = PaymentsPlanAdd
    success_url = '/payments_plan'

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
        form = form.save(commit=False)
        form.flow = 'Payments'
        try:
            form.save()
            return redirect('payments_plan')
        except:
            form.add_error(None, 'Data save error')

    @staticmethod
    def htmx_projects(request):
        form = PaymentsPlanAdd(request.GET)
        return HttpResponse(form["project"])


class PaymentsPlanDeleteView(DeleteView):
    error = ''
    model = PaymentDocumentPlan
    success_url = '/payments_plan'
    template_name = 'planning/payments_plan_delete.html'


class PaymentsPlanUploadFileView(FormView):
    form_class = UploadFile
    template_name = 'planning/payments_plan_upload_file.html'
    success_url = '/payments_plan'

    def form_valid(self, form):
        csvfile = form.cleaned_data['file']
        f = TextIOWrapper(csvfile.file)
        reader = csv.DictReader(f, delimiter=';')
        for _, item in enumerate(reader, start=1):
            payment_pl = PaymentDocumentPlan()
            try:
                payment_pl.organization = Organization.objects.get(organization=item.get('organization'))
                payment_pl.is_cash = PaymentAccount.objects.get(is_cash=item.get('is_cash'))
                if item.get('project'):
                    payment_pl.project = Project.objects.get(project=item.get('project'))
                payment_pl.date = datetime.datetime.strptime(item.get('date'), '%d.%m.%Y').date()
                payment_pl.amount = Decimal(item.get('amount'))
                payment_pl.currency = Currencies.objects.get(code=item.get('currency'))
                payment_pl.counterparty = Counterparties.objects.get(counterparty=item.get('counterparty'))
                payment_pl.item = Items.objects.get(expense_item=item.get('item'))
                payment_pl.comments = item.get('comments')
                payment_pl.save()
            except Exception as e:
                print(e)

        return super().form_valid(form)


class CalculationView(ListView):
    model = Calculations
    template_name = 'planning/calculations.html'
    success_url = '/calculations'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        ctx['form'] = CalculationsFilter()
        return ctx

    def regular_queryset(request):
        payments_pl = Calculations.objects.all()
        form = CalculationsFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['type_calc']:
                payments_pl = payments_pl.filter(type_calc=form.cleaned_data['type_calc'])
            if form.cleaned_data['flow']:
                payments_pl = payments_pl.filter(flow=form.cleaned_data['flow'])
            if form.cleaned_data['counterparty']:
                payments_pl = payments_pl.filter(counterparty=form.cleaned_data['counterparty'])
            if form.cleaned_data['item']:
                payments_pl = payments_pl.filter(item=form.cleaned_data['item'])
            if form.cleaned_data['is_cash']:
                payments_pl = payments_pl.filter(is_cash=True)
            if form.cleaned_data['organization']:
                payments_pl = payments_pl.filter(organization=form.cleaned_data['organization'])
            if form.cleaned_data['project']:
                payments_pl = payments_pl.filter(account=form.cleaned_data['project'])
            if form.cleaned_data['ordering']:
                payments_pl = payments_pl.order_by(form.cleaned_data['ordering'])

        return payments_pl

    @staticmethod
    def htmx_list(request):
        context = {'object_list': CalculationView.regular_queryset(request)}

        return render(request, 'payments/calculations_list.html', context=context)


class CalculationIdView(UpdateView):
    model = Calculations
    template_name = 'planning/calculation_id.html'
    form_class = CalculationAdd
    success_url = '/calculations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            context['object_list'] = self.calculation_queryset(self.kwargs['pk'])
        return context

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

        if 'from_pk' in self.kwargs:
            obj = self.model.objects.get(pk=self.kwargs['from_pk'])
            obj.id = None
            return obj

        if 'calc_pk' in self.kwargs:
            self.model.create_plan_payments(self.kwargs['calc_pk'])
            return redirect('/calculation_id')

        org = AccountSettings.load().organization()
        return self.model(organization=org)

    @staticmethod
    def htmx_projects(request):
        form = CalculationAdd(request.GET)
        return HttpResponse(form["project"])

    @staticmethod
    def calculation_queryset(calc_id):
        payments_pl = PaymentDocumentPlan.objects.all()
        payments_pl = payments_pl.filter(calculation_id=calc_id)

        return payments_pl

    @staticmethod
    def htmx_list(request):
        context = {'object_list': CalculationIdView.calculation_queryset(request)}

        return render(request, 'planning/payments_plan_list.html', context=context)


class CalculationDeleteView(DeleteView):
    error = ''
    model = Calculations
    success_url = '/calculations'
    template_name = 'payments/calculation_delete.html'


class CalculationPlanDeleteView(DeleteView):
    error = ''
    model = Calculations
    success_url = '/calculations'
    template_name = 'planning/calculation_plan_delete.html'