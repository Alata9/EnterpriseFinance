from django.shortcuts import render, redirect

from registers.forms import *


def HomeView(request):
    return render(request, 'registers/home.html')

def RatesView(request):
    return render(request, 'registers/rates.html')

def ReportsView(request):
    return render(request, 'registers/reports.html')

def DashboardView(request):
    return render(request, 'registers/dashboard.html')

def AccountSettingsView(request):
    if request.method == 'POST':
        form = AccountSettingsSet(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('settings')
            except:
                form.add_error(None, 'Data save error')
    else:
        form = AccountSettingsSet()

    context = {'form': form}
    return render(request, 'registers/settings.html', context=context)
