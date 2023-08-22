from django.urls import path

from registers.views import HomeView, RatesView, DashboardView, ReportsView, AccountSettingsView, AccountBalancesView

urlpatterns = [
    path('', HomeView, name='home'),
    path('rates/', RatesView, name='rates'),
    path('dashboard/', DashboardView, name='dashboard'),

    path('reports/', ReportsView, name='reports'),
    path('account_balances/', AccountBalancesView, name='account_balances'),

    path('settings/', AccountSettingsView.as_view(), name='settings'),
]
