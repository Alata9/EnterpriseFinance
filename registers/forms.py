from django import forms
from django.forms import ModelForm, DateInput, DateField, ChoiceField, HiddenInput, ModelChoiceField, \
    MultipleChoiceField
from dynamic_forms import DynamicFormMixin, DynamicField

from directory.models import PaymentAccount, Currencies, Project
from payments.models import PaymentDocuments
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


class CounterpartyFlowsFilter(ModelForm):
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = PaymentDocuments
        fields = ['counterparty', 'date']
        widgets = {
            'date': DateInput(attrs={'type': 'Date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['counterparty'].empty_label = 'All counterparties'
        self.fields['counterparty'].required = True
        self.fields['date'].label = 'From:'
        self.fields['date'].required = False
        self.fields['date_end'].required = False


class AccountFlowsFilter(ModelForm):
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = PaymentDocuments
        fields = ['account', 'date']
        widgets = {
            'date': DateInput(attrs={'type': 'Date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].empty_label = 'All accounts'
        self.fields['account'].required = True
        self.fields['date'].label = 'From:'
        self.fields['date'].required = False
        self.fields['date_end'].required = False


class DashboardFilter(DynamicFormMixin, ModelForm):
    conversion_currency = ModelChoiceField(queryset=Currencies.objects.values_list("code", flat=True),
                                           empty_label='', required=False)
    date_start = DateField(label="From", widget=DateInput(attrs={'type': 'date'}), required=False)
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = PaymentDocuments
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
    Frequency = (
        ('by_years', 'by years'),
        ('by_quarter', 'by quarter'),
        ('by_month', 'by month'),
        ('by_week', 'by week'),
        ('by_days', 'by days'),
    )
    # frequency = ModelChoiceField(widget=forms.CharField, choices=Frequency)
    date_start = DateField(label="From", widget=DateInput(attrs={'type': 'date'}), required=False)
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = PaymentDocuments
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


