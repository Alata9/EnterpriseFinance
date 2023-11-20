from django.contrib import admin

from directory.models import (
    Organization, PaymentAccount, Project, Counterparties, InitialDebts,
    Currencies, CurrenciesRates, Items,
)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'comments']
    list_display_links = ['id', 'organization', 'comments']
    search_fields = ['organization']


class PaymentAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'organization', 'is_cash', 'currency', 'comments']
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


class CurrenciesRatesAdmin(admin.ModelAdmin):
    list_display = ['id', 'accounting_currency', 'currency', 'date', 'rate']
    list_display_links = ['id', 'accounting_currency', 'currency', 'date', 'rate']
    search_fields = ['accounting_currency', 'code']


class CounterpartiesAdmin(admin.ModelAdmin):
    list_display = ['id', 'counterparty', 'comments', 'suppliers', 'customer', 'employee', 'other']
    list_display_links = ['id', 'counterparty', 'comments', 'suppliers', 'customer', 'employee', 'other']
    search_fields = ['counterparty']


class InitialDebtsAdmin(admin.ModelAdmin):
    list_display = ['id', 'counterparty', 'comments', 'organization', 'type_debt', 'debit', 'credit', 'currency']
    list_display_links = ['id', 'counterparty', 'comments', 'organization', 'type_debt', 'debit', 'credit', 'currency']
    search_fields = ['counterparty', 'organization', 'type_debt']


class ItemsAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'group', 'flow', 'activity']
    list_display_links = ['id', 'code', 'name', 'group', 'flow', 'activity']
    search_fields = ['code', 'name']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(PaymentAccount, PaymentAccountAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Currencies, CurrenciesAdmin)
admin.site.register(CurrenciesRates, CurrenciesRatesAdmin)
admin.site.register(Counterparties, CounterpartiesAdmin)
admin.site.register(InitialDebts, InitialDebtsAdmin)
admin.site.register(Items, ItemsAdmin)

