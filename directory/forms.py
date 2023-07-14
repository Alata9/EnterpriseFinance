from django.forms import ModelForm, Textarea

from directory.models import Organization, Project, PaymentAccount, Counterparties, Currencies


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
        fields = ('account', 'organization', 'currency', 'is_cash', 'comments')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = ''
        self.fields['currency'].empty_label = ''
        # self.fields['is_cash'].


class CounterpartyAdd(ModelForm):
    class Meta:
        model = Counterparties
        fields = ('counterparty', 'suppliers', 'customer', 'employee', 'other', 'comments')


class CurrencyAdd(ModelForm):
    class Meta:
        model = Currencies
        fields = ('currency', 'code')
