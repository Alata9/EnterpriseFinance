from django.urls import path

from directory.views import (
    CounterpartiesView, CounterpartyDeleteView, CounterpartyIdView,
    OrganizationsView, OrganizationAddView, OrganizationIdView, OrganizationDeleteView,
    ProjectsView, ProjectsIdView, ProjectDeleteView,
    PaymentAccountsView, PaymentAccountIdView, PaymentAccountDeleteView,
    CurrenciesView, CurrenciesIdView, CurrencyDeleteView,
    RatesView, RatesIdView, RatesDeleteView, RatesParsingView,
    InitialDebtsView, InitialDebtIdView, InitialDebtDeleteView,
    ItemIdView, ItemsView, ItemDeleteView,

    # ---------for delete----------------------------
    ExpensesGroupView, ExpensesGroupIdView, ExpensesGroupDeleteView,
    ExpensesItemView, ExpensesItemIdView, ExpensesItemDeleteView,
    IncomeGroupView, IncomeGroupIdView, IncomeGroupDeleteView,
    IncomeItemView, IncomeItemIdView, IncomeItemDeleteView,
)


urlpatterns = [
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

    path('counterparties/', CounterpartiesView, name='counterparties'),
    path('counterparty/<int:pk>/', CounterpartyIdView.as_view(), name='counterparty_id'),
    path('counterparty/add/', CounterpartyIdView.as_view(), name='counterparty_add'),
    path('<int:pk>/counterparty/delete/', CounterpartyDeleteView.as_view(), name='counterparty_del'),

    path('initial_debts/', InitialDebtsView.as_view(), name='initial_debts'),
    path('initial_debt/<int:pk>/', InitialDebtIdView.as_view(), name='initial_debt_id'),
    path('initial_debt/add/', InitialDebtIdView.as_view(), name='initial_debt_add'),
    path('initial_debts/list', InitialDebtsView.htmx_list, name='initial_debts_list'),
    path('<int:pk>/initial_debt/delete/', InitialDebtDeleteView.as_view(), name='initial_debt_del'),

    path('currencies/', CurrenciesView, name='currencies'),
    path('currency/<int:pk>/', CurrenciesIdView.as_view(), name='currency_id'),
    path('currency/add/', CurrenciesIdView.as_view(), name='currency_add'),
    path('<int:pk>/currency/delete/', CurrencyDeleteView.as_view(), name='currency_del'),

    path('rates/', RatesView.as_view(), name='rates'),
    path('rates/<int:pk>/', RatesIdView.as_view(), name='rate_id'),
    path('rates/add', RatesIdView.as_view(), name='rate_add'),
    path('rates/list', RatesView.htmx_list, name='rate_list'),
    path('rates/copy/<int:from_pk>', RatesIdView.as_view(), name='rate_copy'),
    path('rates/import', RatesParsingView.as_view(), name='rates_parsing'),
    path('<int:pk>/rates/delete', RatesDeleteView.as_view(), name='rate_del'),

    path('items/', ItemsView.as_view(), name='items'),
    path('item/<int:pk>', ItemIdView.as_view(), name='item_id'),
    path('item/add', ItemIdView.as_view(), name='item_add'),
    path('items/list', ItemsView.htmx_list, name='items_list'),
    path('<int:pk>/item/delete', ItemDeleteView.as_view(), name='item_del'),


#----------------for delete------------------------------

    path('expenses_groups/', ExpensesGroupView, name='expenses_group'),
    path('expenses_group/<int:pk>/', ExpensesGroupIdView.as_view(), name='expenses_group_id'),
    path('expenses_group/add/', ExpensesGroupIdView.as_view(), name='expenses_group_add'),
    path('<int:pk>/expenses_group/delete/', ExpensesGroupDeleteView.as_view(), name='expenses_group_delete'),

    path('expenses_items/', ExpensesItemView, name='expenses_items'),
    path('expenses_item/<int:pk>/', ExpensesItemIdView.as_view(), name='expenses_item_id'),
    path('expenses_item/add/', ExpensesItemIdView.as_view(), name='expenses_item_add'),
    path('<int:pk>/expenses_item/delete', ExpensesItemDeleteView.as_view(), name='expenses_item_delete'),

    path('income_groups/', IncomeGroupView, name='income_groups'),
    path('income_group/<int:pk>', IncomeGroupIdView.as_view(), name='income_group_id'),
    path('income_group/add', IncomeGroupIdView.as_view(), name='income_group_add'),
    path('<int:pk>/income_group/delete', IncomeGroupDeleteView.as_view(), name='income_group_delete'),

    path('income_items/', IncomeItemView, name='income_items'),
    path('income_item/<int:pk>', IncomeItemIdView.as_view(), name='income_item_id'),
    path('income_item/add', IncomeItemIdView.as_view(), name='income_item_add'),
    path('<int:pk>/income_item/delete', IncomeItemDeleteView.as_view(), name='income_item_delete'),

]
