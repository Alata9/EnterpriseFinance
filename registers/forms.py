from django import forms
from django.forms import ModelForm, DateInput, DateField, ModelChoiceField, ChoiceField
from dynamic_forms import DynamicField, DynamicFormMixin

from directory.models import Organization, PaymentAccount, CurrenciesRates, Currencies, Project, TypeCF
from payments.models import Payments
from receipts.models import IncomeGroup
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
        self.fields['accounting_currency'].label = 'Main accounting currency'

class AccountBalancesFilter(DynamicFormMixin, ModelForm):
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
        self.fields['date_start'].required = False
        self.fields['date_end'].required = False


class DashboardFilter(DynamicFormMixin, ModelForm):

    conversion_currency = ModelChoiceField(queryset=Currencies.objects.values_list("code", flat=True),
                                           empty_label='', required=False)
    date_start = DateField(label="From", widget=DateInput(attrs={'type': 'date'}), required=False)
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Payments
        fields = ['organization', 'project']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = ''
        self.fields['organization'].required = False
        self.fields['project'].empty_label = ''
        self.fields['project'].required = False

    @staticmethod
    def project_filter(form):
        if form['organization'].value():
            return Project.objects.filter(organization=form['organization'].value())

        return Project.objects.all()

    project = DynamicField(
        ModelChoiceField,
        queryset=project_filter,
    )

class CFStatementFilter(DynamicFormMixin, ModelForm):
    activities = ModelChoiceField(queryset=TypeCF.objects.values_list("type", flat=True),
                                           empty_label='', required=False)
    conversion_currency = ModelChoiceField(queryset=Currencies.objects.values_list("code", flat=True),
                                           empty_label='', required=False)
    date_start = DateField(label="From", widget=DateInput(attrs={'type': 'date'}), required=False)
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Payments
        fields = ['organization', 'project']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = ''
        self.fields['organization'].required = False
        self.fields['project'].empty_label = ''
        self.fields['project'].required = False


    @staticmethod
    def project_filter(form):
        if form['organization'].value():
            return Project.objects.filter(organization=form['organization'].value())

        return Project.objects.all()

    project = DynamicField(
        ModelChoiceField,
        queryset=project_filter,
    )


