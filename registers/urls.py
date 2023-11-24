from django.urls import path

# from registers.views_charts import (htmx_projects,
#     # DashboardView, ChartsOperView, ChartsInvestView, ChartsFinView,
# )
from registers.views_charts import DashboardView, ChartsOperView, htmx_projects
from registers.views_reports import (HomeView, AccountSettingsView, AccountBalancesView, AccountFlowsView, CfBudgetView,
                                     PlanFactAnalysisView, CfStatementView, CounterpartyFlowsView
    # , CfStatementView, CfBudgetView, PlanFactAnalysisView,
                                     )

urlpatterns = [
    path('', HomeView, name='home'),
    path('settings/', AccountSettingsView.as_view(), name='settings'),

    path('account_balances/', AccountBalancesView.as_view(), name='account_balances'),
    path('account_balances/list', AccountBalancesView.htmx_list, name='account_balances_list'),

    path('account_flows/', AccountFlowsView.as_view(), name='account_flows'),
    path('account_flows/list', AccountFlowsView.htmx_list, name='account_flows_list'),

    path('counterparty_flows/', CounterpartyFlowsView.as_view(), name='counterparty_flows'),
    path('counterparty_flows/list', CounterpartyFlowsView.htmx_list, name='counterparty_flows_list'),

    path('dashboard_main', DashboardView.as_view(), name='dashboard'),
    # path('dashboard_main/cf_bar', DashboardView.cf_bar(), name='dashboard_cf_bar'),

    path('operating', ChartsOperView.as_view(), name='charts_oper'),
    path('operating/project', htmx_projects, name='operating_project'),
    # path('investment', ChartsInvestView, name='charts_invest'),
    # path('financing', ChartsFinView.as_view(), name='charts_fin'),
    #
    path('cf_statement/', CfStatementView, name='cf_statement'),
    # path('cf_statement/', CfStatementView.as_view(), name='cf_statement'),
    # path('cf_statement/list', CfStatementView.htmx_list, name='cf_statement_list'),
    path('cf_statement/projects', htmx_projects, name='cf_statement_projects'),

    path('cf_budget/', CfBudgetView.as_view(), name='cf_budget'),
    path('cf_budget/list', CfBudgetView.htmx_list, name='cf_budget_list'),
    path('plan_fact_analysis/', PlanFactAnalysisView, name='plan_fact_analysis'),

]

