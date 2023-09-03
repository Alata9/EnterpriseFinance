from django.contrib import admin

from registers.models import AccountSettings


# registers
class AccountSettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'multiple_organizations', 'multiple_accounts',
                    'multiple_currencies', 'multiple_projects', 'organization_default', 'accounting_currency']
    list_display_links = ['multiple_organizations', 'multiple_accounts',
                          'multiple_currencies', 'multiple_projects', 'organization_default', 'accounting_currency']
    search_fields = ['multiple_organizations', 'multiple_accounts',
                     'multiple_currencies', 'multiple_projects', 'organization_default', 'accounting_currency']


admin.site.register(AccountSettings, AccountSettingsAdmin)
