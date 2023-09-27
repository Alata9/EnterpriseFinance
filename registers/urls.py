from django.urls import path


from registers.views_charts import (
    DashboardView, ChartsOperView, ChartsInvestView, ChartsFinView, htmx_projects
)
from registers.views_reports import (
    HomeView, AccountSettingsView,
    AccountBalancesView, CfStatementView, CfBudgetView, PlanFactAnalysisView,
)

urlpatterns = [
    path('', HomeView, name='home'),
    path('settings/', AccountSettingsView.as_view(), name='settings'),

    path('dashboard_main', DashboardView, name='dashboard'),
    path('operating', ChartsOperView, name='charts_oper'),
    path('operating/project', htmx_projects, name='operating_project'),
    path('investment', ChartsInvestView, name='charts_invest'),
    path('financing', ChartsFinView, name='charts_fin'),

    path('account_balances/', AccountBalancesView.as_view(), name='account_balances'),
    path('account_balances/list', AccountBalancesView.htmx_list, name='account_balances_list'),

    path('cf_statement/', CfStatementView.as_view(), name='cf_statement'),
    path('cf_statement/list', CfStatementView.htmx_list, name='cf_statement_list'),
    path('cf_statement/projects', htmx_projects, name='cf_statement_projects'),

    path('cf_budget/', CfBudgetView, name='cf_budget'),
    path('plan_fact_analysis/', PlanFactAnalysisView, name='plan_fact_analysis'),




]

