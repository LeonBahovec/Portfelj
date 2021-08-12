from yahoofinancials import YahooFinancials
NAKUP = "Nakup"
PRODAJA = "Prodaja"


#class Uporabnik:
#    def __init__(self, ime_uporabnika):
#        self.ime_uporabnika = ime_uporabnika
#        self.portfelji = []
#
#    def dodaj_portfelj(self, portfelj):
#        self.portfelji.append(portfelj)
#    
#    def izbrisi_portfelj(self, portfelj):
#        self.portfelji.remove(portfelj)


class Portfolio:
    def __init__(self, ime_portfelja,valuta):   # Razmisli, ali bi imel vec valut, ali zgolj eno osnovno valuto
        self.ime_portfelja = ime_portfelja
        self.valuta = valuta
        self.transakcije = {}     # Slovar kjer so ključi instrumenti, in vrednosti transakcije opravljene na dolocenem instrumentu
        self.instrumenti = []     # Seznam instrumentov  
    
    def nalozi_sredstva(self, koliko_zelimo_naloziti):
        self.valuta.kolicina += koliko_zelimo_naloziti
    
    def dvigni_sredstva(self, koliko_zelimo_naloziti):
        self.valuta.kolicina =- koliko_zelimo_naloziti

    def dodaj_instrument(self, instrument):
        self.instrumenti.append(instrument) 
    
    def pobrisi_instrument(self, instrument):
        self.instrumenti.remove(instrument)
    
    def opravi_transakcijo(self, transakcija):
        if poteza == NAKUP:
            if not transakcija.instrument in self.instrumenti:
                self.dodaj_instrument()
            transakcija.instrument += transakcija.kolicina
        elif poteza == PRODAJA:
            #DODAJ DA PREVERI ALI JE PRODAJA MOŽNA
            transakcija.instrument.kolicina += -(transakcija.kolicina)
            transakcija.instrument.valuta += (transakcija.kolicina * transakcija.cena)
        self.transakcije.append(transakcija)

class Valuta:
    def __init__(self, kratica, ime, kolicina):
        self.kratica = kratica
        self.ime = ime
        self.kolicina = kolicina

    def __repr__(self):
        return f"Valuta({self.kratica}, {self.ime}, {self.kolicina})"
    
    def __str__(self):
        return f"self.ime"         

class Instrument:
    def __init__(self, kratica, ime, portfolio):
        self.kratica = kratica
        self.ime = ime
        self.portfolio = portfolio
        self.cena = YahooFinancials(kratica).get_current_price()
    
    # DODAJ METODI VLOZENO in KOLICINA(izracunaj iz transakcij)

    def __repr__(self):
        return f"Instrument({self.kratica}, {self.ime}, {self.portfolio})"

    def __str__(self):
        return f"self.ime"
    


class Transakcija:
    def __init__(self, poteza, instrument, kolicina, cena, valuta):
        self.poteza = poteza #nakup/prodaja
        self.kolicina = kolicina
        self.cena = cena #tu daj moznost da clovek bodisi izbere svojo ceno, ali pa kar trzno ceno v tistem trenutku
        self.instrument = instrument
        self.valuta = valuta

valuta1 = Valuta("EUR", "Euro", 0) 
portfelj1 = Portfolio("Slovenija", valuta1)


