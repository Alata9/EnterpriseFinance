from django import forms
from django.core.exceptions import ValidationError
from django.db.models import DateField
from django.forms import ModelForm, Textarea, DateInput, DateField

from directory.models import (
    Organization, Project, PaymentAccount, Counterparties, Currencies, CurrenciesRates, InitialDebts
)


class OrganizationAdd(ModelForm):
    class Meta:
        model = Organization
        fields = ('organization', 'comments')
        widgets = {'comments': Textarea(attrs={'cols': 60, 'rows': 3})}


class ProjectAdd(ModelForm):
    class Meta:
        model = Project
        fields = ('project', 'organization', 'comments')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = ''


class PaymentAccountAdd(ModelForm):
    class Meta:
        model = PaymentAccount
        fields = ('account', 'organization', 'currency', 'is_cash', 'comments')
        widgets = {
            'open_date': DateInput(attrs={'type': 'Date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = ''
        self.fields['currency'].empty_label = ''


class CounterpartyAdd(ModelForm):
    class Meta:
        model = Counterparties
        fields = ('counterparty', 'suppliers', 'customer', 'employee', 'other', 'comments' )

    def clean(self):
        cleaned_data = super().clean()
        if not any(self.data.get(x, '') == 'on' for x in ['suppliers', 'customer', 'employee', 'other']):
            raise ValidationError('Error')

        return cleaned_data


class InitialDebtsAdd(ModelForm):
    class Meta:
        model = InitialDebts
        fields = ('counterparty', 'organization', 'type_debt', 'debit', 'credit', 'currency', 'comments')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_debt'].empty_label = ''
        self.fields['type_debt'].label = 'Type of debt'
        self.fields['counterparty'].empty_label = ''
        self.fields['organization'].empty_label = ''
        self.fields['currency'].empty_label = ''


class InitialDebtsFilter(ModelForm):
    class Meta:
        model = InitialDebts
        fields = ('counterparty', 'organization', 'type_debt')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_debt'].empty_label = ''
        self.fields['type_debt'].label = 'Type of debt'
        self.fields['counterparty'].empty_label = ''
        self.fields['organization'].empty_label = ''


class CurrencyAdd(ModelForm):
    class Meta:
        model = Currencies
        fields = ('currency', 'code')


class CurrenciesRatesAdd(ModelForm):
    class Meta:
        model = CurrenciesRates
        fields = ('accounting_currency', 'currency', 'date', 'rate')
        widgets = {
            'date': DateInput(attrs={'type': 'Date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].empty_label = ''
        self.fields['accounting_currency'].empty_label = ''


class RatesFilter(ModelForm):
    date_end = DateField(label='To', widget=DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = CurrenciesRates
        fields = ['accounting_currency', 'currency', 'date']
        widgets = {
            'date': DateInput(attrs={'type': 'Date'}),
            'date_end': DateInput(attrs={'type': 'Date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['accounting_currency'].empty_label = ''
        self.fields['accounting_currency'].required = False
        self.fields['currency'].empty_label = ''
        self.fields['currency'].required = False
        self.fields['date'].label = 'From'
        self.fields['date'].required = False
        self.fields['date_end'].required = False


class RatesParser(ModelForm):
    class Meta:
        model = CurrenciesRates
        fields = ['accounting_currency', 'currency']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['accounting_currency'].empty_label = ''
        self.fields['accounting_currency'].required = True
        self.fields['currency'].empty_label = ''
        self.fields['currency'].required = True

