from django.core.exceptions import ValidationError
from django.forms import ModelForm, Textarea, DateInput

from directory.models import Organization, Project, PaymentAccount, Counterparties, Currencies, CurrenciesRates


class OrganizationAdd(ModelForm):
    class Meta:
        model = Organization
        fields = ('organization', 'comments')
        widgets = {'comments': Textarea(attrs={'cols': 60, 'rows': 6})}


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
        fields = ('account', 'organization', 'currency', 'is_cash', 'open_date', 'open_balance', 'comments')
        widgets = {
            'open_date': DateInput(attrs={'type': 'Date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = ''
        self.fields['currency'].empty_label = ''
        self.fields['open_date'].label = 'Opening date'
        self.fields['open_balance'].label = 'Opening balance'


class CounterpartyAdd(ModelForm):
    class Meta:
        model = Counterparties
        fields = ('counterparty', 'suppliers', 'customer', 'employee', 'other', 'comments')

    def clean(self):
        cleaned_data = super().clean()
        if not any(self.data.get(x, '') == 'on' for x in ['suppliers', 'customer', 'employee', 'other']):
            raise ValidationError('Error')

        return cleaned_data


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