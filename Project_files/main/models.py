from django.db import models
from django.contrib.auth.models import User


class SalonRelationship(models.Model):
    salonID = models.IntegerField(null=True, blank=True)
    wlascicielID = models.IntegerField(null=True, blank=True)
    fryzjerID = models.IntegerField(null=True, blank=True)
    nazwa_salonu = models.CharField(max_length=250, null=True, blank=True)
    imie_wlasciciela = models.CharField(max_length=250, null=True, blank=True)
    nazwisko_wlasciciela = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"Wlasciciel {self.imie_wlasciciela} {self.nazwisko_wlasciciela} chce Cie dodac do {self.nazwa_salonu}"


class Fryzjer(models.Model):
    salon_to_add = models.ManyToManyField(SalonRelationship, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    imie = models.CharField(max_length=50, null=True)
    nazwisko = models.CharField(max_length=50, null=True)
    srednia_ocena = models.FloatField(blank=True, null=True)
    liczba_ocen = models.IntegerField(blank=True, null=True)
    bio = models.CharField(max_length=5000, null=True, blank=True)
    ulica = models.CharField(max_length=50, blank=True, null=True)
    nr_domu = models.IntegerField(default=0, blank=True, null=True)
    miasto = models.CharField(max_length=50, null=True)
    kod_pocztowy = models.CharField(max_length=20, null=True)
    nr_tel = models.CharField(max_length=20, default='no number')

    avatar = models.ImageField(upload_to='main/static/ocen_fryzjera/avatars/fryzjers/', null=True, blank=True, default='main/static/ocen_fryzjera/avatars/fryzjers/default-avatar.jpg')

    invites = models.ManyToManyField('self', related_name='invites', null=True, blank=True)
    invite_sent = models.ManyToManyField('self', blank=True, related_name='invites_sent', symmetrical=False)
    invite_received = models.ManyToManyField('self', blank=True, related_name='invites_received', symmetrical=False)

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'


class Salon(models.Model):
    wlasciciel = models.ForeignKey(Fryzjer, on_delete=models.CASCADE, related_name='wlasciciel', null=True)
    fryzjer = models.ManyToManyField(Fryzjer, related_name='fryzjer')
    avatar = models.ImageField(upload_to='main/static/ocen_fryzjera/avatars/salony/', null=True, blank=True)
    nazwa = models.CharField(max_length=50, default='NoName')
    NIP = models.CharField(max_length=25)
    regon = models.CharField(max_length=25)
    ulica = models.CharField(max_length=50, blank=True, null=True)
    nr_lokalu = models.IntegerField(default=0, blank=True, null=True)
    miasto = models.CharField(max_length=50)
    kod_pocztowy = models.CharField(max_length=20)
    nr_tel = models.CharField(max_length=20, default='no number')
    godzina_otwarcia = models.CharField(max_length=10, default='Brak')
    godzina_zamkniecia = models.CharField(max_length=10, default='Brak')
    srednia_ocena = models.FloatField(blank=True, null=True)
    liczba_ocen = models.IntegerField(blank=True, null=True)
    bio = models.CharField(max_length=5000, null=True, blank=True)


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

    avatar = models.ImageField(upload_to='main/static/ocen_fryzjera/avatars/klients/', null=True, blank=True)

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

class Ocena(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, null=True, default=None)
    data = models.DateTimeField(auto_now_add=True, null=True)
    fryzjer = models.ForeignKey(Fryzjer, on_delete=models.CASCADE, null=True, default=None)
    tresc = models.CharField(max_length=300, null=True)
    liczba_gwiazdek = models.IntegerField(default=0, null=True)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.klient.imie
class Zamowienie(models.Model):

    STATUS_CHOICES = (
        ('sent', 'sent'),
        ('accepted', 'accepted'),
    )

    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    fryzjer = models.ForeignKey(Fryzjer, on_delete=models.CASCADE, null=True, default=None)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, null=True, default=None)
    nazwa_zamowienia = models.CharField(max_length=80, null=True)
    termin_uslugi = models.DateTimeField(auto_now_add=False, null=True)
    data_zamowienia = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    def __str__(self):
        return self.nazwa_zamowienia




