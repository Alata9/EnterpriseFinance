from django.urls import path

from .views import *

urlpatterns = [
    path('income_group/', IncomeGroupView, name='income_group'),
    path('income_item/', IncomeItemView, name='income_item'),
    path('<int:pk>/income_item_delete', IncomeItemDeleteView.as_view(), name='income_item_delete'),
    path('receipts_id/<int:pk>', ReceiptsIdView.as_view(), name='receipts_id'),
    path('receipts_add/', ReceiptsAddView, name='receipts_add'),
    path('receipts_plan/', ReceiptsPlanView, name='receipts_plan'),
    path('receipts/', ReceiptsView, name='receipts'),
    path('<int:pk>/receipts_delete', ReceiptsDeleteView.as_view(), name='receipts_delete'),
    ]