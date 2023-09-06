from django.forms import ModelForm, DateInput, DateField, ModelChoiceField

from directory.models import Organization, PaymentAccount, CurrenciesRates, Currencies
from payments.models import Payments
from registers.models import AccountSettings


class AccountSettingsSet(ModelForm):
    class Meta:
        model = AccountSettings
        fields = ('multiple_organizations', 'organization_default', 'multiple_accounts',
                  'multiple_currencies', 'accounting_currency', 'multiple_projects')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization_default'].empty_label = ''
        self.fields['accounting_currency'].empty_label = ''


class AccountBalancesFilter(ModelForm):
    conversion_currency = ModelChoiceField(queryset=Currencies.objects.values_list("code", flat=True), empty_label='')
    date_start = DateField(label="From", widget=DateInput(attrs={'type': 'date'}), required=False)
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = PaymentAccount
        fields = ['organization', 'is_cash', 'currency']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = ''
        self.fields['organization'].required = False
        self.fields['currency'].empty_label = ''
        self.fields['currency'].label = 'Accounting currency'
        self.fields['currency'].required = False
        self.fields['conversion_currency'].required = False
        self.fields['date_start'].required = False
        self.fields['date_end'].required = False



