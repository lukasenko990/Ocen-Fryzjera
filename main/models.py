from django.db import models
from django.contrib.auth.models import User


class Salon(models.Model):
    nazwa = models.CharField(max_length=50, default='NoName')
    NIP = models.CharField(max_length=25)
    regon = models.CharField(max_length=25)

    ulica = models.CharField(max_length=50, blank=True, null=True)
    nr_lokalu = models.IntegerField(default=0, blank=True, null=True)
    miasto = models.CharField(max_length=50)
    kod_pocztowy = models.CharField(max_length=20)

    def __str__(self):
        return self.nazwa


class Klient(models.Model):
    imie = models.CharField(max_length=50, null=True)
    nazwisko = models.CharField(max_length=50, null=True)
    #### Klasa bazowa User zawiera w sobie: imie, nazwisko, email, nazwe_uzytkownika, haslo
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='klient')

    staly_klient = models.BooleanField(default=False, null=True)
    nr_telefonu = models.CharField(max_length=20, null=True, blank=True)

    ulica = models.CharField(max_length=50, blank=True, null=True)
    nr_domu = models.IntegerField(default=0, blank=True, null=True)
    miasto = models.CharField(max_length=50, null=True)
    kod_pocztowy = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'


class Fryzjer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salon = models.ManyToManyField(Salon, null=True, blank=True)

    imie = models.CharField(max_length=50, null=True)
    nazwisko = models.CharField(max_length=50, null=True)
    srednia_ocena = models.FloatField(blank=True, null=True)

    ulica = models.CharField(max_length=50, blank=True, null=True)
    nr_domu = models.IntegerField(default=0, blank=True, null=True)
    miasto = models.CharField(max_length=50, null=True)
    kod_pocztowy = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'


class Usluga(models.Model):
    salon = models.ManyToManyField(Salon)

    nazwa = models.CharField(max_length=80, null=True)
    opis = models.TextField(null=True, blank=True)
    cena = models.FloatField(default=0, null=True)
    min_czas = models.IntegerField(default=0, null=True)
    max_czas = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.nazwa


class Zamowienie(models.Model):

    STATUS_CHOICES = (
        ('sent', 'sent'),
        ('accepted', 'accepted'),
    )

    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)

    nazwa_zamowienia = models.CharField(max_length=80, null=True)
    termin_uslugi = models.DateTimeField(auto_now_add=False, null=True)
    data_zamowienia = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    def __str__(self):
        return self.nazwa_zamowienia




