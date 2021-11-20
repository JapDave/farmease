from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from subadmin.models import SubAdmin


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class AdminForm(forms.ModelForm):
   
   class Meta:
      model = SubAdmin
      exclude = ['deleted_at']
      CHOICES = [('M','Male'),('F','Female')]
      widgets = {'gender':forms.RadioSelect(choices=CHOICES)}