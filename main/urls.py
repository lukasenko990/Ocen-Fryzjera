from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),

    path('pokaz_salon/<int:id>/', views.pokaz_salon, name='pokaz_salon'),
    path('pokaz_klienta/<int:id>/', views.pokaz_klienta, name='pokaz_klienta'),
    path('pokaz_fryzjera/<int:id>/', views.pokaz_fryzjera, name='pokaz_fryzjera'),

]
