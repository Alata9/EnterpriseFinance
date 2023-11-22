from django.urls import path

from payments.views import (
    ReceiptsView, ReceiptsIdView, ReceiptsDeleteView, UploadFileReceiptView,
    ChangePayAccountDeleteView, ChangePayAccountView, ChangePayAccountIdView,
    PaymentsView, PaymentsIdView, PaymentsDeleteView, UploadFilePaymentView,
)

urlpatterns = [
    path('receipts/<int:pk>', ReceiptsIdView.as_view(), name='receipts_id'),
    path('receipts/add/', ReceiptsIdView.as_view(), name='receipts_add'),
    path('receipts/add/<int:plan_id>', ReceiptsIdView.as_view(), name='receipts_add_plan'),
    path('receipts/copy/<int:from_pk>', ReceiptsIdView.as_view(), name='receipts_copy'),
    path('receipts/', ReceiptsView.as_view(), name='receipts'),
    path('<int:pk>/receipts_delete', ReceiptsDeleteView.as_view(), name='receipts_delete'),
    path('receipts/accounts', ReceiptsIdView.htmx_accounts, name='receipts_accounts'),
    path('receipts/projects', ReceiptsIdView.htmx_projects, name='receipts_projects'),
    path('receipts/list', ReceiptsView.htmx_list, name='receipts_list'),
    path('receipts/upload_file', UploadFileReceiptView.as_view(), name='upload_file_rec'),

    path('payments/', PaymentsView.as_view(), name='payments'),
    path('payments/list', PaymentsView.htmx_list, name='payments_list'),
    path('payments/<int:pk>', PaymentsIdView.as_view(), name='payments_id'),
    path('payments/add/', PaymentsIdView.as_view(), name='payments_add'),
    path('payments/add/<int:plan_id>', PaymentsIdView.as_view(), name='payments_add_plan'),
    path('payments/copy/<int:from_pk>', PaymentsIdView.as_view(), name='payments_copy'),
    path('<int:pk>/payments_delete', PaymentsDeleteView.as_view(), name='payments_delete'),
    path('payments/upload_file', UploadFilePaymentView.as_view(), name='upload_file_pay'),
    path('payments/accounts', PaymentsIdView.htmx_accounts, name='payments_accounts'),
    path('payments/projects', PaymentsIdView.htmx_projects, name='payments_projects'),

    path('change_payaccount/<int:pk>', ChangePayAccountIdView.as_view(), name='change_payaccount_id'),
    path('change_payaccount/add/', ChangePayAccountIdView.as_view(), name='change_payaccount_add'),
    path('change_payaccount/copy/<int:from_pk>', ChangePayAccountIdView.as_view(), name='change_payaccount_copy'),
    path('change_payaccounts/', ChangePayAccountView.as_view(), name='change_payaccounts'),
    path('change_payaccounts/accounts', ChangePayAccountIdView.htmx_account1, name='change_payaccounts_account'),
    path('change_payaccount/list', ChangePayAccountView.htmx_list, name='change_payaccount_list'),
    path('<int:pk>/change_payaccount_delete', ChangePayAccountDeleteView.as_view(), name='change_payaccount_delete'),

]
