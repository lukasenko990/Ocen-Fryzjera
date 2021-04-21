from django.contrib.auth import logout as django_logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, FryzjerUpdateForm, RegisterFormKlient
from .models import Salon, Fryzjer, Klient
from django.contrib.auth.models import User


# register, login, logout
def register(request):
    form = RegisterForm()
    form2 = RegisterFormKlient()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = RegisterFormKlient(request.POST)
        if form.is_valid() and form2.is_valid():
            user = User()
            user.username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.password = form.cleaned_data.get('password1')
            user.save()
            klient = Klient()
            klient.user = user
            klient.imie = form.cleaned_data.get('first_name')
            klient.nazwisko = form.cleaned_data.get('last_name')
            klient.nr_telefonu = form2.cleaned_data.get('nr_telefonu')
            klient.ulica = form2.cleaned_data.get('ulica')
            klient.nr_domu = form2.cleaned_data.get('nr_domu')
            klient.miasto = form2.cleaned_data.get('miasto')
            klient.kod_pocztowy = form2.cleaned_data.get('kod_pocztowy')
            klient.save()
            username = request.POST.get('username')
            password = request.POST.get('password')
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.info(request, 'Invalid registration!!!')
            return render(request, 'main/register.html', {"form": form, "form2":form2})

    return render(request, 'main/register.html', {"form": form, "form2":form2})

def register_barber(request):
    form = RegisterForm()
    form2 = RegisterFormKlient()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = RegisterFormKlient(request.POST)
        if form.is_valid() and form2.is_valid():
            user = User()
            user.username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.password = form.cleaned_data.get('password1')
            user.save()
            klient = Klient()
            klient.user = user
            klient.imie = form.cleaned_data.get('first_name')
            klient.nazwisko = form.cleaned_data.get('last_name')
            klient.nr_telefonu = form2.cleaned_data.get('nr_telefonu')
            klient.ulica = form2.cleaned_data.get('ulica')
            klient.nr_domu = form2.cleaned_data.get('nr_domu')
            klient.miasto = form2.cleaned_data.get('miasto')
            klient.kod_pocztowy = form2.cleaned_data.get('kod_pocztowy')
            klient.save()
            username = request.POST.get('username')
            password = request.POST.get('password')
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.info(request, 'Invalid registration!!!')
            return render(request, 'main/register.html', {"form": form, "form2":form2})

    return render(request, 'main/register.html', {"form": form, "form2":form2})


def logout(request):
    django_logout(request)
    return render(request, 'main/home.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.info(request, 'Invalid Login!!!')
            return render(request, 'main/login.html')
    else:
        return render(request, 'main/login.html')


########3 home
@login_required
def home(request):
    salony = Salon.objects.all()
    fryzjerzy = Fryzjer.objects.all()
    klienci = Klient.objects.all()
    user_klient = request.user.klient

    context = {
        'user_klient': user_klient,
        'salony': salony,
        'fryzjerzy': fryzjerzy,
        'klienci': klienci,
    }

    return render(request, 'main/home.html', context)


def pokaz_salon(request, id):
    salon = get_object_or_404(Salon, id=id)
    context = {
        'salon': salon,
    }

    return render(request, 'main/pokaz_salon.html', context)


def pokaz_klienta(request, id):
    klient = get_object_or_404(Klient, id=id)
    context = {
        'klient': klient,
    }

    return render(request, 'main/pokaz_klienta.html', context)


def pokaz_fryzjera(request, id):
    fryzjer = get_object_or_404(Fryzjer, id=id)
    context = {
        'fryzjer': fryzjer,
    }

    return render(request, 'main/pokaz_fryzjera.html', context)

def edytuj_fryzjera(request):
    context = {}
    profile = Fryzjer.objects.all().filter(user = request.user).first()
    EditForm = FryzjerUpdateForm(instance=profile)
    if request.method == 'POST':
        EditForm = FryzjerUpdateForm(request.POST, instance=profile)
        if EditForm.is_valid():
            EditForm.save()
        return redirect('/')
    context = {
        'profile': profile,
        'EditForm': EditForm,
    }
    return render(request, 'main/edytuj_fryzjera.html', context)
