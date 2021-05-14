from .models import Salon, Usluga, Fryzjer, Klient, Zamowienie
from rest_framework import serializers

class SalonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Salon
        fields=['wlasciciel','fryzjer','nazwa','NIP','regon','ulica','nr_lokalu','miasto','kod_pocztowy','nr_tel','godzina_otwarcia','godzina_zamkniecia']
        
class FryzjerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Fryzjer
        fields=['imie','nazwisko','srednia_ocena','ulica','nr_domu','miasto','kod_pocztowy','nr_tel','avatar']
        
class KlientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Klient
        fields=['imie','nazwisko','staly_klient','nr_telefonu','ulica','nr_domu','miasto','kod_pocztowy','avatar']
        
class UslugaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Usluga
        fields=['nazwa','opis','cena','min_czas','max_czas']
        
class ZamowienieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Zamowienie
        fields=['salon','nazwa_zamowienia','termin_uslugi','data_zamowienia','status']
                
                