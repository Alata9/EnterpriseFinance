from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.contenttypes import forms


# личные данные пользователя
class ChangeUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


# регистрация пользователя
class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')