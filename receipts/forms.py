from django.forms import ModelForm, DateInput, Textarea

from receipts.models import *


class IncomeGroupAdd(ModelForm):
    class Meta:
        model = IncomeGroup
        fields = ('income_group', 'comments')


class IncomeItemAdd(ModelForm):
    class Meta:
        model = IncomeItem
        fields = ('income_item', 'income_group')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['income_group'].empty_label = ''


class ReceiptsAdd(ModelForm):
    class Meta:
        model = Receipts
        fields = ('organization', 'account', 'date', 'amount', 'counterparty', 'item', 'project', 'comments')
        widgets = {'date': DateInput(attrs={'type': 'Date'}),
                   'comments': Textarea(attrs={'cols': 60, 'rows': 6})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = ''
        self.fields['account'].empty_label = ''
        self.fields['counterparty'].empty_label = ''
        self.fields['item'].empty_label = ''
        self.fields['project'].empty_label = ''