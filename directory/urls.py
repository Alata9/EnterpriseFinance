from django.urls import path

from directory.views import (
    CounterpartiesView, CounterpartyDeleteView, CounterpartyIdView,
    OrganizationIdView, OrganizationsView, OrganizationDeleteView,
    ProjectsView, ProjectsIdView, ProjectDeleteView,
    PaymentAccountsView, PaymentAccountIdView, PaymentAccountDeleteView,
    CurrenciesView, CurrenciesIdView, CurrencyDeleteView,
)

urlpatterns = [
    path('counterparties/', CounterpartiesView, name='counterparties'),
    path('counterparty_id/', CounterpartyIdView, name='counterparty_id'),
    path('<int:pk>/counterparty_del/', CounterpartyDeleteView.as_view(), name='counterparty_del'),

    path('organization/<int:pk>', OrganizationIdView, name='organization_id'),
    path('organizations/', OrganizationsView, name='organizations'),
    path('organization_add/', OrganizationIdView, name='organization_add'),
    path('<int:pk>/organization_del/', OrganizationDeleteView.as_view(), name='organization_del'),

    path('projects/', ProjectsView, name='projects'),
    path('projects_add/', ProjectsIdView, name='projects_add'),
    path('<int:pk>/project_del/', ProjectDeleteView.as_view(), name='project_del'),

    path('payment_accounts/', PaymentAccountsView, name='payment_accounts'),
    path('payment_accounts_add/', PaymentAccountIdView, name='payment_accounts_add'),
    path('<int:pk>/payment_account_del/', PaymentAccountDeleteView.as_view(), name='payment_account_del'),

    path('currencies/', CurrenciesView, name='currencies'),
    path('currency_add/', CurrenciesIdView, name='currency_add'),
    path('<int:pk>/currency_del/', CurrencyDeleteView.as_view(), name='currency_del'),
]
