from django.forms import ModelForm

from registers.models import *


class AccountSettingsSet(ModelForm):
    class Meta:
        model = AccountSettings
        fields = ('multiple_organizations', 'multiple_accounts',
                  'multiple_currencies', 'multiple_projects', 'organization_default')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization_default'].empty_label = ''