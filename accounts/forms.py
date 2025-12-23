from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django import forms

User = get_user_model()

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)

class JapaneseAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='ユーザーネーム',
        widget=forms.TextInput(attrs={'class' : 'form-control'})
    )
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
