from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}), label='', required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), label='', required=True)

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'UserName'}), label='', required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Address'}), label='', required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='', required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'UserName'}), label='', required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='', required=True)
