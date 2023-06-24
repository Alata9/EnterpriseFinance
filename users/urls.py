from django.urls import path

from .views import *

urlpatterns = [
    path('account/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('account/register/', RegisterUserView.as_view(), name='register'),
    path('account/login/', UserLoginView.as_view(), name='login'),
    path('account/logout/', UserLogoutView.as_view(), name='logout'),
    path('account/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('account/profile/', ChangeUserInfoView.as_view(), name='personal_account'),
    path('account/password/change/', UserPasswordChangeView.as_view(), name='password_change'),
    ]
