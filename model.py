from yahoofinancials import YahooFinancials

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

class Model:
    def __init__(self):
        '''Model trenutno vsebuje zgolj seznam portfeljev'''
        self.portfelji = {}
        self.trenutni_portfelj = 0
    
    def dodaj_portfelj(self, portfelj):
        self.portfelji[portfelj.ime_portfelja] = portfelj
    
    def izbrisi_portfelj(self, portfelj):
        del self.portfelji[portfelj.ime_portfelja]
    
    def vrednost_portfelja(self, portfelj):
        pass


class Portfelj:
    def __init__(self, ime_portfelja, valuta):  
        self.ime_portfelja = ime_portfelja
        self.valuta = valuta
        self.kolicina_valute = 0
        self.transakcije = {}     # Slovar kjer so ključi ¸kratice instrumentov, in vrednosti transakcije opravljene na dolocenem instrumentu
        self.instrumenti = []     # Seznam instrumentov  
    
    def __repr__(self):
        return f"Portfelj({self.ime_portfelja}, {self.valuta})"
    
    def povecaj_sredstva(self, koliko_zelimo_naloziti):
        '''Poveca kolicino valute za zeljen znesek'''
        self.kolicina_valute += koliko_zelimo_naloziti

    def zmanjsaj_sredstva(self, koliko_zelimo_naloziti):
        '''Zmanjša kolicino valute za zeljen znesek'''
        self.kolicina_valute -= koliko_zelimo_naloziti

    def dodaj_instrument(self, instrument):
        if instrument not in self.instrumenti:
            self.instrumenti.append(instrument)
        else:
            return None
    
    def pobrisi_prazen_instrument(self, instrument):
        if instrument.kolicina_instrumenta() == 0:
            self.instrumenti.remove(instrument)
        else:
            return None
    def dodaj_transakcijo(self, transakcija):
        if transakcija.instrument.kratica not in self.transakcije:
            self.transakcije[transakcija.instrument.kratica] = [transakcija]
        else:
            self.transakcije[transakcija.instrument.kratica].append(transakcija)

    def opravi_transakcijo(self, transakcija):
        if transakcija.poteza == "Nakup":
            if transakcija.cena * transakcija.kolicina <= self.kolicina_valute:
                self.dodaj_transakcijo(transakcija)
                self.dodaj_instrument(transakcija.instrument)
                self.zmanjsaj_sredstva(transakcija.kolicina * transakcija.cena)
            else:
                raise ValueError("Nimate dovolj denarnih sredstev za nakup instrumenta!")
        elif transakcija.poteza == "Prodaja":
            if transakcija.kolicina <= transakcija.instrument.kolicina_instrumenta():
                self.dodaj_transakcijo(transakcija)
                self.dodaj_instrument(transakcija.instrument)
                self.povecaj_sredstva(transakcija.kolicina * transakcija.cena)
                if transakcija.instrument.kolicina_instrumenta() == 0:
                    self.pobrisi_prazen_instrument(transakcija.instrument)
            else:
                raise ValueError("Na voljo imate premajhno kolicino finančnega inštrumenta. Poskusite s prodajo na prazno")
    
    def vrednost_portfelja(self):
        vrednost_instrumentov = 0
        for instrument in self.instrumenti:
            vrednost_instrumentov += instrument.trenutna_vrednost_instrumenta()
        return vrednost_instrumentov + self.kolicina_valute
                   

class Instrument:
    def __init__(self, kratica, portfelj):
        self.kratica = kratica
        self.portfelj = portfelj

    def __repr__(self):
        return f"Instrument({self.kratica}, {self.ime()}, {self.portfelj})"

    def __str__(self):
        return f"{self.ime}"
    
    def cena(self):
        return YahooFinancials(self.kratica).get_current_price()

    def ime(self):
        return YahooFinancials(self.kratica).get_stock_quote_type_data()[self.kratica]["shortName"]
    
    def kolicina_instrumenta(self):
        kolicina = 0
        for transakcija in self.portfelj.transakcije[self.kratica]:
            if transakcija.poteza == "Nakup":
                kolicina += transakcija.kolicina
            elif transakcija.poteza == "Prodaja":
                kolicina -= transakcija.kolicina
        return kolicina
    
    def neto_vlozeno(self):
        vlozeno = 0
        for transakcija in self.portfelj.transakcije[self.kratica]:
            if transakcija.poteza == "Nakup":
                vlozeno += (transakcija.cena * transakcija.kolicina)
            elif transakcija.poteza == "Prodaja":
                vlozeno -= (transakcija.cena * transakcija.kolicina)
        return vlozeno

    def trenutna_vrednost_instrumenta(self):
        return self.cena * self.kolicina_instrumenta()

class Transakcija:
    def __init__(self, poteza, instrument, kolicina, cena, portfelj):
        self.poteza = poteza # nakup/prodaja
        self.instrument = instrument
        self.kolicina = kolicina  
        self.cena = cena  ## tu daj moznost da clovek bodisi izbere svojo ceno, ali pa kar trzno ceno v tistem trenutku
        self.portfelj = portfelj
    
    def __repr__(self):
        return f"Transakcija({self.poteza}, {self.instrument}, {self.kolicina}, {self.cena}, {self.portfelj}"
    def __str__(self):
        return f"Transakcija({self.poteza}, {self.instrument}, {self.kolicina}, {self.cena}, {self.portfelj}"


model1 = Model()
portfelj1 = Portfelj("Slovenija", "EUR")
portfelj1.povecaj_sredstva(10000)
instrument1 = Instrument("AAPL", portfelj1)
transakcija1 = Transakcija("Nakup", instrument1, 100, 30, portfelj1)
transakcija2 = Transakcija("Nakup", instrument1, 200, 40, portfelj1)
transakcija3 = Transakcija("Prodaja", instrument1, 100, 50, portfelj1)
model1.dodaj_portfelj(portfelj1)

portfelj1.opravi_transakcijo(transakcija1)


