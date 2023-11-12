from django.forms import ModelForm, DateInput, DateField, ChoiceField, HiddenInput
from dynamic_forms import DynamicFormMixin

from directory.models import PaymentAccount
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


class AccountFlowsFilter(ModelForm):
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)
    ordering = ChoiceField(label='Ordering', required=False,
                           choices=[
                               ['date', 'by date'],
                               ['inflow_amount', 'by inflow'],
                               ['outflow_amount', 'by outflow'],
                               ['counterparty', 'by counterparty'],
                               ['item', 'by item'],
                               ['project', 'by project']
                           ])
    class Meta:
        model = PaymentDocuments
        fields = ['organization', 'account', 'project', 'counterparty', 'item', 'date']
        widgets = {
            'date': DateInput(attrs={'type': 'Date'}),
            'date_end': DateInput(attrs={'type': 'Date'}),
            }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = 'Organization:'
        self.fields['organization'].required = False
        self.fields['account'].empty_label = 'Account:'
        self.fields['account'].required = False
        self.fields['project'].empty_label = 'Project:'
        self.fields['project'].required = False
        self.fields['counterparty'].empty_label = 'Counterparty:'
        self.fields['counterparty'].required = False
        self.fields['item'].empty_label = 'Item:'
        self.fields['item'].required = False
        self.fields['date'].label = 'From:'
        self.fields['date'].required = False
        self.fields['date_end'].required = False
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')
        self.fields['account'].queryset = self.fields['account'].queryset.order_by('account')



# class DashboardFilter(DynamicFormMixin, ModelForm):
#
#     conversion_currency = ModelChoiceField(queryset=Currencies.objects.values_list("code", flat=True),
#                                            empty_label='', required=False)
#     date_start = DateField(label="From", widget=DateInput(attrs={'type': 'date'}), required=False)
#     date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)
#
#     class Meta:
#         model = Payments
#         fields = ['organization', 'project']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['organization'].empty_label = ''
#         self.fields['organization'].required = False
#         self.fields['project'].empty_label = ''
#         self.fields['project'].required = False
#
#     @staticmethod
#     def project_filter(form):
#         if form['organization'].value():
#             return Project.objects.filter(organization=form['organization'].value())
#
#         return Project.objects.all()
#
#     project = DynamicField(
#         ModelChoiceField,
#         queryset=project_filter,
#     )
#
#
# class CFStatementFilter(DynamicFormMixin, ModelForm):
#     activities = ModelChoiceField(queryset=TypeCF.objects.values_list("type", flat=True),
#                                            empty_label='', required=False)
#     conversion_currency = ModelChoiceField(queryset=Currencies.objects.values_list("code", flat=True),
#                                            empty_label='', required=False)
#     date_start = DateField(label="From", widget=DateInput(attrs={'type': 'date'}), required=False)
#     date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)
#
#     class Meta:
#         model = Payments
#         fields = ['organization', 'project']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['organization'].empty_label = ''
#         self.fields['organization'].required = False
#         self.fields['project'].empty_label = ''
#         self.fields['project'].required = False
#
#
#     @staticmethod
#     def project_filter(form):
#         if form['organization'].value():
#             return Project.objects.filter(organization=form['organization'].value())
#
#         return Project.objects.all()
#
#     project = DynamicField(
#         ModelChoiceField,
#         queryset=project_filter,
#     )
#
#
