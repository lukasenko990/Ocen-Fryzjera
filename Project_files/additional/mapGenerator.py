#!/usr/bin/env python3

import urllib.parse

# generuje adres do Google Maps w formie gotowej do osadzenia w HTMLu
# (&amp; zamiast samego ampersandu)
def generateHTMLAddress(zipCode, streetName, buildingNumber, objectName, city, country):
    part=""
    if len(zipCode)>0:
        part+=zipCode
    if len(streetName)>0:
        if len(part)>0:
            part+=","
        part+=streetName
    if len(buildingNumber)>0:
        if len(part)>0:
            part+=","
        part+=buildingNumber
    if len(objectName)>0:
        if len(part)>0:
            part+=","
        part+=objectName
    if len(city)>0:
        if len(part)>0:
            part+=","
        part+=city
    if len(country)>0:
        if len(part)>0:
            part+=","
        part+=country
    return "https://maps.google.com/maps?q="+urllib.parse.quote(part) \
            +"&amp;t=&amp;z=15&amp;ie=UTF8&amp;iwloc=&amp;output=embed"

# generuje pełny kod IFRAME gotowy do osadzenia w HTMLu
# użycie: (WSZYSTKO MUSI BYĆ W STRINGACH!) kod pocztowy, nazwa ulicy, numer
#         budynku, nazwa obiektu, miasto, kraj
# konieczne jest podanie tylko tych parametrów, które się ma, w przeciwnym
# wypadku pozostawić puste, zakomentowany przykład na dole
def generateMap(zipCode, streetName, buildingNumber, objectName, city, country):
	return '<div><iframe class="map" src="' \
            +generateHTMLAddress(zipCode, \
                                streetName, \
                                buildingNumber, \
                                objectName, \
                                city, \
                                country) \
            +'"></iframe></div>'

# print(generateMap("20-250","Ignacego Daszyńskiego","19","","Lublin",""))
