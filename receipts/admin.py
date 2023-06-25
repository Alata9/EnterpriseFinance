from django.contrib import admin

from receipts.models import IncomeGroup, IncomeItem, Receipts, ReceiptsPlan


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
    list_display = ['id', 'organization', 'date', 'amount', 'account', 'currency',
                    'counterparty', 'item', 'project', 'comments']
    list_display_links = ['id', 'organization', 'date', 'amount', 'account', 'currency',
                          'counterparty', 'item', 'project', 'comments']
    search_fields = ['organization', 'date', 'counterparty', 'account', 'currency', 'item', 'project']


class ReceiptsPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'date', 'amount', 'currency', 'is_cash',
                    'counterparty', 'item', 'project', 'comments']
    list_display_links = ['id', 'organization', 'date', 'amount', 'currency', 'is_cash',
                          'counterparty', 'item', 'project', 'comments']
    search_fields = ['organization', 'date', 'counterparty', 'currency', 'item', 'project']


admin.site.register(IncomeGroup, IncomeGroupAdmin)
admin.site.register(IncomeItem, IncomeItemAdmin)
admin.site.register(Receipts, ReceiptsAdmin)
admin.site.register(ReceiptsPlan, ReceiptsPlanAdmin)
