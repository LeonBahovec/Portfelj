NAKUP = "Nakup"
PRODAJA = "Prodaja"


class Model:
    def __init__(self):
        self.valute = []
        self.transakcije = []
        self.instrumenti = []
    
    def dodaj_valuto(self, valuta):
        self.valute.append(valuta)
    
    def pobrisi_valuto(self, valuta):
        self.valute.remove(valuta)
    
    def dodaj_instrument(self, instrument):
        self.instrumenti.append(instrument)
    
    def pobrisi_instrument(self, instrument):
        self.istrumenti.append(instrument)
    
    def opravi_transakcijo(self, transakcija):
        self.transakcije.append(transakcija)
        if poteza == NAKUP:
            #DODAJ DA PREVERI ALI JE NAKUP MOŽEN
            transakcija.valuta.kolicina += -(transakcija.kolicina * transakcija.cena)
            if not transakcija.instrument in self.instrumenti:
                self.dodaj_instrument()
            transakcija.instrument += transakcija.kolicina
        elif poteza == PRODAJA:
            #DODAJ DA PREVERI ALI JE PRODAJA MOŽNA
            transakcija.instrument.kolicina += -(transakcija.kolicina)
            transakcija.instrument.valuta += (transakcija.kolicina * transakcija.cena)

class Valuta:
    def __init__(self, kratica, ime, kolicina):
        self.ime = ime
        self.kolicina = kolicina
        self.kratica = kratica

class Instrument:
    def __init__(self, kratica, ime, kolicina):
        self.kratica = kratica
        self.ime = ime
        self.kolicina = kolicina

class Transakcija:
    def __init__(self, poteza, kolicina, cena, opis, instrument, valuta):
        self.poteza = poteza #nakup/prodaja
        self.kolicina = kolicina
        self.cena = cena
        self.opis = opis
        self.instrument = instrument
        self.valuta = valuta