from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeView, name='home'),
    path('rates/', RatesView, name='rates'),
    path('dashboard/', DashboardView, name='dashboard'),
    path('reports/', ReportsView, name='reports'),
    path('settings/', AccountSettingsView, name='settings'),
    ]
