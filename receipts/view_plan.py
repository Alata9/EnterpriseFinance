import csv
import datetime
from decimal import Decimal
from io import TextIOWrapper, StringIO, BytesIO

from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import DeleteView, FormView, ListView, UpdateView

from directory.models import Organization, Project, Currencies, Counterparties, PaymentAccount
from receipts.forms import ReceiptsPlanAdd, ReceiptsPlanFilter, UploadFile
from receipts.models import ReceiptsPlan, IncomeItem
from registers.models import AccountSettings


class ReceiptsPlanView(ListView):
    model = ReceiptsPlan
    template_name = 'receipts/receipts_plan.html'

    def get(self, request, *args, **kwargs):
        if 'btn_to_file' in request.GET:
            return self.to_file(request)
        return super().get(request, *args, **kwargs)

    def to_file(self, request):
        my_data = [["Organization", "Date", "Amount", "Currency", "is_cash", "Counterparty", "Item", "Project", "Comments"]]
        payments = self.receipts_queryset(request)
        for i in payments:
            if i.is_cash is False:
                i.is_cash = ''
            else:
                i.is_cash = 'cash'
            my_data.append([i.organization, i.date, i.amount, i.currency, i.is_cash, i.counterparty, i.item, i.project, i.comments])

        t = str(datetime.datetime.today().strftime('%d-%m-%Y-%H%M%S'))
        file_name = 'receipts_plan' + t + '.csv'
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
        receipts_pl = ReceiptsPlan.objects.all()

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

        return render(request, 'receipts/receipts_plan_list.html', context=context)


class ReceiptsPlanIdView(UpdateView):
    model = ReceiptsPlan
    template_name = 'receipts/receipts_plan_id.html'
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

    @staticmethod
    def htmx_projects(request):
        form = ReceiptsPlanAdd(request.GET)
        return HttpResponse(form["project"])


class ReceiptsPlanDeleteView(DeleteView):
    error = ''
    model = ReceiptsPlan
    success_url = '/receipts_plan'
    template_name = 'receipts/receipts_plan_delete.html'


class ReceiptsPlanUploadFileView(FormView):
    form_class = UploadFile
    template_name = 'receipts/receipts_plan_upload_file.html'
    success_url = '/receipts_plan'

    def form_valid(self, form):
        csvfile = form.cleaned_data['file']
        f = TextIOWrapper(csvfile.file)
        reader = csv.DictReader(f, delimiter=';')
        for _, item in enumerate(reader, start=1):
            receipts_pl = ReceiptsPlan()
            try:
                receipts_pl.organization = Organization.objects.get(organization=item.get('organization'))
                receipts_pl.is_cash = PaymentAccount.objects.get(is_cash=item.get('is_cash'))
                if item.get('project'):
                    receipts_pl.project = Project.objects.get(project=item.get('project'))
                receipts_pl.date = datetime.datetime.strptime(item.get('date'), '%d.%m.%Y').date()
                receipts_pl.amount = Decimal(item.get('amount'))
                receipts_pl.currency = Currencies.objects.get(code=item.get('currency'))
                receipts_pl.counterparty = Counterparties.objects.get(counterparty=item.get('counterparty'))
                receipts_pl.item = IncomeItem.objects.get(expense_item=item.get('item'))
                receipts_pl.comments = item.get('comments')
                receipts_pl.save()
            except Exception as e:
                print(e)

        return super().form_valid(form)