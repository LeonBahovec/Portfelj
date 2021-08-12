from yahoofinancials import YahooFinancials
NAKUP = "Nakup"
PRODAJA = "Prodaja"


class Portfolio:
    def __init__(self, valuta):   # Razmisli, ali bi imel vec valut, ali zgolj eno osnovno valuto
        self.valuta = valuta
        self.transakcije = {}     # Slovar kjer so ključi instrumenti, in vrednosti transakcije opravljene na dolocenem instrumentu
        self.instrumenti = []     # Seznam instrumentov  
    
    #def dodaj_valuto(self, valuta):                to bi bilo za zbrisat 
    #    self.valute[valuta.kratica] = valuta
                    
    #def pobrisi_valuto(self, valuta):              to tudi
    #    self.valute.remove(valuta)
        #izbrisi v slovarju
    
    def dodaj_instrument(self, instrument):
        self.instrumenti.append(instrument) 
    
    def pobrisi_instrument(self, instrument):
        self.instrumenti.remove(instrument)
    
    def opravi_nakup(self, transakcija):
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
        

class Instrument:
    def __init__(self, kratica, ime, portfolio):
        self.kratica = kratica
        self.ime = ime
        self.kolicina = kolicina
        self.portfolio = portfolio
        self.cena = YahooFinancials(kratica).get_current_price()
        self.vlozek = self.vlozeno()
    
    #def vlozeno(self):
     #   for transakcija in self.portfolio.transakcije:
      #      if transakcija.instrument.ime == self.ime:


class Transakcija:
    def __init__(self, poteza, instrument, kolicina, cena, valuta):
        self.poteza = poteza #nakup/prodaja
        self.kolicina = kolicina
        self.cena = cena #tu daj moznost da clovek bodisi izbere svojo ceno, ali pa kar trzno ceno v tistem trenutku
        self.instrument = instrument
        self.valuta = valuta