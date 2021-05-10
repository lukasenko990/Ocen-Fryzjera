from django.contrib.auth import logout as django_logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm,  RegisterFormKlient, RegisterFormFryzjer, FryzjerUpdateForm, KlientUpdateForm, SalonUpdateForm
from .models import Salon, Fryzjer, Klient, Usluga, Zamowienie
from django.contrib.auth.models import User
from django.db.models import Q
import json
import os


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
    user_klient = Klient.objects.all().filter(user=request.user).first()

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
    uslugi = Usluga.objects.all().filter(salon=salon)
    context = {
        'salon': salon,
        'fryzjerzy': fryzjerzy,
        'wlasciciel': wlasciciel,
        'uslugi': uslugi,
    }

    return render(request, 'main/pokaz_salon.html', context)
def pokaz_usluge(request, id):
    usluga = get_object_or_404(Usluga, id=id)
    context = {
        'usluga': usluga,
    }

    return render(request, 'main/pokaz_usluge.html', context)

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
    try:
        oldPath=profile.avatar.path
    except:
        oldPath=None
    EditForm = FryzjerUpdateForm(instance=profile)
    if request.method == 'POST':
        EditForm = FryzjerUpdateForm(request.POST, request.FILES, instance=profile)
        if EditForm.is_valid():
            request.FILES.get('avatar',None)
            if not oldPath==None:
                os.remove(oldPath)
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
    try:
        oldPath=profile.avatar.path
    except:
        oldPath=None
    ClientForm = KlientUpdateForm(instance=profile)
    if request.method == 'POST':
        ClientForm = KlientUpdateForm(request.POST, request.FILES, instance=profile)
        if ClientForm.is_valid():
            request.FILES.get('avatar',None)
            if not oldPath==None:
                os.remove(oldPath)
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

def umow_wizyte(request, id):
    usluga = get_object_or_404(Usluga, id=id)
    salon = usluga.salon.first()
    fryzjerzy = salon.fryzjer.all()
    wizyty = Zamowienie.objects.all().filter(salon=salon)
    uslugi = Usluga.objects.all().filter(salon=salon)
    zamowienia = []
    czasy=[]
    for wizyta in wizyty:
        date_time = wizyta.termin_uslugi.strftime("%Y-%m-%d %H:%M:%S")
        czas=Usluga.objects.all().filter(salon=salon, nazwa=wizyta.nazwa_zamowienia).first().max_czas
        zamowienia.append(date_time)
        czasy.append(czas)
    json_list = json.dumps(zamowienia)
    json_list2 = json.dumps(czasy)
    if request.method == "POST":
        wizyta = Zamowienie()
        wizyta.salon=salon
        wizyta.nazwa_zamowienia=usluga.nazwa
        wizyta.termin_uslugi=request.POST.get('date')
        wizyta.status='sent'
        wizyta.save()
        messages.info(request, 'Pomyslnie zapisano sie na wizyte')
        return redirect('/')
    context = {
        'usluga': usluga,
        'salon': salon,
        'fryzjerzy': fryzjerzy,
        'zamowienia': zamowienia,
        'czasy': czasy,
        'json_list':json_list,
        'json_list2':json_list2,
    }
    return render(request, 'main/umow_wizyte.html', context)


def dodaj_fryzjera(request):
    #salony = Salon.objects.all()
    fryzjer = Fryzjer.objects.get(user=request.user)
    salony = fryzjer.wlasciciel.filter()

    fryzjerzy = Fryzjer.objects.all()

    fryzjerID = request.POST.get('fryzjerSelect', False)
    salonID = request.POST.get('salonSelect', False)

    if salonID != False and fryzjerID != False:
        fryzjerToAdd = Fryzjer.objects.get(id=fryzjerID)
        salonToAdd = Salon.objects.get(id=salonID)

        #fryzjer.invite_sent.add(fryzjerToAdd)
        #fryzjerToAdd.invite_received.add(fryzjer)
        print(f"Fryzjer {fryzjer} wyslal zaproszenie do fryzjera {fryzjerToAdd} do salonu {salonToAdd}")

    context = {
        'salony': salony,
        'fryzjerzy': fryzjerzy,
    }

    return render(request, 'main/dodaj_fryzjera.html', context)

def akceptuj_zaproszenie(request):
    

def zaproszenia_do_salonu(request):
    fryzjer = Fryzjer.objects.get(user=request.user)
    received_invites = fryzjer.invite_received.all()

    context = {
        'received_invites': received_invites,
        'fryzjer': fryzjer,
    }

    return render(request, 'main/zaproszenia_do_salonu.html', context)