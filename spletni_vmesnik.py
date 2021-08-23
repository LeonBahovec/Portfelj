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
    return bottle.template(
        "zacetna_stran.html", 
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


    



bottle.run(debug=True, reloader=True)