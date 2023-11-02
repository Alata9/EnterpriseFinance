from django.contrib import admin

from payments.models import ExpenseGroup, ExpensesItem, Payments, PaymentsPlan, Calculations


class ExpensesGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'expense_group', 'comments']
    list_display_links = ['id', 'expense_group', 'comments']
    search_fields = ['expense_group']


class ExpensesItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'expense_item', 'expense_group']
    list_display_links = ['id', 'expense_item', 'expense_group']
    search_fields = ['expense_item']


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'date', 'amount', 'account', 'currency',
                    'counterparty', 'item', 'project', 'by_request', 'comments']
    list_display_links = ['id', 'organization', 'date', 'amount', 'account', 'currency',
                          'counterparty', 'item', 'project', 'by_request', 'comments']
    search_fields = ['organization', 'date', 'counterparty', 'account', 'item', 'project']


class PaymentsPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'date', 'amount', 'currency', 'is_cash',
                    'counterparty', 'item', 'project', 'comments']
    list_display_links = ['id', 'organization', 'date', 'amount', 'currency', 'is_cash',
                          'counterparty', 'item', 'project', 'comments']
    search_fields = ['organization', 'date', 'counterparty', 'currency', 'item', 'project']


class CalculationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type_calc', 'flow', 'organization', 'date_first', 'amount', 'currency', 'is_cash',
                    'frequency', 'loan_rate', 'term', 'counterparty', 'item', 'project', 'comments']
    list_display_links = ['id', 'name', 'type_calc', 'flow', 'organization', 'date_first', 'amount', 'currency', 'is_cash',
                          'frequency', 'loan_rate', 'term', 'counterparty', 'item', 'project', 'comments']
    search_fields = ['name', 'type_calc', 'organization', 'counterparty', 'item', 'project']


admin.site.register(ExpenseGroup, ExpensesGroupAdmin)
admin.site.register(ExpensesItem, ExpensesItemAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(PaymentsPlan, PaymentsPlanAdmin)
admin.site.register(Calculations, CalculationsAdmin)
