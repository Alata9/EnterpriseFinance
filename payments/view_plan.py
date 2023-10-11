import csv
import datetime
from decimal import Decimal
from io import TextIOWrapper, StringIO, BytesIO

from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import DeleteView, FormView, ListView, UpdateView

from directory.models import Organization, Project, Currencies, Counterparties, PaymentAccount
from payments.forms import UploadFile, PaymentsPlanFilter, PaymentsPlanAdd, PaymentsPlanSeriesAdd, PaymentsAdd
from payments.models import PaymentsPlan, ExpensesItem, Payments
from registers.models import AccountSettings


class PaymentsPlanView(ListView):
    model = PaymentsPlan
    template_name = 'payments/payments_plan.html'

    def get(self, request, *args, **kwargs):
        if 'btn_to_file' in request.GET:
            return self.to_file(request)
        return super().get(request, *args, **kwargs)

    def to_file(self, request):
        my_data = [["Organization", "Date", "Amount", "Currency", "is_cash", "Counterparty", "Item", "Project", "Comments"]]
        payments = self.payments_queryset(request)
        for i in payments:
            if i.is_cash is False:
                i.is_cash = ''
            else:
                i.is_cash = 'cash'
            my_data.append([i.organization, i.date, i.amount, i.currency, i.is_cash, i.counterparty, i.item, i.project, i.comments])

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
        payments_pl = PaymentsPlan.objects.all()

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
                payments_pl = payments_pl.filter(account=form.cleaned_data['is_cash'])
            if form.cleaned_data['currency']:
                payments_pl = payments_pl.filter(currency=form.cleaned_data['currency'])
            if form.cleaned_data['ordering']:
                payments_pl = payments_pl.order_by(form.cleaned_data['ordering'])

        return payments_pl

    @staticmethod
    def htmx_list(request):
        context = {'object_list': PaymentsPlanView.payments_queryset(request)}

        return render(request, 'payments/payments_plan_list.html', context=context)


class PaymentsPlanIdView(UpdateView):
    model = PaymentsPlan
    template_name = 'payments/payments_plan_id.html'
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



    @staticmethod
    def htmx_projects(request):
        form = PaymentsPlanAdd(request.GET)
        return HttpResponse(form["project"])


class PaymentsPlanSeriesView(ListView):
    model = PaymentsPlan
    template_name = 'payments/payments_plan_series.html'
    form_class = PaymentsPlanSeriesAdd
    success_url = '/payments_plan'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        ctx['form'] = PaymentsPlanSeriesAdd()
        return ctx

    @staticmethod
    def htmx_projects(request):
        form = PaymentsPlanSeriesAdd(request.GET)
        return HttpResponse(form["project"])

    def series_queryset(request):
        payments_pl = PaymentsPlan.objects.all()
        form = PaymentsPlanSeriesAdd(request.POST)
        frequency_list = {'annually': 365, 'monthly': 30, 'weekly': 7, 'daily': 1}
        if form.is_valid():
            quentety = form.cleaned_data['quentety']
            frequency = form.cleaned_data['frequency']

            for i in range(quentety):
                date = form.cleaned_data['date']
                i = PaymentsPlan(
                    organization=form.cleaned_data['organization'],
                    counterparty=form.cleaned_data['counterparty'],
                    item=form.cleaned_data['item'],
                    project=form.cleaned_data['project'],
                    amount=form.cleaned_data['amount'],
                    currency=form.cleaned_data['currency'],
                    is_cash=form.cleaned_data['is_cash'],
                    date=date,
                )
                i.save()
                date += frequency_list.get(frequency)

            return super().form_valid(form)

        return payments_pl

    @staticmethod
    def htmx_list(request):
        context = {'object_list': PaymentsPlanSeriesView.series_queryset(request)}

        return render(request, 'payments/series_list.html', context=context)


class PaymentsPlanDeleteView(DeleteView):
    error = ''
    model = PaymentsPlan
    success_url = '/payments_plan'
    template_name = 'payments/payments_plan_delete.html'


class PaymentsPlanUploadFileView(FormView):
    form_class = UploadFile
    template_name = 'payments/payments_plan_upload_file.html'
    success_url = '/payments_plan'

    def form_valid(self, form):
        csvfile = form.cleaned_data['file']
        f = TextIOWrapper(csvfile.file)
        reader = csv.DictReader(f, delimiter=';')
        for _, item in enumerate(reader, start=1):
            payment_pl = PaymentsPlan()
            try:
                payment_pl.organization = Organization.objects.get(organization=item.get('organization'))
                payment_pl.is_cash = PaymentAccount.objects.get(is_cash=item.get('is_cash'))
                if item.get('project'):
                    payment_pl.project = Project.objects.get(project=item.get('project'))
                payment_pl.date = datetime.datetime.strptime(item.get('date'), '%d.%m.%Y').date()
                payment_pl.amount = Decimal(item.get('amount'))
                payment_pl.currency = Currencies.objects.get(code=item.get('currency'))
                payment_pl.counterparty = Counterparties.objects.get(counterparty=item.get('counterparty'))
                payment_pl.item = ExpensesItem.objects.get(expense_item=item.get('item'))
                payment_pl.comments = item.get('comments')
                payment_pl.save()
            except Exception as e:
                print(e)

        return super().form_valid(form)