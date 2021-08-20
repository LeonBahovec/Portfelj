from model import Model, Portfelj, Instrument, Transakcija #, Uporabnik
import datetime
import json
###########################################################
# Pomožne funkcije za prikaz
###########################################################

DATOTEKA_S_STANJEM = "stanje.json"

try:
    testni_model = Model.preberi_iz_datoteke(DATOTEKA_S_STANJEM)
except FileNotFoundError:
    testni_model = Model()

def krepko(niz):
    return f"\033[1m{niz}\033[0m"


def dobro(niz):
    return f"\033[1;94m{niz}\033[0m"


def slabo(niz):
    return f"\033[1;91m{niz}\033[0m"

def vnesi_stevilo(pozdrav):
    """S standardnega vhoda prebere naravno število."""
    while True:
        try:
            stevilo = input(pozdrav)
            return int(stevilo)
        except ValueError:
            print(slabo("Prosim, da vnesete število!"))


def izberi(seznam):
    """
    Uporabniku omogoči interaktivno izbiro elementa iz seznama.
    Funkcija sprejme seznam parov (oznaka, element), prikaže seznam
    oznak ter vrne element, ki ustreza vpisani oznaki.
    >>> izberi([('deset', 10), ('trideset', 30)])
    1) deset
    2) trideset
    > 2
    30
    """
    if len(seznam) == 1:
        opis, element = seznam[0]
        print(f"Na voljo je samo možnost {opis}, zato sem jo izbral.")
        return element
    for indeks, (oznaka, _) in enumerate(seznam, 1):
        print(f"{indeks}) {oznaka}")
    while True:
        izbira = vnesi_stevilo("> ")
        if 1 <= izbira <= len(seznam):
            _, element = seznam[izbira - 1]
            return element
        else:
            print(slabo(f"Izberi število med 1 in {len(seznam)}"))

###########################################################
# Tekstovni vmesnik
###########################################################


def tekstovni_vmesnik():
    uvodni_pozdrav()
    while True:
        try:    
            print(80 * "=")
            print()
            print(krepko("Kaj bi radi naredili?"))
            if testni_model.trenutni_portfelj == 0:
                pass
            else:
                print(dobro(f"Vaš trenutni aktivni portfelj je: {testni_model.trenutni_portfelj.ime_portfelja}"))
            moznosti = [
                ("izberi aktivni portfelj", izberi_aktivni_portfelj),
                ("dodal portfelj", dodaj_portfelj),
                ("nalozi sredstva", nalozi_sredstva),
                ("dvigni sredstva", dvigni_sredstva),
                ("kupil instrument", kupi_instrument),
                ("prodal instrument", prodaj_instrument),
                ("izpisek instrumentov", izpis_instrumentov),
                ("pogledal stanje sredstev", izpis_stanja_sredstev),
            ]
            izbira = izberi(moznosti)
            print(80 * "-")
            izbira()
            print()
            input("Pritisnite Enter za shranjevanje in vrnitev v osnovni meni...")
        except KeyboardInterrupt:
            print()
            testni_model.shrani_datoteko(DATOTEKA_S_STANJEM)
            print("Nasvidenje")
            return None
        except ValueError as e:
            print(slabo(e.args[0]))
            

def dodaj_portfelj():
    print("Prosimo vnesite sledeče podatke: ")
    ime_portfelja = input("> Ime portfelja: ")
    for portfelj in testni_model.portfelji.values():
        if ime_portfelja == portfelj.ime_portfelja:
            print("Portfelj s takim imenom že obstaja, poskusite ponovno!")
            print("Prosimo izberite novo ime!")
            ime_portfelja = input("> Ime portfelja: ")
    valuta = input(" Valuta (prosimo vnesite 3-mestno kratico): ")
    portfelj = Portfelj(ime_portfelja, valuta)
    testni_model.dodaj_portfelj(portfelj)
    testni_model.trenutni_portfelj = portfelj
    print("Uspešno ste dodali portfelj " + krepko(f"{portfelj.ime_portfelja}"))
    print(krepko(f"{portfelj.ime_portfelja}" + "je bil nastavljen kot aktivni portfelj"))

def izberi_aktivni_portfelj():
    if testni_model.portfelji == {}:
        print("Trenutno niste dodali še nobenega portfelja!")
        return None
    print("Izberite enega izmed vaših portfeljev:")
    moznosti = []
    for par in testni_model.portfelji.items():
        moznosti.append(par)
    izbran_portfelj = izberi(moznosti)
    testni_model.trenutni_portfelj = izbran_portfelj
    print(f"{izbran_portfelj.ime_portfelja} je bil nastavljen kot aktivni portfelj")


def nalozi_sredstva():
    portfelj = testni_model.trenutni_portfelj
    koliko_zelite_naloziti = vnesi_stevilo("> Koliko denarja zelite naloziti: ")
    portfelj.povecaj_sredstva(koliko_zelite_naloziti) 
    print(f"Uspesno ste nalozili sredstva, trenutno imate na racunu portfelja \"{portfelj.ime_portfelja}\" {portfelj.kolicina_valute} {portfelj.valuta}") 

def dvigni_sredstva():
    portfelj = testni_model.trenutni_portfelj
    koliko_zelite_dvigniti = vnesi_stevilo("> Koliko denarja želite dvigniti: ")
    portfelj.zmanjsaj_sredstva(koliko_zelite_dvigniti)
    print(f"Uspesno ste dvignili sredstva, trenutno imate na racunu portfelja \"{portfelj.ime_portfelja}\" {portfelj.kolicina_valute} {portfelj.valuta}") 


def kupi_instrument():
    print("Prosimo vnesite sledeče podatke: ")
    # ustvarjanje instrumenta
    portfelj = testni_model.trenutni_portfelj
    kratica = input("> Kratica finančnega inštrumenta: ")
    ime = input("> Ime inštrumenta: ")
    print("Nalaganje podatkov, prosimo počakajte par sekund!")
    instrument = Instrument(kratica, ime, portfelj)
    #ustvarjanje transakcije
    kolicina = vnesi_stevilo("> Število enot: ")
    cena = instrument.cena
    print(f"Trenutna cena ene enote instrumenta je {cena} {instrument.portfelj.valuta}")    
    transakcija = Transakcija("Nakup", instrument, kolicina, cena, datetime.date.today(), portfelj)
    portfelj.opravi_transakcijo(transakcija)
    print(f"Uspešno ste kupili {kolicina} enot " + krepko(f"{instrument.ime}. Na voljo imate še " f"{portfelj.kolicina_valute} {portfelj.valuta}"))

def prodaj_instrument():
    #ustvarjanje instrumenta
    portfelj = testni_model.trenutni_portfelj
    if portfelj.instrumenti == []:
        print("Trenutno niste dodali še nobenega portfelja!")
        return None
    print("Izberite kateri inštrument želite prodati:")
    moznosti = []
    for instrument in portfelj.instrumenti.values():
        moznosti.append((instrument.ime, instrument))
    instrument = izberi(moznosti)
    #ustvarjanje transakcije
    kolicina = vnesi_stevilo("> Število enot: ")
    cena = instrument.cena
    print(f"Trenutna cena ene enote instrumenta je {cena} {instrument.portfelj.valuta}")
    transakcija = Transakcija("Prodaja", instrument, kolicina, cena, portfelj)
    portfelj.opravi_transakcijo(transakcija)
    print(f"Uspesno ste prodali {kolicina} enot " + krepko(f"{instrument.ime}."))


def izpis_instrumentov():
    portfelj = testni_model.trenutni_portfelj
    if portfelj.instrumenti == {}:
        print("Trenutno nimate še nobenih finančnih inštrumentov")
        return None
    for instrument in portfelj.instrumenti.values():
        print(f"{instrument.ime}, {instrument.kolicina_instrumenta()}, {instrument.cena} {portfelj.valuta}")

def izpis_stanja_sredstev():
    portfelj = testni_model.trenutni_portfelj
    print(f"{portfelj.kolicina_valute} {portfelj.valuta}")

def uvodni_pozdrav():
    print(krepko("Pozdravljeni!"))
    print("Za izhod pritisnite Ctrl-C.")



tekstovni_vmesnik()