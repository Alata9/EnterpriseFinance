import datetime
from decimal import Decimal
from io import TextIOWrapper, StringIO, BytesIO

from django.db.models import ProtectedError
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView, DeleteView, ListView, FormView

from directory.models import Organization, PaymentAccount, Currencies, Counterparties, Project
from receipts.forms import IncomeGroupAdd, IncomeItemAdd, ReceiptsFilter, ReceiptsAdd, UploadFile
from receipts.models import IncomeGroup, IncomeItem, Receipts
from registers.models import AccountSettings

import csv

def IncomeGroupView(request):
    income_groups = IncomeGroup.objects.all()
    context = {'income_groups': income_groups}

    return render(request, 'receipts/income_groups.html', context=context)


class IncomeGroupIdView(UpdateView):
    model = IncomeGroup
    template_name = 'receipts/income_group_id.html'
    form_class = IncomeGroupAdd

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

    def form_valid(self, form):
        try:
            form.save()
            return redirect('income_groups')
        except:
            form.add_error(None, 'Data save error')


class IncomeGroupDeleteView(DeleteView):
    error = ''
    model = IncomeGroup
    success_url = '/income_groups'
    template_name = 'receipts/income_group_delete.html'

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
    income_items = IncomeItem.objects.all()
    context = {'income_items': income_items}

    return render(request, 'receipts/income_items.html', context=context)


class IncomeItemIdView(UpdateView):
    model = IncomeItem
    template_name = 'receipts/income_item_id.html'
    form_class = IncomeItemAdd

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)

    def form_valid(self, form):
        try:
            form.save()
            return redirect('income_items')
        except:
            form.add_error(None, 'Data save error')


class IncomeItemDeleteView(DeleteView):
    error = ''
    model = IncomeItem
    success_url = '/income_items'
    template_name = 'receipts/income_item_delete.html'

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

# -------------------------------------------


class ReceiptsView(ListView):
    model = Receipts
    template_name = 'receipts/receipts.html'

    def get(self, request, *args, **kwargs):
        if 'btn_to_file' in request.GET:
            return self.to_file(request)
        return super().get(request, *args, **kwargs)

    def to_file(self, request):
        my_data = [["Organization", "Account", "Date", "Amount", "Currency", "Counterparty", "Item", "Project", "Comments"]]
        receipts = self.receipts_queryset(request)
        for i in receipts:
            my_data.append([i.organization, i.account, i.date, i.amount, i.currency, i.counterparty, i.item, i.project, i.comments])

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
        receipts = Receipts.objects.all()

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

        return receipts

    @staticmethod
    def htmx_list(request):
        context = {'object_list': ReceiptsView.receipts_queryset(request)}

        return render(request, 'receipts/receipts_list.html', context=context)


class ReceiptsIdView(UpdateView):
    model = Receipts
    template_name = 'receipts/receipts_id.html'
    form_class = ReceiptsAdd
    success_url = '/receipts'

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
        form = ReceiptsAdd(request.GET)
        return HttpResponse(form["account"])

    @staticmethod
    def htmx_projects(request):
        form = ReceiptsAdd(request.GET)
        return HttpResponse(form["project"])


class ReceiptsDeleteView(DeleteView):
    error = ''
    model = Receipts
    success_url = '/receipts'
    template_name = 'receipts/receipts_delete.html'






def ReceiptsPlanView(request):
    return render(request, 'receipts/receipts_plan.html')


class UploadFileView(FormView):
    form_class = UploadFile
    template_name = 'receipts/receipts_upload_file.html'
    success_url = '/receipts'

    def form_valid(self, form):
        csvfile = form.cleaned_data['file']
        f = TextIOWrapper(csvfile.file)
        reader = csv.DictReader(f, delimiter=';')
        for _, item in enumerate(reader, start=1):
            receipt = Receipts()
            try:
                receipt.organization = Organization.objects.get(organization=item.get('organization'))
                receipt.account = PaymentAccount.objects.get(account=item.get('account'))
                if item.get('project'):
                    receipt.project = Project.objects.get(project=item.get('project'))
                receipt.date = datetime.datetime.strptime(item.get('date'), '%d.%m.%Y').date()
                receipt.amount = Decimal(item.get('amount'))
                receipt.currency = Currencies.objects.get(code=item.get('currency'))
                receipt.counterparty = Counterparties.objects.get(counterparty=item.get('counterparty'))
                receipt.item = IncomeItem.objects.get(income_item=item.get('item'))
                receipt.comments = item.get('comments')
                receipt.save()
            except Exception as e:
                print(e)

        return super().form_valid(form)

