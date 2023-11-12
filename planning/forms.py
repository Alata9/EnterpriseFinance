
from django.forms import ModelForm, DateInput, Textarea, ModelChoiceField, DateField, ChoiceField, HiddenInput
from dynamic_forms import DynamicFormMixin, DynamicField

from directory.models import Project, Items
from planning.models import Calculations, PaymentDocumentPlan


class CalculationAdd(DynamicFormMixin, ModelForm):
    class Meta:
        model = Calculations
        fields = ('type_calc', 'name', 'flow', 'organization', 'counterparty', 'item', 'project', 'date_first',
                  'amount', 'currency', 'is_cash', 'frequency', 'loan_rate', 'term', 'comments')
        widgets = {'date_first': DateInput(attrs={'type': 'Date'}),
                   'comments': Textarea(attrs={'cols': 60, 'rows': 4, 'placeholder': 'Comments:'}),
                   }

    project = DynamicField(
        ModelChoiceField,
        queryset=lambda form: Project.objects.filter(organization=form['organization'].value()),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = 'Organization:'
        self.fields['currency'].empty_label = 'Currency:'
        self.fields['counterparty'].empty_label = 'Counterparty:'
        self.fields['item'].empty_label = 'Item:'
        self.fields['project'].empty_label = 'Project:'
        self.fields['frequency'].empty_label = ''

        self.fields['type_calc'].label = 'Type of calculation*'
        self.fields['is_cash'].label = 'is cash'
        self.fields['date_first'].label = 'First payment day'
        self.fields['name'].label = "Calculation's name (unique)*"
        self.fields['flow'].label = "Flow direction*"
        self.fields['term'].label = 'Quantity*'
        self.fields['amount'].label = 'Amount'
        self.fields['loan_rate'].label = 'Annual loan rate, %*'

        self.fields['name'].unique = True

        self.fields['project'].required = False
        self.fields['comments'].required = False
        self.fields['name'].required = True
        self.fields['date_first'].required = True
        self.fields['amount'].required = True
        self.fields['currency'].required = True
        self.fields['item'].required = True

        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')


class CalculationsFilter(ModelForm):
    ordering = ChoiceField(label='Ordering', required=False,
                           choices=[
                               ['date_first', 'by date'],
                               ['type_calc', 'by type'],
                               ['flow', 'by flow'],
                               ['amount', 'by amount'],
                               ['counterparty', 'by counterparty'],
                               ['item', 'by item'],
                               ['project', 'by project']
                           ])
    class Meta:
        model = Calculations
        fields = ['organization', 'project', 'counterparty', 'item', 'type_calc', 'flow']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = 'Organization:'
        self.fields['organization'].required = False
        self.fields['project'].empty_label = 'Project:'
        self.fields['project'].required = False
        self.fields['counterparty'].empty_label = 'Counterparty:'
        self.fields['counterparty'].required = False
        self.fields['item'].empty_label = 'Item:'
        self.fields['item'].required = False
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')


class ReceiptsPlanAdd(DynamicFormMixin, ModelForm):

    class Meta:
        model = PaymentDocumentPlan
        fields = ('organization', 'is_cash', 'date', 'inflow_amount', 'currency', 'counterparty', 'item', 'project',
                  'comments', 'calculation', 'flow')
        widgets = {'date': DateInput(attrs={'type': 'Date'}),
                   'comments': Textarea(attrs={'cols': 60, 'rows': 3}),
                   'flow': HiddenInput()}

    project = DynamicField(
        ModelChoiceField,
        queryset=lambda form: Project.objects.filter(organization=form['organization'].value()),
    )

    item = DynamicField(
        ModelChoiceField,
        queryset=lambda form: Items.objects.filter(flow='Receipts'))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = 'Organization:'
        self.fields['is_cash'].label = 'is cash'
        self.fields['counterparty'].empty_label = 'Counterparty:'
        self.fields['currency'].empty_label = 'Currency:'
        self.fields['item'].empty_label = 'Item:'
        self.fields['inflow_amount'].label = 'Amount'
        self.fields['project'].empty_label = 'Project:'
        self.fields['project'].required = False
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')


class ReceiptsPlanFilter(ModelForm):
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)
    ordering = ChoiceField(label='Ordering', required=False,
                           choices=[
                               ['date', 'by date'],
                               ['inflow_amount', 'by amount'],
                               ['counterparty', 'by counterparty'],
                               ['item', 'by item'],
                               ['project', 'by project'],
                               ['calculation', 'by calculation']
                           ])
    class Meta:
        model = PaymentDocumentPlan
        fields = ['organization', 'is_cash', 'currency', 'project', 'counterparty', 'item', 'date', 'calculation', 'flow']
        widgets = {
            'date': DateInput(attrs={'type': 'Date'}),
            'date_end': DateInput(attrs={'type': 'Date'}),
            'flow': HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = 'Organization:'
        self.fields['organization'].required = False
        self.fields['is_cash'].label = 'is cash'
        self.fields['currency'].empty_label = 'Currency'
        self.fields['is_cash'].required = False
        self.fields['project'].empty_label = 'Project:'
        self.fields['project'].required = False
        self.fields['counterparty'].empty_label = 'Counterparty:'
        self.fields['counterparty'].required = False
        self.fields['item'].empty_label = 'Item:'
        self.fields['item'].required = False
        self.fields['calculation'].empty_label = "Calculation's name:"
        self.fields['calculation'].required = False
        self.fields['date'].label = 'From'
        self.fields['date'].required = False
        self.fields['date_end'].required = False
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')


class PaymentsPlanAdd(DynamicFormMixin, ModelForm):
    class Meta:
        model = PaymentDocumentPlan
        fields = (
            'organization', 'is_cash', 'date', 'outflow_amount', 'currency', 'counterparty', 'item', 'project',
            'comments', 'calculation', 'flow')
        widgets = {'date': DateInput(attrs={'type': 'Date'}),
                   'comments': Textarea(attrs={'cols': 60, 'rows': 3}),
                   'flow': HiddenInput()}

    project = DynamicField(
        ModelChoiceField,
        queryset=lambda form: Project.objects.filter(organization=form['organization'].value()),
    )

    item = DynamicField(
        ModelChoiceField,
        queryset=lambda form: Items.objects.filter(flow='Payments'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = 'Organization:'
        self.fields['currency'].empty_label = 'Currency:'
        self.fields['counterparty'].empty_label = 'Counterparty:'
        self.fields['item'].empty_label = 'Item:'
        self.fields['outflow_amount'].label = 'Amount'
        self.fields['project'].empty_label = 'Project:'
        self.fields['project'].required = False
        self.fields['is_cash'].label = 'is cash'
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')


class PaymentsPlanFilter(ModelForm):
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)
    ordering = ChoiceField(label='Ordering', required=False,
                           choices=[
                               ['date', 'by date'],
                               ['outflow_amount', 'by amount'],
                               ['counterparty', 'by counterparty'],
                               ['item', 'by item'],
                               ['project', 'by project'],
                               ['calculation', 'by calculation']
                           ])
    class Meta:
        model = PaymentDocumentPlan
        fields = ['organization', 'currency', 'is_cash', 'project', 'counterparty', 'item', 'date', 'calculation', 'flow']
        widgets = {
            'date': DateInput(attrs={'type': 'Date'}),
            'date_end': DateInput(attrs={'type': 'Date'}),
            'flow': HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = 'Organization:'
        self.fields['organization'].required = False
        self.fields['currency'].empty_label = 'Currency:'
        self.fields['currency'].required = False
        self.fields['project'].empty_label = 'Project:'
        self.fields['project'].required = False
        self.fields['counterparty'].empty_label = 'Counterparty:'
        self.fields['counterparty'].required = False
        self.fields['calculation'].empty_label = "Calculation's name:"
        self.fields['calculation'].required = False
        self.fields['item'].empty_label = 'Item:'
        self.fields['item'].required = False
        self.fields['date'].label = 'From:'
        self.fields['date'].required = False
        self.fields['date_end'].required = False
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')
