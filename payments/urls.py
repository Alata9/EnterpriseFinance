from django.urls import path

from payments.views import (
    ExpensesGroupView, ExpensesGroupIdView, ExpensesGroupDeleteView,
    ExpensesItemView, ExpensesItemIdView, ExpensesItemDeleteView,
    PaymentsView, PaymentsIdView, PaymentsDeleteView,
    PaymentsPlanView,
    UploadFileView
)

urlpatterns = [
    path('expenses_groups/', ExpensesGroupView, name='expenses_group'),
    path('expenses_group/<int:pk>/', ExpensesGroupIdView.as_view(), name='expenses_group_id'),
    path('expenses_group/add/', ExpensesGroupIdView.as_view(), name='expenses_group_add'),
    path('<int:pk>/expenses_group/delete/', ExpensesGroupDeleteView.as_view(), name='expenses_group_delete'),

    path('expenses_items/', ExpensesItemView, name='expenses_items'),
    path('expenses_item/<int:pk>/', ExpensesItemIdView.as_view(), name='expenses_item_id'),
    path('expenses_item/add/', ExpensesItemIdView.as_view(), name='expenses_item_add'),
    path('<int:pk>/expenses_item/delete', ExpensesItemDeleteView.as_view(), name='expenses_item_delete'),

    path('payments/<int:pk>', PaymentsIdView.as_view(), name='payments_id'),
    path('payments/add/', PaymentsIdView.as_view(), name='payments_add'),
    path('payments/copy/<int:from_pk>', PaymentsIdView.as_view(), name='payments_copy'),
    path('payments/list', PaymentsView.htmx_list, name='payments_list'),
    path('payments/', PaymentsView.as_view(), name='payments'),

    path('<int:pk>/payments_delete', PaymentsDeleteView.as_view(), name='payments_delete'),
    path('payments/accounts', PaymentsIdView.htmx_accounts, name='payments_accounts'),
    path('payments/projects', PaymentsIdView.htmx_projects, name='payments_projects'),
    path('receipts/upload_file', UploadFileView.as_view(), name='upload_file'),

    path('payments_plan/', PaymentsPlanView, name='payments_plan'),
]

