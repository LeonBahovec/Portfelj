from model import Portfolio, Valuta, Instrument, Transakcija
###########################################################
# Pomožne funkcije za prikaz
###########################################################
testni_portfelj = Portfolio("EUR")

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
            #povzetek_stanja()
            print()
            print(krepko("Kaj bi radi naredili?"))
            moznosti = [
                ("dodal instrument", kupi_instrument),
                ("izbrisal instrument", izbrisi_instrument),
                ("izpisek instrumentov", izpis_instrumentov),
                ("pogledal stanje", izpis_stanja),
            ]
            izbira = izberi(moznosti)
            print(80 * "-")
            izbira()
            print()
            input("Pritisnite Enter za shranjevanje in vrnitev v osnovni meni...")
            proracun.shrani_stanje(DATOTEKA_S_STANJEM)
        except ValueError as e:
            print(slabo(e.args[0]))
        except KeyboardInterrupt:
            print()
            print("Nasvidenje!")
            return

def kupi_instrument():
    print("Prosimo vnesite sledeče podatke: ")
    poteza = "Nakup"
    instrument = input("> Kratica finančnega inštrumenta: ")
    cena = input("> Nakupna cena enote finančnega inštrumenta: ") # tu je treba dodati moznost da cloveku ponudimo trenutno ceno
    kolicina = input("> Število enot: ")
    valuta = testni_portfelj.valuta  ##Tole bo treba se popraviti, (posplositi na poljuben portfelj)
    transakcija = Transakcija("Nakup", instrument, kolicina, cena, valuta)
    testni_portfelj.opravi_transakcijo(transakcija)



def uvodni_pozdrav():
    print(krepko("Pozdravljeni!"))
    print("Za izhod pritisnite Ctrl-C.")
moznosti = [
                ("kupil instrument", "dodaj_racun"),
                ("prodal instrument", "dodaj_kuverto"),
                ("pogledal instrumente", "odstrani_kuverto"),
                ("pogledal stanje", "poglej_stanje"),
            ]