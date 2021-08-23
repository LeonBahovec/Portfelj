from os import stat
from yahoofinancials import YahooFinancials
from datetime import date
import json



class Model:
    def __init__(self):
        '''Model trenutno vsebuje zgolj slovar portfeljev'''
        self.portfelji = {}
        self.trenutni_portfelj = 0
    
    def dodaj_portfelj(self, portfelj):
        self.portfelji[portfelj.ime_portfelja] = portfelj
    
    def izbrisi_portfelj(self, portfelj):
        del self.portfelji[portfelj.ime_portfelja]
    
    def v_slovar(self):
        return {
            "portfelji":[portfelj.v_slovar() for portfelj in self.portfelji.values()]
        }
    
    @staticmethod
    def iz_slovarja(slovar):
        krovni_model = Model()
        for portfelj_kot_slovar in slovar["portfelji"]:
            portfelj = Portfelj(portfelj_kot_slovar["ime_portfelja"], portfelj_kot_slovar["valuta"])
            portfelj.kolicina_valute = portfelj_kot_slovar["kolicina_valute"]
            krovni_model.dodaj_portfelj(portfelj)
            for transakcija_kot_slovar in portfelj_kot_slovar["transakcije"]:
                transakcija = Transakcija(
                    transakcija_kot_slovar["poteza"], 
                    Instrument(transakcija_kot_slovar["instrument"]["kratica"], transakcija_kot_slovar["instrument"]["ime"], portfelj), 
                    transakcija_kot_slovar["kolicina"], 
                    transakcija_kot_slovar["cena"], 
                    date.fromisoformat(transakcija_kot_slovar["datum"]), 
                    portfelj
                    )
                portfelj.dodaj_transakcijo(transakcija)
            for instrument_kot_slovar in portfelj_kot_slovar["instrumenti"]:
                instrument = Instrument(instrument_kot_slovar["kratica"], instrument_kot_slovar["ime"], portfelj)
                portfelj.dodaj_instrument(instrument)
        return krovni_model

    def shrani_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w", encoding="utf-8") as datoteka:
            slovar = self.v_slovar()
            json.dump(slovar, datoteka)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke, "r", encoding="utf-8") as datoteka:
            slovar = json.load(datoteka)
            return Model.iz_slovarja(slovar)

class Portfelj:
    def __init__(self, ime_portfelja, valuta):  
        self.ime_portfelja = ime_portfelja
        self.valuta = valuta
        self.kolicina_valute = 100000
        self.transakcije = {}     # Slovar kjer so ključi ¸kratice instrumentov, in vrednosti transakcije opravljene na dolocenem instrumentu
        self.instrumenti = {}     # Seznam instrumentov  
    
    def __repr__(self):
        return f"Portfelj({self.ime_portfelja}, {self.valuta})"
    
    def povecaj_sredstva(self, koliko_zelimo_naloziti):
        '''Poveca kolicino valute za zeljen znesek'''
        self.kolicina_valute += koliko_zelimo_naloziti

    def zmanjsaj_sredstva(self, koliko_zelimo_naloziti):
        '''Zmanjša kolicino valute za zeljen znesek'''
        self.kolicina_valute -= koliko_zelimo_naloziti

    def dodaj_instrument(self, instrument):
        if instrument.kratica not in self.instrumenti:
            self.instrumenti[instrument.kratica] = instrument
        else:
            return None
    
    def pobrisi_prazen_instrument(self, instrument):
        if instrument.kolicina_instrumenta() == 0:
            del self.instrumenti[instrument.kratica]
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
                self.zmanjsaj_sredstva(round(transakcija.kolicina * transakcija.cena, 2))
            else:
                raise ValueError("Nimate dovolj denarnih sredstev za nakup instrumenta!")
        elif transakcija.poteza == "Prodaja":
            if transakcija.kolicina <= transakcija.instrument.kolicina_instrumenta():
                self.dodaj_transakcijo(transakcija)
                self.dodaj_instrument(transakcija.instrument)
                self.povecaj_sredstva(round(transakcija.kolicina * transakcija.cena, 2))
                if transakcija.instrument.kolicina_instrumenta() == 0:
                    self.pobrisi_prazen_instrument(transakcija.instrument)
            else:
                raise ValueError("Na voljo imate premajhno kolicino finančnega inštrumenta. Poskusite s prodajo na prazno")
    
    def vrednost_portfelja(self):
        vrednost_instrumentov = 0
        for instrument in self.instrumenti:
            vrednost_instrumentov += instrument.trenutna_vrednost_instrumenta()
        return vrednost_instrumentov + self.kolicina_valute

    def v_slovar(self):
        seznam_transakcij = []
        for seznam in self.transakcije.values():
            for transakcija in seznam:
                seznam_transakcij.append(transakcija)
        return {
            "ime_portfelja": self.ime_portfelja,
            "valuta": self.valuta,
            "kolicina_valute": self.kolicina_valute,            
            "transakcije": [
                {
                    "poteza": transakcija.poteza,
                    "instrument": {
                        "kratica": transakcija.instrument.kratica,
                        "ime": transakcija.instrument.ime,
                    },
                    "kolicina":transakcija.kolicina,
                    "cena": transakcija.cena,
                    "datum": date.isoformat(transakcija.datum),
                }
                for transakcija in seznam_transakcij
            ],
            "instrumenti": [
                {
                    "kratica": instrument.kratica,
                    "ime": instrument.ime
                }
                for instrument in self.instrumenti.values()
            ]
        }

class Instrument:
    def __init__(self, kratica, ime, portfelj):
        self.kratica = kratica
        self.portfelj = portfelj
        self.ime = ime
        valuta_instrumenta = YahooFinancials(self.kratica).get_currency()
        if valuta_instrumenta == portfelj.valuta:
            self.cena = YahooFinancials(self.kratica).get_current_price()
        else:
            self.cena = YahooFinancials(self.kratica).get_current_price() / YahooFinancials((portfelj.valuta + valuta_instrumenta + "=X")).get_current_price()
        

    def __repr__(self):
        return f"Instrument({self.kratica}, {self.ime}, {self.portfelj})"

    def __str__(self):
        return f"{self.ime}"
    
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

    def donosnost(self):
        vlozeno = self.neto_vlozeno()
        trenutna_vrednost = self.cena * self.kolicina_instrumenta()
        rezultat = round(((trenutna_vrednost / vlozeno) - 1) * 100, 2)
        return f"{rezultat} %"
    


class Transakcija:
    def __init__(self, poteza, instrument, kolicina, cena, datum, portfelj):
        self.poteza = poteza # nakup/prodaja
        self.instrument = instrument
        self.kolicina = kolicina  
        self.cena = cena  
        self.datum = datum
        self.portfelj = portfelj
        
    
    def __repr__(self):
        return f"Transakcija({self.poteza}, {self.instrument}, {self.kolicina}, {self.cena}, {self.datum.isoformat()}, {self.portfelj}"
    def __str__(self):
        return f"Transakcija({self.poteza}, {self.instrument}, {self.kolicina}, {self.cena}, {self.datum.isoformat()}, {self.portfelj}"

    def v_slovar(self):
        return {
            "poteza": self.poteza,
            "instrument": self.instrument,
            "kolicina":self.kolicina,
            "cena": self.cena,
            "datum": date.isoformat(self.datum),
            "portfelj": self.portfelj,
        }

    



