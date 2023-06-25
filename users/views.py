from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, TemplateView, DeleteView
from users.forms import ChangeUserInfoForm, RegisterUserForm


# Вход пользователя на сайт
class UserLoginView(LoginView):
    template_name = 'users/login.html'


# Выход
class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'users/logout.html'


# Смена данных пользователя
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/personal_account.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('home')
    success_message = 'Personal data has been successfully changed'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


# Смена пароля
class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('home')
    success_message = 'User password changed successfully'


# Регистрация пользователя
class RegisterUserView(CreateView):
    model = User
    template_name = 'users/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'users/register_done.html'


# Удаление пользователя
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/profile_delete.html'
    success_url = reverse_lazy('home')


    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

