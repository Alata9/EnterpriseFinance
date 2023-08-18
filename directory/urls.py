from django.urls import path

from directory.views import (
    CounterpartiesView,
    CounterpartyDeleteView,
    CounterpartyIdView,
    OrganizationIdView,
    OrganizationsView,
    ProjectsView,
    PaymentAccountsView,
    CurrenciesView,
)

urlpatterns = [
    path('counterparties/', CounterpartiesView, name='counterparties'),
    path('counterparty_id/', CounterpartyIdView, name='counterparty_id'),
    path('<int:pk>/counterparty_del/', CounterpartyDeleteView.as_view(), name='counterparty_del'),


    path('organization/<int:pk>', OrganizationIdView, name='organization_id'),
    path('organization_add/', OrganizationIdView, name='organization_add'),
    path('organizations/', OrganizationsView, name='organizations'),

    path('projects/', ProjectsView, name='projects'),

    path('payment_accounts/', PaymentAccountsView, name='payment_accounts'),

    path('currencies/', CurrenciesView, name='currencies'),
]
