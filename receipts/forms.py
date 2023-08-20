from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput, Textarea, HiddenInput, DateField, ModelChoiceField, Form, FileField
from dynamic_forms import DynamicField, DynamicFormMixin

from directory.models import PaymentAccount, Project
from receipts.models import IncomeGroup, IncomeItem, Receipts


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
        self.fields['account'].bold = True
        self.fields['project'].empty_label = ''
        self.fields['project'].required = False
        self.fields['counterparty'].empty_label = ''
        self.fields['counterparty'].required = False
        self.fields['item'].empty_label = ''
        self.fields['item'].required = False
        self.fields['date'].label = 'From'
        self.fields['date'].required = False
        self.fields['date_end'].required = False


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