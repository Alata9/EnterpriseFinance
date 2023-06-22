from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls, name='admin'),
    path('', include('registers.urls')),
    path('', include('payments.urls')),
    path('', include('receipts.urls')),
    # path('', include('users.urls')),
    path('', include('directory.urls')),

]
