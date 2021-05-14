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
    path('barber/register', views.barber_register, name='barber_register'),
    path('search/', views.search, name='search'),

    path('pokaz_salon/<int:id>/', views.pokaz_salon, name='pokaz_salon'),
    path('pokaz_klienta/<int:id>/', views.pokaz_klienta, name='pokaz_klienta'),
    path('pokaz_fryzjera/<int:id>/', views.pokaz_fryzjera, name='pokaz_fryzjera'),
    path('pokaz_usluge/<int:id>/', views.pokaz_usluge, name='pokaz_usluge'),
    path('umow_wizyte/<int:id>/', views.umow_wizyte, name='umow_wizyte'),
    path('edytuj_fryzjera/<int:id>', views.edytuj_fryzjera, name='edytuj_fryzjera'),
    path('edytuj_klienta/<int:id>', views.edytuj_klienta, name='edytuj_klienta'),
    path('edytuj_salon/<int:id>/', views.edytuj_salon, name='edytuj_salon'),

    path('dodaj_fryzjera/', views.dodaj_fryzjera, name='dodaj_fryzjera'),
    path('zaproszenia/', views.zaproszenia_do_salonu, name='zaproszenia_do_salonu'),
    path('api/',include(router.urls))
]
