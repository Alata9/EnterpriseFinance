from django.urls import path

from payments.view_plan import (
    PaymentsPlanView, PaymentsPlanIdView, PaymentsPlanDeleteView, PaymentsPlanUploadFileView, PaymentsPlanSeriesView
)
from payments.views import (
    ExpensesGroupView, ExpensesGroupIdView, ExpensesGroupDeleteView,
    ExpensesItemView, ExpensesItemIdView, ExpensesItemDeleteView,
    PaymentsView, PaymentsIdView, PaymentsDeleteView, UploadFileView
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


    path('payments/', PaymentsView.as_view(), name='payments'),
    path('payments/list', PaymentsView.htmx_list, name='payments_list'),
    path('payments/<int:pk>', PaymentsIdView.as_view(), name='payments_id'),
    path('payments/add/', PaymentsIdView.as_view(), name='payments_add'),
    path('payments/copy/<int:from_pk>', PaymentsIdView.as_view(), name='payments_copy'),
    path('<int:pk>/payments_delete', PaymentsDeleteView.as_view(), name='payments_delete'),
    path('payments/upload_file', UploadFileView.as_view(), name='upload_file'),
    path('payments/accounts', PaymentsIdView.htmx_accounts, name='payments_accounts'),
    path('payments/projects', PaymentsIdView.htmx_projects, name='payments_projects'),

    path('payments_plan/', PaymentsPlanView.as_view(), name='payments_plan'),
    path('payments_plan/list', PaymentsPlanView.htmx_list, name='payments_plan_list'),
    path('payments_plan/<int:pk>', PaymentsPlanIdView.as_view(), name='payments_plan_id'),
    path('payments_plan/add/', PaymentsPlanIdView.as_view(), name='payments_plan_add'),
    path('payments_plan/series/', PaymentsPlanSeriesView.as_view(), name='payments_plan_series'),
    # path('payments_plan/credit/', PaymentsPlanSeriesView.as_view(), name='payments_plan_credit'),
    path('payments_plan/copy/<int:from_pk>', PaymentsPlanIdView.as_view(), name='payments_plan_copy'),
    path('payments_plan/to_fact/<int:pk_fact>', PaymentsPlanIdView.as_view(), name='payments_plan_to_fact'),
    path('<int:pk>/payments_plan_delete', PaymentsPlanDeleteView.as_view(), name='payments_plan_delete'),
    path('payments_plan/upload_file', PaymentsPlanUploadFileView.as_view(), name='payments_plan_upload_file'),
    path('payments_plan/projects', PaymentsPlanIdView.htmx_projects, name='payments_plan_projects'),
    path('payments_plan/series/projects', PaymentsPlanSeriesView.htmx_projects, name='payments_plan_series_projects'),



]

