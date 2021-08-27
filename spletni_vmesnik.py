from typing import Type
import bottle
from model import Model, Portfelj, Transakcija, Instrument
from datetime import date

DATOTEKA_S_STANJEM = "stanje.json"


try:
    testni_model = Model.preberi_iz_datoteke(DATOTEKA_S_STANJEM)
except FileNotFoundError:
    testni_model = Model()


@bottle.get("/")
def osnovna_stran():
    if testni_model.trenutni_portfelj != 0:
        bottle.redirect("/portfelj/" + testni_model.trenutni_portfelj.ime_portfelja)
    else:
        if testni_model.portfelji != {}:
            nakljucno_ime_portfelja = list(testni_model.portfelji.keys())[0]
            bottle.redirect("portfelj/" + nakljucno_ime_portfelja)
        else:
            return bottle.template(
                "brez_portfeljev.html",
                portfelji=testni_model.portfelji.values(),
                trenutni_portfelj=testni_model.trenutni_portfelj
            )

@bottle.get("/portfelj/<portfelj>")
def osnovna_stran_portfelja(portfelj):
    testni_model.trenutni_portfelj = testni_model.portfelji[portfelj]
    return bottle.template(
        "zacetna_stran.html",
        sporocilo=None, 
        portfelji=testni_model.portfelji.values(),
        trenutni_portfelj=testni_model.trenutni_portfelj
    ) 

@bottle.get("/prijava/")
def prijava():
    return bottle.template(
        "prijava.html",
        sporocilo=None,
        portfelji=testni_model.portfelji.values(),
        trenutni_portfelj=testni_model.trenutni_portfelj
    )


@bottle.get("/obrazec-za-dodajanje-portfelja/")
def obrazec_za_dodajanje_portfelja():
    return bottle.template(
        "obrazec_za_dodajanje_portfelja.html",
        portfelji=testni_model.portfelji.values(),
        trenutni_portfelj=testni_model.trenutni_portfelj
        )

@bottle.post("/dodaj-portfelj/")
def dodaj_portfelj():
    novi_portfelj = Portfelj(
        bottle.request.forms.getunicode("ime_portfelja"),
        bottle.request.forms.getunicode("valuta"))
    testni_model.dodaj_portfelj(novi_portfelj)
    testni_model.trenutni_portfelj = novi_portfelj
    testni_model.shrani_datoteko(DATOTEKA_S_STANJEM)
    bottle.redirect("/")

@bottle.post("/zamenjaj-portfelj/")
def zamenjaj_portfelj():
    testni_model.trenutni_portfelj = testni_model.portfelji[
        (bottle.request.forms.getunicode("trenutni_portfelj"))
        ]
    bottle.redirect("/")

@bottle.get("/obrazec-za-nakup/")
def obrazec_za_nakup():
    return bottle.template(
        "obrazec_za_nakup.html",
        sporocilo=None,
        portfelji=testni_model.portfelji.values())

@bottle.post("/opravi-nakup/")
def opravi_nakup():
    portfelj = testni_model.portfelji[bottle.request.forms.getunicode("izberi_portfelj")]
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
            portfelji=testni_model.portfelji.values(),
            trenutni_portfelj=testni_model.trenutni_portfelj
        )

    kolicina = float(bottle.request.forms.getunicode("kolicina"))
    cena = instrument.cena
    datum = date.today()
    transakcija = Transakcija("Nakup", instrument, kolicina, cena, datum, portfelj)
    try:
        portfelj.opravi_transakcijo(transakcija)
        testni_model.shrani_datoteko(DATOTEKA_S_STANJEM)
        return bottle.template(
            "zacetna_stran.html",
            sporocilo="Uspešno ste opravili transakcijo!",
            portfelji=testni_model.portfelji.values(),
            trenutni_portfelj=testni_model.trenutni_portfelj,
        )
    except ValueError as e:
        return bottle.template(
            "zacetna_stran.html",
            sporocilo=e.args[0],
            portfelji=testni_model.portfelji.values(),
            trenutni_portfelj=testni_model.trenutni_portfelj,
         )

@bottle.post("/opravi-prodajo/")
def opravi_prodajo():
    portfelj = testni_model.trenutni_portfelj
    instrument = portfelj.instrumenti[
        bottle.request.forms.getunicode("kratica")
            
    ]
    kolicina = float(bottle.request.forms.getunicode("kolicina"))
    cena = instrument.cena
    datum = date.today()
    transakcija = Transakcija("Prodaja", instrument, kolicina, cena, datum, portfelj)
    try:
        portfelj.opravi_transakcijo(transakcija)
        testni_model.shrani_datoteko(DATOTEKA_S_STANJEM)
        return bottle.template(
            "zacetna_stran.html",
            sporocilo="Uspešno ste opravili transakcijo",
            portfelji=testni_model.portfelji.values(),
            trenutni_portfelj=testni_model.trenutni_portfelj
        )
    except ValueError as e:
        return bottle.template(
            "zacetna_stran.html",
            sporocilo=e.args[0],
            portfelji=testni_model.portfelji.values(),
            trenutni_portfelj=testni_model.trenutni_portfelj
        )







    



bottle.run(debug=True, reloader=True)