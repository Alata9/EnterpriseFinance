from django.urls import path

from .views import *

urlpatterns = [
    path('counterparties/', CounterpartiesView, name='counterparties'),
    path('organizations/', OrganizationsView, name='organizations'),
    path('projects/', ProjectsView, name='projects'),
    path('payment_accounts/', PaymentAccountsView, name='payment_accounts'),
    path('currencies/', CurrenciesView, name='currencies'),

    ]
