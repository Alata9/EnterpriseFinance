from django.urls import path

from receipts.view_plan import ReceiptsPlanIdView, ReceiptsPlanDeleteView, ReceiptsPlanUploadFileView, ReceiptsPlanView
from receipts.views import (
    IncomeGroupView, IncomeGroupIdView, IncomeGroupDeleteView,
    IncomeItemView, IncomeItemIdView, IncomeItemDeleteView,
    ReceiptsView, ReceiptsIdView, ReceiptsDeleteView,
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

    path('receipts_plan/', ReceiptsPlanView.as_view(), name='receipts_plan'),
    path('receipts_plan/<int:pk>', ReceiptsPlanIdView.as_view(), name='receipts_plan_id'),
    path('receipts_plan/add/', ReceiptsPlanIdView.as_view(), name='receipts_plan_add'),
    path('receipts_plan/copy/<int:from_pk>', ReceiptsPlanIdView.as_view(), name='receipts_plan_copy'),
    path('<int:pk>/receipts_plan_delete', ReceiptsPlanDeleteView.as_view(), name='receipts_plan_delete'),
    path('receipts_plan/projects', ReceiptsPlanIdView.htmx_projects, name='receipts_plan_projects'),
    path('receipts_plan/list', ReceiptsPlanView.htmx_list, name='receipts_plan_list'),
    path('receipts_plan/receipts_plan_upload_file', ReceiptsPlanUploadFileView.as_view(), name='receipts_plan_upload_file'),

]
