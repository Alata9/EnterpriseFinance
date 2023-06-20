from django.urls import path

from .views import *

urlpatterns = [
    path('expenses_group/', ExpensesGroupView, name='expenses_group'),
    path('expenses_item/', ExpensesItemView, name='expenses_item'),
    path('payments_plan/', PaymentsPlanView, name='payments_plan'),
    path('payments/', PaymentsView, name='payments'),
    ]