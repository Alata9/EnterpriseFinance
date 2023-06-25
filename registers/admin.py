from django.contrib import admin

from registers.models import Rates, AccountSettings


# registers
class RatesAdmin(admin.ModelAdmin):
    list_display = ['id', 'currency', 'date', 'rate']
    list_display_links = ['id', 'currency', 'date', 'rate']
    search_fields = ['currency', 'date', 'rate']


class AccountSettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'multiple_organizations', 'multiple_accounts',
                    'multiple_currencies', 'multiple_projects', 'organization_default']
    list_display_links = ['multiple_organizations', 'multiple_accounts',
                          'multiple_currencies', 'multiple_projects', 'organization_default']
    search_fields = ['multiple_organizations', 'multiple_accounts',
                     'multiple_currencies', 'multiple_projects', 'organization_default']


admin.site.register(Rates, RatesAdmin)
admin.site.register(AccountSettings, AccountSettingsAdmin)
