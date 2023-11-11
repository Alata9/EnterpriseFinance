from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls, name='admin'),
    path('', include('directory.urls')),
    path('', include('payments.urls')),
    path('', include('planning.urls')),
    path('', include('registers.urls')),
    path('', include('users.urls')),
]
