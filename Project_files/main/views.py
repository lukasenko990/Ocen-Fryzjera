from django.contrib.auth import logout as django_logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, FryzjerUpdateForm
from .models import Salon, Fryzjer, Klient


# register, login, logout
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = request.POST.get('username')
            password = request.POST.get('password')
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.info(request, 'Invalid registration!!!')
            return render(request, 'main/register.html', {"form": form})

    return render(request, 'main/register.html', {"form": form})


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
    f_u = FryzjerUpdateForm()
    context = {
        'f_u': f_u,
    }
    return render(request, 'main/edytuj_fryzjera.html', context)