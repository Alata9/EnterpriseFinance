from django.contrib import admin

from payments.models import Receipts, ChangePayAccount, Payments, PaymentDocuments


class PaymentDocumentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'date', 'outflow_amount', 'inflow_amount', 'account', 'currency',
                    'counterparty', 'item', 'project', 'comments', 'flow']
    list_display_links = ['id', 'organization', 'date', 'outflow_amount', 'inflow_amount', 'account', 'currency',
                          'counterparty', 'item', 'project', 'comments', 'flow']
    search_fields = ['flow', 'organization', 'date', 'counterparty', 'account', 'currency', 'item', 'project']


class ChangePayAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'pay_account_from', 'pay_account_to', 'date', 'amount', 'currency']
    list_display_links = ['id', 'pay_account_from', 'pay_account_to', 'date', 'amount', 'currency']
    search_fields = ['pay_account_from', 'pay_account_to', 'date', 'amount', 'currency']


admin.site.register(PaymentDocuments, PaymentDocumentsAdmin)
admin.site.register(ChangePayAccount, ChangePayAccountAdmin)


#------------for delete---------------

class ReceiptsAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'date', 'amount', 'account', 'currency',
                    'counterparty', 'item', 'project', 'comments']
    list_display_links = ['id', 'organization', 'date', 'amount', 'account', 'currency',
                          'counterparty', 'item', 'project', 'comments']
    search_fields = ['organization', 'date', 'counterparty', 'account', 'currency', 'item', 'project']

class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'date', 'amount', 'account', 'currency',
                    'counterparty', 'item', 'project', 'by_request', 'comments']
    list_display_links = ['id', 'organization', 'date', 'amount', 'account', 'currency',
                          'counterparty', 'item', 'project', 'by_request', 'comments']
    search_fields = ['organization', 'date', 'counterparty', 'account', 'item', 'project']



admin.site.register(Payments, PaymentsAdmin)
admin.site.register(Receipts, ReceiptsAdmin)