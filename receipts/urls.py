from django.urls import path

from receipts.views import (
    IncomeGroupView, IncomeGroupIdView, IncomeGroupDeleteView,
    IncomeItemView, IncomeItemIdView, IncomeItemDeleteView,
    ReceiptsView, ReceiptsIdView, ReceiptsDeleteView,
    ReceiptsPlanView,
    UploadFileView,
)

urlpatterns = [
    path('income_groups/', IncomeGroupView, name='income_groups'),
    path('income_group/<int:pk>', IncomeGroupIdView.as_view(), name='income_group_id'),
    path('income_group/add', IncomeGroupIdView.as_view(), name='income_group_add'),
    path('<int:pk>/income_group/delete', IncomeGroupDeleteView.as_view(), name='income_group_delete'),

    path('income_items/', IncomeItemView, name='income_items'),
    path('income_item/<int:pk>', IncomeItemIdView.as_view(), name='income_item_id'),
    path('income_item/add', IncomeItemIdView.as_view(), name='income_item_add'),
    path('<int:pk>/income_item/delete', IncomeItemDeleteView.as_view(), name='income_item_delete'),

    path('receipts/<int:pk>', ReceiptsIdView.as_view(), name='receipts_id'),
    path('receipts/add/', ReceiptsIdView.as_view(), name='receipts_add'),
    path('receipts/copy/<int:from_pk>', ReceiptsIdView.as_view(), name='receipts_copy'),
    path('receipts/', ReceiptsView.as_view(), name='receipts'),

    path('<int:pk>/receipts_delete', ReceiptsDeleteView.as_view(), name='receipts_delete'),
    path('receipts/accounts', ReceiptsIdView.htmx_accounts, name='receipts_accounts'),
    path('receipts/projects', ReceiptsIdView.htmx_projects, name='receipts_projects'),
    path('receipts/list', ReceiptsView.htmx_list, name='receipts_list'),
    path('receipts/upload_file', UploadFileView.as_view(), name='upload_file'),

    path('receipts_plan/', ReceiptsPlanView, name='receipts_plan'),

]
