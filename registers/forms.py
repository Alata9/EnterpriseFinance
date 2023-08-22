from django.forms import ModelForm, DateInput, DateField

from directory.models import Organization
from registers.models import AccountSettings


class AccountSettingsSet(ModelForm):
    class Meta:
        model = AccountSettings
        fields = ('multiple_organizations', 'multiple_accounts',
                  'multiple_currencies', 'multiple_projects', 'organization_default')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization_default'].empty_label = ''

# account balances
# cash flow statement
# cash flow budget
# cash flow plan-fact


class AccountBalancesFilter(ModelForm):
    # date_start = DateField(lable="From", widget=DateInput(attrs={'type': 'date'}), required=False)
    # date_end = DateField(lable="To", widget=DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Organization
        fields = ['organization']
        # widgets = {
        #     'date_start': DateInput(attrs={'type': 'Date'}),
        #     'date_end': DateInput(attrs={'type': 'Date'}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].empty_label = ''
        self.fields['organization'].required = False
        # self.fields['date_start'].required = False
        # self.fields['date_end'].required = False