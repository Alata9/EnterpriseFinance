from django.urls import path

from receipts.views import (
    IncomeGroupView,
    IncomeItemView,
    IncomeItemDeleteView,
    ReceiptsIdView,
    ReceiptsView,
    ReceiptsPlanView,
    ReceiptsDeleteView,
)

urlpatterns = [
    path('income_group/', IncomeGroupView, name='income_group'),
    path('income_item/', IncomeItemView, name='income_item'),
    path('<int:pk>/income_item_delete', IncomeItemDeleteView.as_view(), name='income_item_delete'),
    path('receipts/<int:pk>', ReceiptsIdView.as_view(), name='receipts_id'),
    path('receipts/add/', ReceiptsIdView.as_view(), name='receipts_add'),
    path('receipts/', ReceiptsView, name='receipts'),
    path('receipts_plan/', ReceiptsPlanView, name='receipts_plan'),
    path('<int:pk>/receipts_delete', ReceiptsDeleteView.as_view(), name='receipts_delete'),
    path('receipts/accounts', ReceiptsIdView.htmx_accounts, name='receipts_accounts'),
    path('receipts/projects', ReceiptsIdView.htmx_projects, name='receipts_projects'),
]
