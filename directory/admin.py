from django.contrib import admin

from directory.models import Organization, PaymentAccount, Project, Currencies, Counterparties


# directory
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'comments']
    list_display_links = ['id', 'organization', 'comments']
    search_fields = ['organization']


class PaymentAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'organization', 'is_cash', 'currency', 'comments', 'open_date', 'open_balance']
    list_display_links = ['id', 'account', 'organization', 'currency', 'comments']
    search_fields = ['account', 'organization', 'is_cash']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'project']
    list_display_links = ['id', 'organization', 'project']
    search_fields = ['organization', 'project']


class CurrenciesAdmin(admin.ModelAdmin):
    list_display = ['id', 'currency', 'code']
    list_display_links = ['id', 'currency', 'code']
    search_fields = ['currency', 'code']


class CounterpartiesAdmin(admin.ModelAdmin):
    list_display = ['id', 'counterparty', 'suppliers', 'customer', 'employee', 'other', 'comments']
    list_display_links = ['id', 'counterparty', 'suppliers', 'customer', 'employee', 'other', 'comments']
    search_fields = ['counterparty']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(PaymentAccount, PaymentAccountAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Currencies, CurrenciesAdmin)
admin.site.register(Counterparties, CounterpartiesAdmin)
