from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView

from registers.forms import *


def HomeView(request):
    return render(request, 'registers/home.html')

def RatesView(request):
    return render(request, 'registers/rates.html')

def ReportsView(request):
    return render(request, 'registers/reports.html')

def DashboardView(request):
    return render(request, 'registers/dashboard.html')


class AccountSettingsView(UpdateView):
    model = AccountSettings
    template_name = 'registers/settings.html'
    form_class = AccountSettingsSet
    success_url = '/settings'

    def get_object(self):
        return self.model.load()

