from django.contrib import admin
from .models import Salon, Usluga, Fryzjer, Klient, Zamowienie, SalonRelationship, Ocena


admin.site.register(Salon)
admin.site.register(Usluga)
admin.site.register(Fryzjer)
admin.site.register(Klient)
admin.site.register(Zamowienie)
admin.site.register(SalonRelationship)
admin.site.register(Ocena)