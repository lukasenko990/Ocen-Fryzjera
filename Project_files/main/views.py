from django.contrib.auth import logout as django_logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm,  RegisterFormKlient, RegisterFormFryzjer, FryzjerUpdateForm, KlientUpdateForm, SalonUpdateForm
from .models import Salon, Fryzjer, Klient
from django.contrib.auth.models import User
from django.db.models import Q


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

def barber_register(request):
    form = RegisterForm()
    form2 = RegisterFormFryzjer()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = RegisterFormFryzjer(request.POST)
        if form.is_valid() and form2.is_valid():
            user = User()
            user.username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.password = form.cleaned_data.get('password1')
            user.save()
            fryzjer = Fryzjer()
            fryzjer.user = user
            fryzjer.imie = form.cleaned_data.get('first_name')
            fryzjer.nazwisko = form.cleaned_data.get('last_name')
            fryzjer.ulica = form2.cleaned_data.get('ulica')
            fryzjer.nr_domu = form2.cleaned_data.get('nr_domu')
            fryzjer.miasto = form2.cleaned_data.get('miasto')
            fryzjer.kod_pocztowy = form2.cleaned_data.get('kod_pocztowy')
            fryzjer.save()
            username = request.POST.get('username')
            password = request.POST.get('password')
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.info(request, 'Invalid registration!!!')
            return render(request, 'main/barber_register.html', {"form": form, "form2":form2})

    return render(request, 'main/barber_register.html', {"form": form, "form2":form2})


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
    fryzjerzy = salon.fryzjer.all()
    wlasciciel = salon.wlasciciel
    context = {
        'salon': salon,
        'fryzjerzy': fryzjerzy,
        'wlasciciel': wlasciciel,
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

def edytuj_fryzjera(request, id):
    context = {}
    profile = Fryzjer.objects.all().filter(id=id).first()
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


def edytuj_klienta(request, id):
    context = {}
    profile = Klient.objects.all().filter(id=id).first()
    ClientForm = KlientUpdateForm(instance=profile)
    if request.method == 'POST':
        ClientForm = KlientUpdateForm(request.POST, instance=profile)
        if ClientForm.is_valid():
            ClientForm.save()
        return redirect('/')
    context = {
        'profile': profile,
        'ClientForm': ClientForm,
    }
    return render(request, 'main/edytuj_klienta.html', context)


def edytuj_salon(request, id):
    context = {}
    profile = Salon.objects.all().filter(id=id).first()
    SalonForm = SalonUpdateForm(instance=profile)
    if request.method == 'POST':
        SalonForm = SalonUpdateForm(request.POST, instance=profile)
        if SalonForm.is_valid():
            SalonForm.save()
        return redirect('/')
    context = {
        'profile': profile,
        'SalonForm': SalonForm,
    }
    return render(request, 'main/edytuj_salon.html', context)

def search(request):
    if request.method == "GET":
        searched = request.GET['searched']
        if " " in searched:
            searched_split=searched.split()
            fryzjerzy = Fryzjer.objects.filter(Q(imie__contains=searched_split[0]) | Q(nazwisko__contains=searched_split[0]) |
                                               Q(imie__contains=searched_split[1]) | Q(nazwisko__contains=searched_split[1]))
        else:
            fryzjerzy = Fryzjer.objects.filter(Q(imie__contains=searched) | Q(nazwisko__contains=searched))
        salony = Salon.objects.filter(Q(nazwa__contains=searched))
        return render(request, 'main/search.html', {'searched':searched, 'fryzjerzy':fryzjerzy, 'salony':salony})
    else:
        return render(request, 'main/search.html', {})
