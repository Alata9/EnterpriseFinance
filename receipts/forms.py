from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput, Textarea, HiddenInput, DateField, ModelChoiceField, Form, FileField, \
    ChoiceField
from dynamic_forms import DynamicField, DynamicFormMixin

from directory.models import PaymentAccount, Project
from receipts.models import IncomeGroup, IncomeItem, Receipts, ReceiptsPlan, ChangePayAccount


class IncomeGroupAdd(ModelForm):
    class Meta:
        model = IncomeGroup
        fields = ('income_group', 'type_cf', 'comments')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_cf'].empty_label = ''
        self.fields['type_cf'].label = 'Activities'


class IncomeItemAdd(ModelForm):
    class Meta:
        model = IncomeItem
        fields = ('income_item', 'income_group')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['income_group'].empty_label = ''



class ReceiptsAdd(DynamicFormMixin, ModelForm):

    class Meta:
        model = Receipts
        fields = (
            'organization', 'account', 'date', 'amount', 'currency', 'counterparty', 'item', 'project', 'comments')
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
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('income_item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')
        self.fields['account'].queryset = self.fields['account'].queryset.order_by('account')

    def clean(self):
        cleaned_data = super().clean()
        acc = cleaned_data.get('account')

        if not acc or not acc.currency:
            raise ValidationError("Account with currency required")

        cleaned_data['currency'] = acc.currency

        return cleaned_data



class ReceiptsFilter(ModelForm):
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
        model = Receipts
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
        self.fields['account'].bold = True
        self.fields['project'].empty_label = 'Project:'
        self.fields['project'].required = False
        self.fields['counterparty'].empty_label = 'Counterparty:'
        self.fields['counterparty'].required = False
        self.fields['item'].empty_label = 'Item:'
        self.fields['item'].required = False
        self.fields['date'].label = 'From'
        self.fields['date'].required = False
        self.fields['date_end'].required = False
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('income_item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')
        self.fields['account'].queryset = self.fields['account'].queryset.order_by('account')


class ReceiptsPlanAdd(DynamicFormMixin, ModelForm):

    class Meta:
        model = ReceiptsPlan
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
        self.fields['is_cash'].label = 'is cash'
        self.fields['counterparty'].empty_label = 'Counterparty:'
        self.fields['currency'].empty_label = 'Currency:'
        self.fields['item'].empty_label = 'Item:'
        self.fields['project'].empty_label = 'Project:'
        self.fields['project'].required = False
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('income_item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')


class ReceiptsPlanFilter(ModelForm):
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
        model = ReceiptsPlan
        fields = ['organization', 'is_cash', 'currency', 'project', 'counterparty', 'item', 'date']
        widgets = {
            'date': DateInput(attrs={'type': 'Date'}),
            'date_end': DateInput(attrs={'type': 'Date'}),
        }

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
        self.fields['date'].label = 'From'
        self.fields['date'].required = False
        self.fields['date_end'].required = False
        self.fields['counterparty'].queryset = self.fields['counterparty'].queryset.order_by('counterparty')
        self.fields['item'].queryset = self.fields['item'].queryset.order_by('income_item')
        self.fields['project'].queryset = self.fields['project'].queryset.order_by('project')


class ChangePayAccountAdd(ModelForm):
    class Meta:
        model = ChangePayAccount
        fields = ('pay_account_from', 'pay_account_to', 'date', 'amount', 'currency')
        widgets = {'date': DateInput(attrs={'type': 'Date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pay_account_from'].empty_label = ''
        self.fields['pay_account_from'].label = 'From'
        self.fields['pay_account_to'].empty_label = ''
        self.fields['pay_account_to'].label = 'To'
        self.fields['currency'].empty_label = ''


class ChangePayAccountFilter(ModelForm):
    class Meta:
        model = ChangePayAccount
        fields = ['pay_account_from', 'pay_account_to', 'amount', 'currency', 'date']
        widgets = {
            'date': DateInput(attrs={'type': 'Date'}),
            'date_end': DateInput(attrs={'type': 'Date'}),
        }
    date_end = DateField(label="To", widget=DateInput(attrs={'type': 'date'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pay_account_from'].label = 'Account from:'
        self.fields['pay_account_from'].empty_label = ''
        self.fields['pay_account_from'].required = False
        self.fields['pay_account_to'].label = 'Account to:'
        self.fields['pay_account_to'].empty_label = ''
        self.fields['pay_account_to'].required = False
        self.fields['date'].label = 'From'
        self.fields['date'].required = False
        self.fields['date_end'].required = False
        self.fields['currency'].empty_label = ''
        self.fields['currency'].required = False


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