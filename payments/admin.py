from django.contrib import admin

from payments.models import ChangePayAccount, PaymentDocuments


class PaymentDocumentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'date', 'outflow_amount', 'inflow_amount', 'account', 'currency',
                    'counterparty', 'item', 'project', 'comments', 'flow']
    list_display_links = ['id', 'organization', 'date', 'outflow_amount', 'inflow_amount', 'account', 'currency',
                          'counterparty', 'item', 'project', 'comments', 'flow']
    search_fields = ['date', 'flow', 'organization', 'counterparty', 'account', 'currency', 'item', 'project']


class ChangePayAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'pay_account_from', 'pay_account_to', 'date', 'amount', 'currency']
    list_display_links = ['id', 'pay_account_from', 'pay_account_to', 'date', 'amount', 'currency']
    search_fields = ['pay_account_from', 'pay_account_to', 'date', 'amount', 'currency']


admin.site.register(PaymentDocuments, PaymentDocumentsAdmin)
admin.site.register(ChangePayAccount, ChangePayAccountAdmin)

