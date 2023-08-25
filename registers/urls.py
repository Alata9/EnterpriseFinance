from django.urls import path

from registers.views import (
    HomeView, RatesView, DashboardView, AccountSettingsView,
    ReportsView,  AccountBalancesView, CfStatementView, CfBudgetView, PlanFactAnalysisView,
)

urlpatterns = [
    path('', HomeView, name='home'),
    path('rates/', RatesView, name='rates'),
    path('dashboard/', DashboardView, name='dashboard'),

    path('reports/', ReportsView, name='reports'),
    path('account_balances/', AccountBalancesView, name='account_balances'),
    path('cf_statement/', CfStatementView, name='cf_statement'),
    path('cf_budget/', CfBudgetView, name='cf_budget'),
    path('plan_fact_analysis/', PlanFactAnalysisView, name='plan_fact_analysis'),

    path('settings/', AccountSettingsView.as_view(), name='settings'),
]
