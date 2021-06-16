from .models import Salon, Fryzjer, Klient, Usluga, Zamowienie, SalonRelationship, Ocena
from django.contrib.auth.models import User
def request_user_fryzjer(request):
    if request.user.is_authenticated:
        user_fryzjer = Fryzjer.objects.all().filter(user=request.user).first()
        return {
            'user_fryzjer': user_fryzjer
        }
    else:
        return {}

def request_user_klient(request):
    if request.user.is_authenticated:
        user_klient = Klient.objects.all().filter(user=request.user).first()
        return {'user_klient': user_klient}
    else:
        return {}
def request_user_wlasciciel(request):
    if request.user.is_authenticated:
        user_wlasciciel = Salon.objects.all().filter(wlasciciel=Fryzjer.objects.all().filter(user=request.user).first()).first()
        return {'user_wlasciciel': user_wlasciciel}
    else:
        return {}

