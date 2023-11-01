from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput, Textarea, HiddenInput, ModelChoiceField, DateField, Form, FileField, \
    ChoiceField, IntegerField, CharField, DecimalField
from dynamic_forms import DynamicFormMixin, DynamicField

from directory.models import PaymentAccount, Project
from payments.models import ExpenseGroup, ExpensesItem, Payments, PaymentsPlan, Calculations


class ExpenseGroupAdd(ModelForm):
    class Meta:
        model = ExpenseGroup
        fields = ('expense_group', 'type_cf', 'comments')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_cf'].empty_label = ''
        self.fields['type_cf'].label = 'Activities'


class ExpenseItemAdd(ModelForm):
    class Meta:
        model = ExpensesItem
        fields = ('expense_item', 'expense_group')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expense_group'].empty_label = ''


class PaymentsAdd(DynamicFormMixin, ModelForm):
    class Meta:
        model = Payments
        fields = (
            'organization', 'account', 'date', 'amount', 'currency', 'counterparty', 'item', 'project', 'by_request', 'comments')
        widgets = {'date': DateInput(attrs={'type': 'Date'}),
                   'comments': Textarea(attrs={'cols': 60, 'rows': 3}),
                   'currency': HiddenInput()}

    account = DynamicField(
        ModelChoiceField,
        queryset=lambda form: PaymentAccount.objects.filter(organization=form['organization'].value()),
    )

    project = DynamicField(
        ModelChoiceField,
        queryset=lambda form: Project.objects.filter(organization=form['organization'].value()),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = 'Organization:'
        self.fields['account'].empty_label = 'Account:'
        self.fields['counterparty'].empty_label = 'Counterparty:'
        self.fields['item'].empty_label = 'Item:'
        self.fields['project'].empty_label = 'Project:'
        self.fields['project'].required = False
        self.fields['by_request'].empty_label = 'by Request:'
        self.fields['by_request'].required = False
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('expense_item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')
        self.fields['account'].queryset = self.fields['account'].queryset.order_by('account')

    def clean(self):
        cleaned_data = super().clean()
        acc = cleaned_data.get('account')

        if not acc or not acc.currency:
            raise ValidationError("Account with currency required")

        cleaned_data['currency'] = acc.currency

        return cleaned_data


class PaymentsFilter(ModelForm):
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)
    ordering = ChoiceField(label='Ordering', required=False,
                           choices=[
                               ['date', 'by date'],
                               ['amount', 'by amount'],
                               ['counterparty', 'by counterparty'],
                               ['item', 'by item'],
                               ['project', 'by project']
                           ])
    class Meta:
        model = Payments
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
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('expense_item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')
        self.fields['account'].queryset = self.fields['account'].queryset.order_by('account')


class PaymentsPlanAdd(DynamicFormMixin, ModelForm):
    class Meta:
        model = PaymentsPlan
        fields = (
            'organization', 'is_cash', 'date', 'amount', 'currency', 'counterparty', 'item', 'project', 'comments')
        widgets = {'date': DateInput(attrs={'type': 'Date'}),
                   'comments': Textarea(attrs={'cols': 60, 'rows': 3}),
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
        self.fields['project'].required = False
        self.fields['is_cash'].label = 'is cash'
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('expense_item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')


class CalculationAdd(DynamicFormMixin, ModelForm):
    class Meta:
        model = Calculations
        fields = ('type_calc', 'name', 'organization', 'counterparty', 'item', 'project', 'date_first',
                  'amount', 'currency', 'is_cash', 'frequency', 'loan_rate', 'term', 'comments')
        widgets = {'date_first': DateInput(attrs={'type': 'Date'}),
                   'comments': Textarea(attrs={'cols': 60, 'rows': 2, 'placeholder': 'Comments:'}),
                   'name': DateInput(attrs={'placeholder': "Calculation's name:"}),
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
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].empty_label = 'Item:'
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('expense_item')
        self.fields['project'].empty_label = 'Project:'
        self.fields['project'].required = False
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')
        self.fields['comments'].required = False
        self.fields['type_calc'].empty_label = 'Type of calculation:'
        self.fields['frequency'].empty_label = ''
        self.fields['is_cash'].label = 'is cash'
        self.fields['date_first'].label = 'First payment day'
        self.fields['name'].label = "Calculation's name (must be unique):"
        self.fields['name'].unique = True
        self.fields['date_first'].required = True
        self.fields['term'].label = 'Quantity of payments'
        self.fields['amount'].label = 'Regular amount'
        self.fields['amount'].required = True
        self.fields['currency'].required = True
        self.fields['item'].required = True



class PaymentsPlanFilter(ModelForm):
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)
    ordering = ChoiceField(label='Ordering', required=False,
                           choices=[
                               ['date_first', 'by date'],
                               ['amount', 'by amount'],
                               ['counterparty', 'by counterparty'],
                               ['item', 'by item'],
                               ['project', 'by project']
                           ])
    class Meta:
        model = PaymentsPlan
        fields = ['organization', 'currency', 'is_cash', 'project', 'counterparty', 'item', 'date']
        widgets = {
            'date': DateInput(attrs={'type': 'Date'}),
            'date_end': DateInput(attrs={'type': 'Date'}),
        }

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
        self.fields['item'].empty_label = 'Item:'
        self.fields['item'].required = False
        self.fields['date'].label = 'From:'
        self.fields['date'].required = False
        self.fields['date_end'].required = False
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('expense_item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')



class UploadFile(Form):
    file = FileField()

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")
        if not file.name.endswith(".csv"):
            raise ValidationError(
                {
                    "file": "Filetype not supported, the file must be a '.csv'",
                }
            )
        return cleaned_data