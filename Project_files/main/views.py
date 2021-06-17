from django.contrib.auth import logout as django_logout, login, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm,  RegisterFormKlient, RegisterFormFryzjer, FryzjerUpdateForm, KlientUpdateForm, SalonUpdateForm, RateForm
from .models import Salon, Fryzjer, Klient, Usluga, Zamowienie, SalonRelationship, Ocena
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets
from .serializer import SalonSerializer, FryzjerSerializer, KlientSerializer, UslugaSerializer, ZamowienieSerializer
import json
import os
from additional.mapGenerator import generateMap
from PIL import Image

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
            user.set_password(user.password)
            user.email = form.cleaned_data.get('email')
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
            user.set_password(user.password)
            user.email = form.cleaned_data.get('email')
            user.save()
            fryzjer = Fryzjer()
            fryzjer.user = user
            fryzjer.imie = form.cleaned_data.get('first_name')
            fryzjer.nazwisko = form.cleaned_data.get('last_name')
            fryzjer.nr_tel = form.cleaned_data.get('nr_tel')
            fryzjer.bio = form.cleaned_data.get('bio')
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

def home(request):
    salony = Salon.objects.all()
    fryzjerzy = Fryzjer.objects.all()
    klienci = Klient.objects.all()
    if request.user.is_authenticated:
        user_klient = Klient.objects.all().filter(user=request.user).first()
        user_fryzjer=Fryzjer.objects.all().filter(user=request.user).first()
        user_wlasciciel=Salon.objects.all().filter(wlasciciel=user_fryzjer).first()
        context = {
            'user_klient': user_klient,
            'salony': salony,
            'fryzjerzy': fryzjerzy,
            'klienci': klienci,
            'user_fryzjer': user_fryzjer,
            'user_wlasciciel': user_wlasciciel
        }
    else:
        context = {
            'salony': salony,
            'fryzjerzy': fryzjerzy,
        }
    return render(request, 'main/home.html', context)

def pokaz_salon(request, id):
    salon = get_object_or_404(Salon, id=id)
    fryzjerzy = salon.fryzjer.all()
    wlasciciel = salon.wlasciciel
    uslugi = Usluga.objects.all().filter(salon=salon)
    mapObject = generateMap(salon.kod_pocztowy, \
                            salon.ulica, \
                            str(salon.nr_lokalu), \
                            "", \
                            salon.miasto, \
                            "")
    oceny = Ocena.objects.all().filter(salon=salon)
    if request.user.is_authenticated:
        zamowienia_klienta = Zamowienie.objects.all().filter(salon=salon).filter(klient=Klient.objects.all().filter(user=request.user).first())
    else:
        zamowienia_klienta=None
    context = {
        'salon': salon,
        'fryzjerzy': fryzjerzy,
        'wlasciciel': wlasciciel,
        'uslugi': uslugi,
        'mapObject': mapObject,
        'oceny': oceny,
        'zamowienia_klienta': zamowienia_klienta
    }

    return render(request, 'main/salon_default.html', context)
def pokaz_usluge(request, id):
    usluga = get_object_or_404(Usluga, id=id)
    context = {
        'usluga': usluga,
    }

    return render(request, 'main/pokaz_usluge.html', context)

def pokaz_uslugi(request, id):
    salon = get_object_or_404(Salon, id=id)
    fryzjerzy = salon.fryzjer.all()
    wlasciciel = salon.wlasciciel
    uslugi = Usluga.objects.all().filter(salon=salon)
    mapObject = generateMap(salon.kod_pocztowy, \
                            salon.ulica, \
                            str(salon.nr_lokalu), \
                            "", \
                            salon.miasto, \
                            "")
    oceny = Ocena.objects.all().filter(salon=salon)
    if request.user.is_authenticated:
        zamowienia_klienta = Zamowienie.objects.all().filter(salon=salon).filter(
        klient=Klient.objects.all().filter(user=request.user).first())
    else:
        zamowienia_klienta=None
    context = {
        'salon': salon,
        'fryzjerzy': fryzjerzy,
        'wlasciciel': wlasciciel,
        'uslugi': uslugi,
        'mapObject': mapObject,
        'oceny': oceny,
        'zamowienia_klienta': zamowienia_klienta
    }

    return render(request, 'main/salon_uslugi.html', context)

def pokaz_mape(request, id):
    salon = get_object_or_404(Salon, id=id)
    fryzjerzy = salon.fryzjer.all()
    wlasciciel = salon.wlasciciel
    uslugi = Usluga.objects.all().filter(salon=salon)
    mapObject = generateMap(salon.kod_pocztowy, \
                            salon.ulica, \
                            str(salon.nr_lokalu), \
                            "", \
                            salon.miasto, \
                            "")
    oceny = Ocena.objects.all().filter(salon=salon)
    if request.user.is_authenticated:
        zamowienia_klienta = Zamowienie.objects.all().filter(salon=salon).filter(
        klient=Klient.objects.all().filter(user=request.user).first())
    else:
        zamowienia_klienta=None
    context = {
        'salon': salon,
        'fryzjerzy': fryzjerzy,
        'wlasciciel': wlasciciel,
        'uslugi': uslugi,
        'mapObject': mapObject,
        'oceny': oceny,
        'zamowienia_klienta': zamowienia_klienta
    }

    return render(request, 'main/salon_mapa.html', context)

def pokaz_opinie(request, id):
    salon = get_object_or_404(Salon, id=id)
    fryzjerzy = salon.fryzjer.all()
    wlasciciel = salon.wlasciciel
    uslugi = Usluga.objects.all().filter(salon=salon)
    mapObject = generateMap(salon.kod_pocztowy, \
                            salon.ulica, \
                            str(salon.nr_lokalu), \
                            "", \
                            salon.miasto, \
                            "")
    oceny = Ocena.objects.all().filter(salon=salon)
    if request.user.is_authenticated:
        zamowienia_klienta = Zamowienie.objects.all().filter(salon=salon).filter(
        klient=Klient.objects.all().filter(user=request.user).first())
    else:
        zamowienia_klienta=None
    context = {
        'salon': salon,
        'fryzjerzy': fryzjerzy,
        'wlasciciel': wlasciciel,
        'uslugi': uslugi,
        'mapObject': mapObject,
        'oceny': oceny,
        'zamowienia_klienta': zamowienia_klienta
    }

    return render(request, 'main/salon_opinie.html', context)

def pokaz_klienta(request, id):
    klient = get_object_or_404(Klient, id=id)
    context = {
        'klient': klient,
    }

    return render(request, 'main/pokaz_klienta.html', context)


def pokaz_fryzjera(request, id):
    fryzjer = get_object_or_404(Fryzjer, id=id)
    salon = Salon.objects.all().filter(fryzjer=fryzjer).first()
    oceny = Ocena.objects.all().filter(fryzjer=fryzjer)
    if request.user.is_authenticated:
        zamowienia_klienta = Zamowienie.objects.all().filter(fryzjer=fryzjer).filter(klient=Klient.objects.all().filter(user=request.user).first())
    else:
        zamowienia_klienta=None
    context = {
        'fryzjer': fryzjer,
        'oceny': oceny,
        'zamowienia_klienta': zamowienia_klienta,
        'salon': salon
    }
    return render(request, 'main/pokaz_fryzjera.html', context)

def pokaz_wizyty(request):
    klient=Klient.objects.all().filter(user=request.user).first()
    wizyty=Zamowienie.objects.all().filter(klient=klient)
    context = {
        'klient': klient,
        'wizyty': wizyty,
    }
    return render(request, 'main/pokaz_wizyty.html', context)
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
            try:
                if len(request.FILES['avatar'])>0:
                    if not oldPath==None:
                        os.remove(oldPath)
            except:
                pass
            EditForm.save()
            if profile.avatar=='':
                try:
                    os.remove(oldPath)
                except:
                    pass
            else:
                try:
                    image=Image.open(profile.avatar)
                    (width,height)=image.size
                    if width>250 or height>250:
                        ratio=height/width
                        width=250
                        height=int(ratio*width)
                        new_size=(width,height)
                        image=image.resize(new_size,Image.ANTIALIAS)
                        image.save(str(profile.avatar))
                except:
                    pass
        return redirect('/')
    context = {
        'profile': profile,
        'EditForm': EditForm,
    }
    return render(request, 'main/edytuj_fryzjera.html', context)


def dodaj_opinie_fryzjer(request, id):
    context = {}
    fryzjer = Fryzjer.objects.all().filter(id=id).first()
    context = {
        'fryzjer': fryzjer,
    }
    if request.method == 'POST':
        if fryzjer.srednia_ocena!=None:
            fryzjer.srednia_ocena*=fryzjer.liczba_ocen
            fryzjer.liczba_ocen+=1
            rate=request.POST.get('rate')
            if float(rate)!=0:
                fryzjer.srednia_ocena+=float(request.POST.get('rate'))
                fryzjer.srednia_ocena/=fryzjer.liczba_ocen
                fryzjer.save()
                ocena= Ocena(fryzjer=fryzjer, salon=None, liczba_gwiazdek=rate, klient=Klient.objects.all().filter(user=request.user).first(), tresc=request.POST.get('tresc'))
                ocena.save()
                return redirect('/')
            else:
                messages.info(request, 'Musisz wybrac liczbe gwiazdek!')
                return render(request, 'main/dodaj_opinie_fryzjer.html', context)

        else:
            rate = request.POST.get('rate')
            if float(rate)!=0:
                fryzjer.srednia_ocena=float(request.POST.get('rate'))
                fryzjer.liczba_ocen=1
                fryzjer.save()
                ocena = Ocena(fryzjer=fryzjer, salon=None, liczba_gwiazdek=rate,
                              klient=Klient.objects.all().filter(user=request.user).first(), tresc=request.POST.get('tresc'))
                ocena.save()
                return redirect('/')
            else:
                messages.info(request, 'Musisz wybrac liczbe gwiazdek!')
                return render(request, 'main/dodaj_opinie_fryzjer.html', context)
    return render(request, 'main/dodaj_opinie_fryzjer.html', context)


def dodaj_opinie_salon(request, id):
    context = {}
    salon = Salon.objects.all().filter(id=id).first()
    context = {
        'salon': salon,
    }
    if request.method == 'POST':
        if salon.srednia_ocena!=None:
            salon.srednia_ocena*=salon.liczba_ocen
            salon.liczba_ocen+=1
            rate=request.POST.get('rate')
            if float(rate)!=0:
                salon.srednia_ocena+=float(request.POST.get('rate'))
                salon.srednia_ocena/=salon.liczba_ocen
                salon.save()
                ocena= Ocena(salon=salon, fryzjer=None, liczba_gwiazdek=rate, klient=Klient.objects.all().filter(user=request.user).first(), tresc=request.POST.get('tresc'))
                ocena.save()
                return redirect('/')
            else:
                messages.info(request, 'Musisz wybrac liczbe gwiazdek!')
                return render(request, 'main/dodaj_opinie_salon.html', context)

        else:
            rate = request.POST.get('rate')
            if float(rate)!=0:
                salon.srednia_ocena=float(request.POST.get('rate'))
                salon.liczba_ocen=1
                salon.save()
                ocena = Ocena(salon=salon, fryzjer=None, liczba_gwiazdek=rate,
                              klient=Klient.objects.all().filter(user=request.user).first(), tresc=request.POST.get('tresc'))
                ocena.save()
                return redirect('/')
            else:
                messages.info(request, 'Musisz wybrac liczbe gwiazdek!')
                return render(request, 'main/dodaj_opinie_salon.html', context)
    return render(request, 'main/dodaj_opinie_salon.html', context)


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
            request.FILES.get('avatar', None)
            try:
                if len(request.FILES['avatar']) > 0:
                    if not oldPath == None:
                        os.remove(oldPath)
            except:
                pass
            ClientForm.save()
            if profile.avatar=='':
                try:
                    os.remove(oldPath)
                except:
                    pass
            else:
                try:
                    image=Image.open(profile.avatar)
                    (width,height)=image.size
                    if width>250 or height>250:
                        ratio=height/width
                        width=250
                        height=int(ratio*width)
                        new_size=(width,height)
                        image=image.resize(new_size,Image.ANTIALIAS)
                        image.save(str(profile.avatar))
                except:
                    pass
        return redirect('/')
    context = {
        'profile': profile,
        'ClientForm': ClientForm,
    }
    return render(request, 'main/edytuj_klienta.html', context)


def edytuj_salon(request, id):
    context = {}
    profile = Salon.objects.all().filter(id=id).first()
    try:
        oldPath=profile.avatar.path
    except:
        oldPath=None
    SalonForm = SalonUpdateForm(instance=profile)
    if request.method == 'POST':
        SalonForm = SalonUpdateForm(request.POST, request.FILES, instance=profile)
        if SalonForm.is_valid():
            print("poprawne")
            request.FILES.get('avatar', None)
            try:
                if len(request.FILES['avatar']) > 0:
                    if not oldPath == None:
                        os.remove(oldPath)
            except:
                pass
            SalonForm.save()
            if profile.avatar=='':
                try:
                    os.remove(oldPath)
                except:
                    pass
            else:
                try:
                    image=Image.open(profile.avatar)
                    (width,height)=image.size
                    if width>250 or height>250:
                        ratio=height/width
                        width=250
                        height=int(ratio*width)
                        new_size=(width,height)
                        image=image.resize(new_size,Image.ANTIALIAS)
                        image.save(str(profile.avatar))
                except:
                    pass
        return redirect('/')
    else:
        print(SalonForm.errors)
    context = {
        'profile': profile,
        'SalonForm': SalonForm,
    }
    return render(request, 'main/edytuj_salon.html', context)


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
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
        wizyta.klient=Klient.objects.all().filter(user=request.user).first()
        dane_fryzjera=request.POST.get('wybor').split()
        wizyta.fryzjer=Fryzjer.objects.all().filter(imie=dane_fryzjera[0]).filter(nazwisko=dane_fryzjera[1]).first()
        wizyta.status='sent'
        wizyta.save()
        messages.info(request, generateMap(wizyta.salon.kod_pocztowy, \
                                            wizyta.salon.ulica, \
                                            str(wizyta.salon.nr_lokalu), \
                                            "", \
                                            wizyta.salon.miasto, \
                                            ""), extra_tags='safe')
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
    zapro = {}
    fryzjerzy = Fryzjer.objects.all()

    fryzjerID = request.POST.get('fryzjerSelect', False)
    salonID = request.POST.get('salonSelect', False)

    if salonID != False and fryzjerID != False:
        fryzjerToAdd = Fryzjer.objects.get(id=fryzjerID)
        salonToAdd = Salon.objects.get(id=salonID)
        zapro = SalonRelationship.objects.all()
        is_already_sent = False
        for z in zapro:
            print(f"OBJECT {z.salonID} -- {z.fryzjerID}")
            print(f"TOADD {salonID} -- {fryzjerToAdd.id}")
            if int(z.salonID) == int(salonID) and int(z.fryzjerID) == int(fryzjerToAdd.id):
                is_already_sent = True
                break

        if is_already_sent is False:
            zaproszenie = SalonRelationship(
            salonID=salonID,
            wlascicielID=fryzjer.id,
            fryzjerID=fryzjerToAdd.id,
            imie_fryzjera=fryzjerToAdd.imie,
            imie_wlasciciela=fryzjer.imie,
            nazwisko_wlasciciela=fryzjer.nazwisko,
            nazwa_salonu=salonToAdd.nazwa,
            )
            zaproszenie.save()
            fryzjer.invite_sent.add(fryzjerToAdd)
            fryzjerToAdd.salon_to_add.add(zaproszenie)

        #fryzjer.invite_sent.add(fryzjerToAdd)
        #fryzjerToAdd.invite_received.add(fryzjer)
        #print(f"Fryzjer {fryzjer} wyslal zaproszenie do fryzjera {fryzjerToAdd} do salonu {salonToAdd}")


    context = {
        'salony': salony,
        'fryzjerzy': fryzjerzy,
        'zapro': zapro,
    }

    return render(request, 'main/dodaj_fryzjera.html', context)


#def akceptuj_zaproszenie(request):
   # fryzjer = Fryzjer.objects.get(user=request.user)
    #if request.method == 'POST':
        #Salon.fryzjer.add(fryzjer)

def check_username(request):
    username = request.GET.get('username', None)

    context = {
        'user_exists': User.objects.filter(username=username).exists()
    }

    return JsonResponse(context)

def tworcy(request):
    context = {
        'lukasz': 'Łukasz Lewicki',
        'jakub': 'Jakub Barwiński',
        'bartek': 'Bartłomiej Węgrzyn',
        'michal': 'Michał Ochmiński',
    }
    return render(request, 'main/tworcy.html', context)
def zaproszenia_do_salonu(request):
    fryzjer = Fryzjer.objects.get(user=request.user)
    received_invites = fryzjer.invite_received.all()
    zapro = fryzjer.salon_to_add.all()

    context = {
        'received_invites': received_invites,
        'fryzjer': fryzjer,
        'zapro': zapro,
    }

    return render(request, 'main/zaproszenia_do_salonu.html', context)


def akceptuj_zaproszenie(request, fryzjerID, salonID):
    if request.method == 'POST':
        fryzjer_to_add = Fryzjer.objects.get(id=fryzjerID)
        salon_to_add = Salon.objects.get(id=salonID)

        salon_to_add.fryzjer.add(fryzjer_to_add)
        zapro = SalonRelationship.objects.filter(fryzjerID=fryzjerID, salonID=salonID)
        #print(zapro)
        zapro.delete()

    return redirect('/')


def usun_zaproszenie(request, fryzjerID, salonID):
    wlasciciel = Fryzjer.objects.get(user=request.user)
    fryzjer = Fryzjer.objects.get(id=fryzjerID)
    if request.method == 'POST':
        zapro = SalonRelationship.objects.filter(fryzjerID=fryzjerID, salonID=salonID)
        wlasciciel.invite_sent.remove(fryzjer)
        zapro.delete()

    return redirect('/')


def usun_z_salonu(request, fryzjerID, salonID):
    if request.method == 'POST':
        salon = Salon.objects.get(id=salonID)
        fryzjer = Fryzjer.objects.get(id=fryzjerID)
        salon.fryzjer.remove(fryzjer)

    return redirect('/')


def wyslane_zaproszenia(request):
    wlasciciel = Fryzjer.objects.get(user=request.user)
    zapro = SalonRelationship.objects.filter(wlascicielID=wlasciciel.id)
    zaproszenia = wlasciciel.invite_sent.all()
    context = {
        'zaproszenia': zaproszenia,
        'zapro': zapro,
    }

    return render(request, 'main/zaproszenia.html', context)


def salony(request):
    salony=Salon.objects.all()
    context={'salony': salony}
    return render(request, 'main/salony.html', context)

def fryzjerzy(request):
    fryzjerzy=Fryzjer.objects.all()
    context={'fryzjerzy': fryzjerzy}
    return render(request, 'main/fryzjerzy.html', context)
############## API ###################
class SalonViewSet(viewsets.ModelViewSet):
    queryset = Salon.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class=SalonSerializer
    
class KlientViewSet(viewsets.ModelViewSet):
    queryset = Klient.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class=KlientSerializer
    
class FryzjerViewSet(viewsets.ModelViewSet):
    queryset = Fryzjer.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class=FryzjerSerializer

class UslugaViewSet(viewsets.ModelViewSet):
    queryset = Usluga.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class=UslugaSerializer



class ZamowienieViewSet(viewsets.ModelViewSet):
    queryset = Zamowienie.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class=ZamowienieSerializer    
