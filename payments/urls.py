from django.urls import path

from payments.views import ExpensesGroupView, ExpensesItemView, PaymentsPlanView, PaymentsView, PaymentsIdView, \
    PaymentsDeleteView, ExpensesItemDeleteView, UploadFileView

urlpatterns = [
    path('expenses_group/', ExpensesGroupView, name='expenses_group'),
    path('expenses_item/', ExpensesItemView, name='expenses_item'),
    path('payments_plan/', PaymentsPlanView, name='payments_plan'),
    path('payments/<int:pk>', PaymentsIdView.as_view(), name='payments_id'),
    path('payments/add/', PaymentsIdView.as_view(), name='payments_add'),
    path('payments/copy/<int:from_pk>', PaymentsIdView.as_view(), name='payments_copy'),
    path('payments/list', PaymentsView.htmx_list, name='payments_list'),
    path('payments/', PaymentsView.as_view(), name='payments'),
    path('<int:pk>/expenses_item_delete', ExpensesItemDeleteView.as_view(), name='expenses_item_delete'),
    path('<int:pk>/payments_delete', PaymentsDeleteView.as_view(), name='payments_delete'),
    path('payments/accounts', PaymentsIdView.htmx_accounts, name='payments_accounts'),
    path('payments/projects', PaymentsIdView.htmx_projects, name='payments_projects'),
    path('receipts/upload_file', UploadFileView.as_view(), name='upload_file'),
]

