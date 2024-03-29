# Portfelj

## Opis programa

S programom lahko uporabnik virtualno trguje s finančnimi inštrumenti. 
Uporabnik lahko ustvari poljubno mnogo portfeljev. Pri ustvarjanju portfelja uporabnik izbere v kateri valuti želi spremljati gibanje cen. Ko je portfelj ustvarjen uporabnik dobi 100.000 enot valute, ki jih prosto lahko uporabi za nakupe finančnih instrumentov. Program nato spremlja premike cen ter prikazuje vrednost in donosnost portfelja. 

Program omogoča trgovanje z inštrumenti, ki so na voljo na platformi [Yahoo Finance](https://finance.yahoo.com/).
Pri nakupu inštrumenta je potrebno vnesti njegovo borzno kratico. Slednja se nahaja na osnovni strani posameznega inštrumenta v oklepaju poleg imena inštrumenta. Applova kratica je tako na primer [AAPL](https://finance.yahoo.com/quote/AAPL/).


![Apple, Yahoo finance](https://i.ibb.co/8czyg4m/apple.png)


## Navodila za uporabo
Za delovanje programa je potrebno naložiti knjižnico **YahooFinancials**.

Program se požene prek datoteke **spletni_vmesnik.py**

## Opomba
Knjižnjica YahooFinancials, ki skrbi za podatke o finančnih inštrumentih pobira podatke izredno počasi (Vsak klic funkcije iz te knjižnice traja vsaj nekaj sekund), zato tudi sam program deluje počasi. Sploh počasna je spletna storitev za več uporabnikov. Vsakič ko prijavljen uporabnik naloži novo stran, namreč na novo preberemo podatke iz uporabnikove datoteke in ob tem uporabimo YahooFinancials precejkrat, zato nalaganje strani lahko traja tudi po nekaj minut.

Različica za enega uporabnika ([git commit iz 27. avgusta "Popravil opozorila za napacne vnose"](https://github.com/LeonBahovec/Portfelj/tree/5be1c7494ea23cb43f9bd85681449224b2424692)) je zato načeloma prijaznejša za uporabo, saj iz datoteke podatke nalaga le ob ponovnem zagonu programa.