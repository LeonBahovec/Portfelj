import hashlib
import random
from os import stat
from re import A
from yahoofinancials import YahooFinancials
from datetime import date
import json


class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, model):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.model = model	
    
    @staticmethod
    def prijava(uporabnisko_ime, geslo_v_cistopisu):
        uporabnik = Uporabnik.preberi_iz_datoteke(uporabnisko_ime)
        if uporabnik is None:
            raise ValueError("Uporabniško ime ne obstaja")
        elif uporabnik.preveri_geslo(geslo_v_cistopisu):
            return uporabnik
        else:
            raise ValueError("Geslo je napačno")
    
    @staticmethod
    def registracija(uporabnisko_ime, geslo_v_cistopisu):
        if Uporabnik.preberi_iz_datoteke(uporabnisko_ime) is not None:
            raise ValueError("Uporabniško ime že obstaja")
        else:
            zasifrirano_geslo = Uporabnik.zasifriraj_geslo(geslo_v_cistopisu)
            uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo, Model())
            uporabnik.shrani_datoteko()
            return uporabnik

    @staticmethod
    def zasifriraj_geslo(geslo_v_cistopisu, sol=None):
        if sol is None:
            sol = str(random.getrandbits(32))
        posojeno_geslo = sol + geslo_v_cistopisu
        h = hashlib.blake2b()
        h.update(posojeno_geslo.encode(encoding="utf-8"))
        return f"{sol}${h.hexdigest()}"
    
    
    def v_slovar(self):
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "model": self.model.v_slovar(),
        }
    
    @staticmethod
    def ime_uporabnikove_datoteke(uporabnisko_ime):
        return f"{uporabnisko_ime}.json"


    def shrani_datoteko(self):
        with open(Uporabnik.ime_uporabnikove_datoteke(self.uporabnisko_ime), "w", encoding="utf-8") as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    def preveri_geslo(self, geslo_v_cistopisu):
        sol, _ = self.zasifrirano_geslo.split("$")
        return self.zasifrirano_geslo == Uporabnik.zasifriraj_geslo(geslo_v_cistopisu, sol)

    @staticmethod
    def iz_slovarja(slovar):
        uporabnisko_ime = slovar["uporabnisko_ime"]
        zasifrirano_geslo = slovar["zasifrirano_geslo"]
        model = Model.iz_slovarja(slovar["model"])
        return Uporabnik(uporabnisko_ime, zasifrirano_geslo, model)
    
    @staticmethod
    def preberi_iz_datoteke(uporabnisko_ime):
        try:
            with open(Uporabnik.ime_uporabnikove_datoteke(uporabnisko_ime), "r", encoding="utf-8") as datoteka:
                slovar = json.load(datoteka)
                return Uporabnik.iz_slovarja(slovar)
        except FileNotFoundError:
            return None




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
        if self.trenutni_portfelj == 0:
            return {
                "portfelji":[portfelj.v_slovar() for portfelj in self.portfelji.values()],
                "trenutni_portfelj": 0
            }
        else:
            return {
                "portfelji":[portfelj.v_slovar() for portfelj in self.portfelji.values()],
                "trenutni_portfelj": self.trenutni_portfelj.ime_portfelja
            }
    
    @staticmethod
    def iz_slovarja(slovar):
        krovni_model = Model()
        for portfelj_kot_slovar in slovar["portfelji"]:
            portfelj = Portfelj(portfelj_kot_slovar["ime_portfelja"], portfelj_kot_slovar["valuta"])
            portfelj.kolicina_valute = portfelj_kot_slovar["kolicina_valute"]
            krovni_model.dodaj_portfelj(portfelj)
            seznam_kratic = [instrument["kratica"] for instrument in portfelj_kot_slovar["instrumenti"]]
            slovar_cen = YahooFinancials(seznam_kratic).get_current_price()
            for instrument_kot_slovar in portfelj_kot_slovar["instrumenti"]:
                if instrument_kot_slovar["valuta"] == portfelj.valuta:
                    cena = slovar_cen[instrument_kot_slovar["kratica"]]
                    instrument = Instrument(
                        instrument_kot_slovar["kratica"],
                        instrument_kot_slovar["ime"],
                        portfelj,
                        instrument_kot_slovar["valuta"],
                        cena
                    )
                    portfelj.dodaj_instrument(instrument)
                else:
                    cena_v_valuti_delnice = slovar_cen[instrument_kot_slovar["kratica"]]
                    cena = cena_v_valuti_delnice / (YahooFinancials(portfelj.valuta + instrument_kot_slovar["valuta"] + "=X").get_current_price())
                    instrument = Instrument(
                        instrument_kot_slovar["kratica"],
                        instrument_kot_slovar["ime"],
                        portfelj,
                        instrument_kot_slovar["valuta"],
                        cena
                    )
                    portfelj.dodaj_instrument(instrument)                   
            for transakcija_kot_slovar in portfelj_kot_slovar["transakcije"]:
                transakcija = Transakcija(
                    transakcija_kot_slovar["poteza"], 
                    portfelj.instrumenti[transakcija_kot_slovar["instrument"]], 
                    transakcija_kot_slovar["kolicina"], 
                    transakcija_kot_slovar["cena"], 
                    date.fromisoformat(transakcija_kot_slovar["datum"]), 
                    portfelj
                )       
                portfelj.dodaj_transakcijo(transakcija)
        if slovar["trenutni_portfelj"] == 0:
            krovni_model.trenutni_portfelj = 0
        else:
            krovni_model.trenutni_portfelj = krovni_model.portfelji[slovar["trenutni_portfelj"]]
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
                raise ValueError("Na voljo imate premajhno kolicino finančnega inštrumenta.")
    
    def vrednost_portfelja(self):
        vrednost_instrumentov = 0
        for instrument in self.instrumenti.values():
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
                    "instrument": transakcija.instrument.kratica,
                    "kolicina":transakcija.kolicina,
                    "cena": transakcija.cena,
                    "datum": date.isoformat(transakcija.datum),
                }
                for transakcija in seznam_transakcij
            ],
            "instrumenti": [
                {
                    "kratica": instrument.kratica,
                    "ime": instrument.ime,
                    "valuta" : instrument.valuta
                }
                for instrument in self.instrumenti.values()
            ]
        }

class Instrument:
    def __init__(self, kratica, ime, portfelj, valuta=None, cena=None):
        self.kratica = kratica
        self.portfelj = portfelj
        self.ime = ime
        if valuta == None:
            self.valuta = YahooFinancials(self.kratica).get_currency()
        else:
            self.valuta = valuta
        if cena == None:    
            if self.valuta == portfelj.valuta:
                self.cena = YahooFinancials(self.kratica).get_current_price()
            else:
                self.cena = YahooFinancials(self.kratica).get_current_price() / YahooFinancials((portfelj.valuta + self.valuta + "=X")).get_current_price()
        else:
            self.cena = cena
        

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

    



    