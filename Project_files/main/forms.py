from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import Fryzjer
from main.models import Klient


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class RegisterFormKlient(forms.ModelForm):
    class Meta:
        model = Klient
        fields = ('nr_telefonu', 'ulica', 'miasto', 'nr_domu', 'kod_pocztowy')

class FryzjerUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Fryzjer
        fields = ('imie', 'nazwisko', 'email', 'ulica', 'nr_domu', 'miasto', 'kod_pocztowy' )