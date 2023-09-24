from django.urls import path


from registers.views import (
    HomeView,  AccountSettingsView,
    ReportsView, AccountBalancesView, CfStatementView, CfBudgetView, PlanFactAnalysisView,
    DashboardView, ChartsOperView, ChartsInvestView, ChartsFinView
)

urlpatterns = [
    path('', HomeView, name='home'),
    path('dashboard_main', DashboardView, name='dashboard'),
    path('operating', ChartsOperView, name='charts_oper'),
    path('investment', ChartsInvestView, name='charts_invest'),
    path('financing', ChartsFinView, name='charts_fin'),
    path('settings/', AccountSettingsView.as_view(), name='settings'),
    path('reports/', ReportsView, name='reports'),
    path('account_balances/', AccountBalancesView, name='account_balances'),
    path('cf_statement/', CfStatementView, name='cf_statement'),
    path('cf_budget/', CfBudgetView, name='cf_budget'),
    path('plan_fact_analysis/', PlanFactAnalysisView, name='plan_fact_analysis'),


]

