from django.contrib import admin
from .models import Salon, Usluga, Fryzjer, Klient, Zamowienie, SalonRelationship


admin.site.register(Salon)
admin.site.register(Usluga)
admin.site.register(Fryzjer)
admin.site.register(Klient)
admin.site.register(Zamowienie)
admin.site.register(SalonRelationship)