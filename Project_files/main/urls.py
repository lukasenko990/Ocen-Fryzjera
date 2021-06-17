from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import SalonViewSet,KlientViewSet,FryzjerViewSet,UslugaViewSet,ZamowienieViewSet


router=routers.DefaultRouter()
router.register(r'fryzjer', FryzjerViewSet)
router.register(r'salon',SalonViewSet)
router.register(r'klient',KlientViewSet)
router.register(r'usluga',UslugaViewSet)
router.register(r'zamowienie',ZamowienieViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('barber_register/', views.barber_register, name='barber_register'),
    path('search/', views.search, name='search'),

    path('opinie/<int:id>/', views.pokaz_opinie, name='pokaz_opinie'),
    path('uslugi/<int:id>/', views.pokaz_uslugi, name='pokaz_uslugi'),
    path('mapa/<int:id>/', views.pokaz_mape, name='pokaz_mape'),
    path('wizyty/', views.pokaz_wizyty, name='pokaz_wizyty'),
    path('salony/', views.salony, name='salony'),
    path('fryzjerzy/', views.fryzjerzy, name='fryzjerzy'),
    path('pokaz_salon/<int:id>/', views.pokaz_salon, name='pokaz_salon'),
    path('pokaz_klienta/<int:id>/', views.pokaz_klienta, name='pokaz_klienta'),
    path('pokaz_fryzjera/<int:id>/', views.pokaz_fryzjera, name='pokaz_fryzjera'),
    path('pokaz_usluge/<int:id>/', views.pokaz_usluge, name='pokaz_usluge'),
    path('umow_wizyte/<int:id>/', views.umow_wizyte, name='umow_wizyte'),
    path('edytuj_fryzjera/<int:id>', views.edytuj_fryzjera, name='edytuj_fryzjera'),
    path('edytuj_klienta/<int:id>', views.edytuj_klienta, name='edytuj_klienta'),
    path('edytuj_salon/<int:id>/', views.edytuj_salon, name='edytuj_salon'),
    path('dodaj_opinie_fryzjer/<int:id>/', views.dodaj_opinie_fryzjer, name='dodaj_opinie_fryzjer'),
    path('dodaj_opinie_salon/<int:id>/', views.dodaj_opinie_salon, name='dodaj_opinie_salon'),
    path('dodaj_fryzjera/', views.dodaj_fryzjera, name='dodaj_fryzjera'),
    path('zaproszenia/', views.zaproszenia_do_salonu, name='zaproszenia_do_salonu'),
    path('akceptuj_zaproszenie/<int:fryzjerID>/<int:salonID>/', views.akceptuj_zaproszenie, name='akceptuj_zaproszenie'),
    path('usun_zaproszenie/<int:fryzjerID>/<int:salonID>/', views.usun_zaproszenie, name='usun_zaproszenie'),
    path('usun_z_salonu/<int:fryzjerID>/<int:salonID>/', views.usun_z_salonu, name="usun_z_salonu"),
    path('wyslane_zaproszenia/', views.wyslane_zaproszenia, name="wyslane_zaproszenia"),


    ### api ####
    path('api/',include(router.urls))
]
