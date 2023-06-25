from django import forms
from django.forms import ModelForm, DateInput, Textarea, HiddenInput, DateField
from dynamic_forms import DynamicFormMixin, DynamicField

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
        fields = ('organization', 'account', 'date', 'amount', 'currency', 'counterparty', 'item', 'project', 'comments')
        widgets = {'date': DateInput(attrs={'type': 'Date'}),
                   'comments': Textarea(attrs={'cols': 60, 'rows': 6}),
                   'currency': HiddenInput()}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = ''
        self.fields['account'].empty_label = ''
        self.fields['account'].queryset = Payment_account.objects.filter(organization=self.initial.get('organization'))
        self.fields['counterparty'].empty_label = ''
        self.fields['item'].empty_label = ''
        self.fields['project'].empty_label = ''


    # def account_choices(self):
    #     org = self.initial.get('organization')
    #     return Payment_account.objects.filter(organization=org)
    #
    #
    # def account_initial(self):
    #     org = self.initial.get('organization')
    #     return Payment_account.objects.filter(organization=org).first()
    #
    # account = forms.ModelChoiceField(queryset=account_choices, initial=account_initial)


class ReceiptsFilter(ModelForm):
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Receipts
        fields = ['organization', 'account', 'project', 'counterparty', 'item', 'date']
        widgets = {
            'date': DateInput(attrs={'type': 'Date'}),
            'date_end': DateInput(attrs={'type': 'Date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = ''
        self.fields['organization'].required = False
        self.fields['account'].empty_label = ''
        self.fields['account'].required = False
        self.fields['project'].empty_label = ''
        self.fields['project'].required = False
        self.fields['counterparty'].empty_label = ''
        self.fields['counterparty'].required = False
        self.fields['item'].empty_label = ''
        self.fields['item'].required = False
        self.fields['date'].label = 'From'
        self.fields['date'].required = False
        self.fields['date_end'].required = False


