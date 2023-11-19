from django.urls import path

from planning.views import (
    PaymentsPlanView, PaymentsPlanIdView, PaymentsPlanDeleteView, PaymentsPlanUploadFileView,
    ReceiptsPlanView, ReceiptsPlanIdView, ReceiptsPlanDeleteView, ReceiptsPlanUploadFileView,
    CalculationView, CalculationIdView, CalculationDeleteView, CalculationPlanDeleteView
)

urlpatterns = [
    path('payments_plan/', PaymentsPlanView.as_view(), name='payments_plan'),
    path('payments_plan/list', PaymentsPlanView.htmx_list, name='payments_plan_list'),
    path('payments_plan/<int:pk>', PaymentsPlanIdView.as_view(), name='payments_plan_id'),
    path('payments_plan/add/', PaymentsPlanIdView.as_view(), name='payments_plan_add'),
    path('payments_plan/copy/<int:from_pk>', PaymentsPlanIdView.as_view(), name='payments_plan_copy'),
    path('payments_plan/to_fact/<int:pk_fact>', PaymentsPlanIdView.as_view(), name='payments_plan_to_fact'),
    path('<int:pk>/payments_plan_delete', PaymentsPlanDeleteView.as_view(), name='payments_plan_delete'),
    path('payments_plan/upload_file', PaymentsPlanUploadFileView.as_view(), name='payments_plan_upload_file'),
    path('payments_plan/projects', PaymentsPlanIdView.htmx_projects, name='payments_plan_projects'),

    path('calculations/', CalculationView.as_view(), name='calculations'),
    path('calculations/list', CalculationView.htmx_list, name='calculations_list'),
    path('calculations/projects', CalculationIdView.htmx_projects, name='calculations_projects'),
    path('calculation/delete_plan/<int:pk>', CalculationPlanDeleteView.as_view(), name='calculation_delete_plan'),
    path('calculation/<int:pk>/list', CalculationIdView.htmx_list, name='calculations_id_list'),
    path('calculation/<int:calc_pk>/create_plan', CalculationIdView.as_view(), name='calculation_create_plan'),
    path('calculation/<int:pk>', CalculationIdView.as_view(), name='calculation_id'),
    path('calculation/add', CalculationIdView.as_view(), name='calculation_add'),
    path('calculation/copy/<int:from_pk>', CalculationIdView.as_view(), name='calculation_copy'),
    path('<int:pk>/calculation_delete', CalculationDeleteView.as_view(), name='calculation_delete'),

    path('receipts_plan/', ReceiptsPlanView.as_view(), name='receipts_plan'),
    path('receipts_plan/<int:pk>', ReceiptsPlanIdView.as_view(), name='receipts_plan_id'),
    path('receipts_plan/add/', ReceiptsPlanIdView.as_view(), name='receipts_plan_add'),
    path('receipts_plan/copy/<int:from_pk>', ReceiptsPlanIdView.as_view(), name='receipts_plan_copy'),
    path('<int:pk>/receipts_plan_delete', ReceiptsPlanDeleteView.as_view(), name='receipts_plan_delete'),
    path('receipts_plan/projects', ReceiptsPlanIdView.htmx_projects, name='receipts_plan_projects'),
    path('receipts_plan/list', ReceiptsPlanView.htmx_list, name='receipts_plan_list'),
    path('receipts_plan/receipts_plan_upload_file', ReceiptsPlanUploadFileView.as_view(), name='receipts_plan_upload_file'),

]

