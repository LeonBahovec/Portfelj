from pickle import PickleBuffer
from typing import Type
import bottle
from model import Uporabnik, Model, Portfelj, Transakcija, Instrument
from datetime import date

#DATOTEKA_S_STANJEM = "stanje.json"
PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "1988"

#    testni_model = Model.preberi_iz_datoteke(DATOTEKA_S_STANJEM)
#except FileNotFoundError:
#ime_uporabnikove_datoteke(uporabnik.uporabnisko_ime)

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    if uporabnisko_ime:
        return podatki_uporabnika(uporabnisko_ime)
    else:
        bottle.redirect("/prijava/")

def podatki_uporabnika(uporabnisko_ime):
    return Uporabnik.preberi_iz_datoteke(uporabnisko_ime)







@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija", napaka=None)

@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    try:
        Uporabnik.registracija(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
        )
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template("registracija.html", napaka=e.args[0])


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template(
        "prijava.html",
        napaka=None
    )

@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    try:
        Uporabnik.prijava(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
        )
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template(
            "prijava.html", napaka=e.args[0]
        )

@bottle.post("/odjava/")
def odjava():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path="/")
    bottle.redirect("/")

@bottle.get("/")
def osnovna_stran():
    uporabnik = trenutni_uporabnik()
    if uporabnik.model.trenutni_portfelj != 0:
        bottle.redirect("/portfelj/" + uporabnik.model.trenutni_portfelj.ime_portfelja)
    else:
        if uporabnik.model.portfelji != {}:
            nakljucno_ime_portfelja = list(uporabnik.model.portfelji.keys())[0]
            bottle.redirect("portfelj/" + nakljucno_ime_portfelja)
        else:
            return bottle.template(
                "brez_portfeljev.html",
                portfelji=uporabnik.model.portfelji.values(),
                trenutni_portfelj=uporabnik.model.trenutni_portfelj,
                user=uporabnik
            )

@bottle.get("/portfelj/<portfelj>")
def osnovna_stran_portfelja(portfelj):
    uporabnik = trenutni_uporabnik()
    uporabnik.model.trenutni_portfelj = uporabnik.model.portfelji[portfelj]
    return bottle.template(
        "zacetna_stran.html",
        sporocilo=None, 
        portfelji=uporabnik.model.portfelji.values(),
        trenutni_portfelj=uporabnik.model.trenutni_portfelj,
        user=uporabnik
    ) 

@bottle.get("/obrazec-za-dodajanje-portfelja/")
def obrazec_za_dodajanje_portfelja():
    uporabnik = trenutni_uporabnik()
    return bottle.template(
        "obrazec_za_dodajanje_portfelja.html",
        portfelji=uporabnik.model.portfelji.values(),
        trenutni_portfelj=uporabnik.model.trenutni_portfelj,
        user=uporabnik
        )


@bottle.post("/dodaj-portfelj/")
def dodaj_portfelj():
    uporabnik = trenutni_uporabnik()
    novi_portfelj = Portfelj(
        bottle.request.forms.getunicode("ime_portfelja"),
        bottle.request.forms.getunicode("valuta"))
    uporabnik.model.dodaj_portfelj(novi_portfelj)
    uporabnik.model.trenutni_portfelj = novi_portfelj
    uporabnik.shrani_datoteko()
    bottle.redirect("/")

@bottle.post("/zamenjaj-portfelj/")
def zamenjaj_portfelj():
    uporabnik = trenutni_uporabnik()
    uporabnik.model.trenutni_portfelj = uporabnik.model.portfelji[
        (bottle.request.forms.getunicode("trenutni_portfelj"))
        ]
    bottle.redirect("/")

@bottle.get("/obrazec-za-nakup/")
def obrazec_za_nakup():
    uporabnik = trenutni_uporabnik()
    return bottle.template(
        "obrazec_za_nakup.html",
        sporocilo=None,
        portfelji=uporabnik.model.portfelji.values())

@bottle.post("/opravi-nakup/")
def opravi_nakup():
    uporabnik = trenutni_uporabnik()
    portfelj = uporabnik.model.portfelji[bottle.request.forms.getunicode("izberi_portfelj")]
    try:
        instrument = Instrument(
        bottle.request.forms.getunicode("kratica"),
        bottle.request.forms.getunicode("ime_instrumenta"),
        portfelj
    )
    except TypeError:
        return bottle.template(
            "zacetna_stran.html",
            sporocilo="Kratica, ki ste jo vnesli ne obstaja",
            portfelji=uporabnik.model.portfelji.values(),
            trenutni_portfelj=uporabnik.model.trenutni_portfelj,
            user=uporabnik
        )
    kolicina = float(bottle.request.forms.getunicode("kolicina"))
    cena = instrument.cena
    datum = date.today()
    transakcija = Transakcija("Nakup", instrument, kolicina, cena, datum, portfelj)
    try:
        portfelj.opravi_transakcijo(transakcija)
        uporabnik.shrani_datoteko()
        return bottle.template(
            "zacetna_stran.html",
            sporocilo="Uspešno ste opravili transakcijo!",
            portfelji=uporabnik.model.portfelji.values(),
            trenutni_portfelj=uporabnik.model.trenutni_portfelj,
            user=uporabnik
        )
    except ValueError as e:
        return bottle.template(
            "zacetna_stran.html",
            sporocilo=e.args[0],
            portfelji=uporabnik.model.portfelji.values(),
            trenutni_portfelj=uporabnik.model.trenutni_portfelj,
            user=uporabnik
         )

@bottle.post("/opravi-prodajo/")
def opravi_prodajo():
    uporabnik = trenutni_uporabnik()
    portfelj = uporabnik.model.trenutni_portfelj
    instrument = portfelj.instrumenti[
        bottle.request.forms.getunicode("kratica")
            
    ]
    kolicina = float(bottle.request.forms.getunicode("kolicina"))
    cena = instrument.cena
    datum = date.today()
    transakcija = Transakcija("Prodaja", instrument, kolicina, cena, datum, portfelj)
    try:
        portfelj.opravi_transakcijo(transakcija)
        uporabnik.shrani_datoteko()
        return bottle.template(
            "zacetna_stran.html",
            sporocilo="Uspešno ste opravili transakcijo",
            portfelji=uporabnik.model.portfelji.values(),
            trenutni_portfelj=uporabnik.model.trenutni_portfelj,
            user=uporabnik
        )
    except ValueError as e:
        return bottle.template(
            "zacetna_stran.html",
            sporocilo=e.args[0],
            portfelji=uporabnik.model.portfelji.values(),
            trenutni_portfelj=uporabnik.model.trenutni_portfelj,
            user=uporabnik
        )







    



bottle.run(debug=True, reloader=True)

