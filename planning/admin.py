from django.contrib import admin

from planning.models import PaymentDocumentPlan, Calculations


class PaymentDocumentPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'date', 'outflow_amount', 'inflow_amount', 'currency', 'calculation',
                    'counterparty', 'item', 'project', 'comments', 'flow']
    list_display_links = ['id', 'organization', 'date', 'outflow_amount', 'inflow_amount', 'currency', 'calculation',
                          'counterparty', 'item', 'project', 'comments', 'flow']
    search_fields = ['organization', 'date', 'counterparty', 'currency', 'item', 'project']


class CalculationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type_calc', 'flow', 'organization', 'date_first', 'amount', 'currency', 'is_cash',
                    'frequency', 'loan_rate', 'term', 'counterparty', 'item', 'project',  'comments']
    list_display_links = ['id', 'name', 'type_calc', 'flow', 'organization', 'date_first', 'amount', 'currency',
                          'is_cash', 'frequency', 'loan_rate', 'term', 'counterparty', 'item', 'project', 'comments']

    search_fields = ['name', 'type_calc', 'organization', 'counterparty', 'item', 'project']


admin.site.register(Calculations, CalculationsAdmin)
admin.site.register(PaymentDocumentPlan, PaymentDocumentPlanAdmin)
