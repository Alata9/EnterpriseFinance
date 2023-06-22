from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView

from receipts.forms import *
from receipts.models import *
from registers.models import AccountSettings

# --------------------------------------
def IncomeGroupView(request):
    income_groups = IncomeGroup.objects.all()
    if request.method == 'POST':
        form = IncomeGroupAdd(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('income_group')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = IncomeGroupAdd()
    context = {'form': form,
               'income_groups': income_groups}
    return render(request, 'receipts/income_group.html', context=context)


# -------------------------------------------

def IncomeItemView(request):
    income_items = IncomeItem.objects.all()

    if request.method == 'POST':
        form = IncomeItemAdd(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('income_item')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = IncomeItemAdd()

    context = {'form': form,
               'income_items': income_items}

    return render(request, 'receipts/income_item.html', context=context)


def ReceiptsPlanView(request):
    return render(request, 'receipts/receipts_plan.html')


def ReceiptsView(request):
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

    context = {'receipts': receipts,
               'form': form}

    return render(request, 'receipts/receipts.html', context=context)



class ReceiptsIdView(UpdateView):
    model = Receipts
    template_name = 'receipts/receipts_id.html'
    form_class = ReceiptsAdd

    def get_object(self):
        if 'pk' in self.kwargs:
            return super().get_object()

        org = AccountSettings.load().organization_default
        return self.model(organization=org)

    def form_valid(self, form):
        try:
            receipt = form.save(commit=False)
            receipt.currency = receipt.account.currency
            receipt.save()
            return redirect('receipts')
        except:
            form.add_error(None, 'Data save error')



class ReceiptsDeleteView(DeleteView):
    error = ''
    model = Receipts
    success_url = '/receipts'
    template_name = 'receipts/receipts_delete.html'


class IncomeItemDeleteView(DeleteView):
    error = ''
    model = IncomeItem
    success_url = '/income_item'
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
