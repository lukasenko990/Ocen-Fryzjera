from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import Fryzjer
from main.models import Klient, Salon


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class RegisterFormKlient(forms.ModelForm):
    class Meta:
        model = Klient
        fields = ('nr_telefonu', 'ulica', 'miasto', 'nr_domu', 'kod_pocztowy')


class RegisterFormFryzjer(forms.ModelForm):
    class Meta:
        model = Fryzjer
        fields = ( 'ulica', 'miasto', 'nr_domu', 'kod_pocztowy')


class FryzjerUpdateForm(forms.ModelForm):
    #email = forms.EmailField()
    class Meta:
        model = Fryzjer
        fields = ('imie', 'nazwisko', 'ulica', 'nr_domu', 'miasto', 'kod_pocztowy', 'avatar')


class KlientUpdateForm(forms.ModelForm):
    class Meta:
        model = Klient
        fields = ('imie', 'nazwisko', 'nr_telefonu', 'ulica', 'nr_domu', 'miasto', 'kod_pocztowy', 'avatar')


class SalonUpdateForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = ('nazwa', 'NIP', 'regon', 'ulica', 'nr_lokalu', 'miasto', 'kod_pocztowy')


class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

