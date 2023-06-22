from django.forms import ModelForm, BooleanField, Textarea

from directory.models import *


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
        model = Payment_account
        fields = ('account', 'organization', 'currency', 'is_cash',  'comments')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = ''
        self.fields['currency'].empty_label = ''
        # self.fields['is_cash'].


class CounterpartyAdd(ModelForm):
    class Meta:
        model = Сounterparties
        fields = ('counterparty', 'suppliers', 'customer', 'employee', 'other', 'comments')


class CurrencyAdd(ModelForm):
    class Meta:
        model = Currenсies
        fields = ('currency', 'code')