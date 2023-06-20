from django.contrib import admin

from directory.models import *
from payments.models import *
from receipts.models import *
from registers.models import *

# directory
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'comments']
    list_display_links = ['id', 'organization', 'comments']
    search_fields = ['organization']

class Payment_accountAdmin(admin.ModelAdmin):
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

class CounterpartiesAdmin(admin.ModelAdmin):
    list_display = ['id', 'counterparty', 'suppliers', 'customer', 'employee', 'other', 'comments']
    list_display_links = ['id', 'counterparty', 'suppliers', 'customer', 'employee', 'other', 'comments']
    search_fields = ['counterparty']

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Payment_account, Payment_accountAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Currenсies, CurrenciesAdmin)
admin.site.register(Сounterparties, CounterpartiesAdmin)

# receipts
class IncomeGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'income_group', 'comments']
    list_display_links = ['id', 'income_group', 'comments']
    search_fields = ['income_group']

class IncomeItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'income_item', 'income_group']
    list_display_links = ['id', 'income_item', 'income_group']
    search_fields = ['income_item']

class ReceiptsAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'date', 'amount', 'account', 'currency', 'counterparty', 'item', 'project', 'comments']
    list_display_links = ['id', 'organization', 'date', 'amount', 'account', 'currency', 'counterparty', 'item', 'project', 'comments']
    search_fields = ['organization', 'date', 'counterparty', 'account', 'currency', 'item', 'project']

class Receipts_planAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'date', 'amount', 'currency', 'is_cash', 'counterparty', 'item', 'project', 'comments']
    list_display_links = ['id', 'organization', 'date', 'amount', 'currency', 'is_cash', 'counterparty', 'item', 'project', 'comments']
    search_fields = ['organization', 'date', 'counterparty', 'currency', 'item', 'project']


admin.site.register(IncomeGroup, IncomeGroupAdmin)
admin.site.register(IncomeItem, IncomeItemAdmin)
admin.site.register(Receipts, ReceiptsAdmin)
admin.site.register(Receipts_plan, Receipts_planAdmin)

# payments
class ExpensesGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'expense_group', 'comments']
    list_display_links = ['id', 'expense_group', 'comments']
    search_fields = ['expense_group']

class ExpensesItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'expense_item', 'expense_group']
    list_display_links = ['id', 'expense_item', 'expense_group']
    search_fields = ['expense_item']

class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'date', 'amount', 'account', 'counterparty', 'item', 'project', 'comments']
    list_display_links = ['id', 'organization', 'date', 'amount', 'account', 'counterparty', 'item', 'project', 'comments']
    search_fields = ['organization', 'date', 'counterparty', 'account', 'item', 'project']

class Payments_planAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'date', 'amount', 'currency', 'is_cash', 'counterparty', 'item', 'project', 'comments']
    list_display_links = ['id', 'organization', 'date', 'amount', 'currency', 'is_cash', 'counterparty', 'item', 'project', 'comments']
    search_fields = ['organization', 'date', 'counterparty', 'currency', 'item', 'project']

admin.site.register(ExpenseGroup, ExpensesGroupAdmin)
admin.site.register(ExpensesItem, ExpensesItemAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(Payments_plan, Payments_planAdmin)

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

