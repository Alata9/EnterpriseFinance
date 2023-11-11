from django.contrib import admin


from planning.models import PaymentsPlan, Calculations, ReceiptsPlan


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


class ReceiptsPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'date', 'amount', 'currency', 'is_cash',
                    'counterparty', 'item', 'project', 'comments']
    list_display_links = ['id', 'organization', 'date', 'amount', 'currency', 'is_cash',
                          'counterparty', 'item', 'project', 'comments']
    search_fields = ['organization', 'date', 'counterparty', 'currency', 'item', 'project']


admin.site.register(PaymentsPlan, PaymentsPlanAdmin)
admin.site.register(Calculations, CalculationsAdmin)
admin.site.register(ReceiptsPlan, ReceiptsPlanAdmin)