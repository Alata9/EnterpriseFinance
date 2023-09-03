from django.urls import path

from directory.views import (
    CounterpartiesView, CounterpartyDeleteView, CounterpartyIdView,
    OrganizationsView, OrganizationAddView, OrganizationIdView, OrganizationDeleteView,
    ProjectsView, ProjectsIdView, ProjectDeleteView,
    PaymentAccountsView, PaymentAccountIdView, PaymentAccountDeleteView,
    CurrenciesView, CurrenciesIdView, CurrencyDeleteView, RatesView, RatesIdView, RatesDeleteView,
)

urlpatterns = [
    path('counterparties/', CounterpartiesView, name='counterparties'),
    path('counterparty/<int:pk>/', CounterpartyIdView.as_view(), name='counterparty_id'),
    path('counterparty/add/', CounterpartyIdView.as_view(), name='counterparty_add'),
    path('<int:pk>/counterparty/delete/', CounterpartyDeleteView.as_view(), name='counterparty_del'),

    path('organizations/', OrganizationsView, name='organizations'),
    path('organization/<int:pk>', OrganizationIdView, name='organization_id'),
    path('organization/add/', OrganizationAddView, name='organization_add'),
    path('<int:pk>/organization/delete/', OrganizationDeleteView.as_view(), name='organization_del'),

    path('projects/', ProjectsView, name='projects'),
    path('project/<int:pk>/', ProjectsIdView.as_view(), name='project_id'),
    path('project/add/', ProjectsIdView.as_view(), name='project_add'),
    path('<int:pk>/project/delete/', ProjectDeleteView.as_view(), name='project_del'),

    path('payment_accounts/', PaymentAccountsView, name='payment_accounts'),
    path('payment_account/<int:pk>/', PaymentAccountIdView.as_view(), name='payment_account_id'),
    path('payment_account/add/', PaymentAccountIdView.as_view(), name='payment_account_add'),
    path('<int:pk>/payment_account/delete/', PaymentAccountDeleteView.as_view(), name='payment_account_del'),

    path('currencies/', CurrenciesView, name='currencies'),
    path('currency/<int:pk>/', CurrenciesIdView.as_view(), name='currency_id'),
    path('currency/add/', CurrenciesIdView.as_view(), name='currency_add'),
    path('<int:pk>/currency/delete/', CurrencyDeleteView.as_view(), name='currency_del'),

    path('rates/', RatesView, name='rates'),
    path('rates/<int:pk>/', RatesIdView.as_view(), name='rate_id'),
    path('rates/add', RatesIdView.as_view(), name='rate_add'),
    path('<int:pk>/rates/delete', RatesDeleteView.as_view(), name='rate_del'),

]
