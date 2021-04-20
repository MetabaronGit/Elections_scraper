# Engeto Academy projekt č.3
Závěrečný projekt Python Engeto Academy Brno.
## Popis projektu
Tento projekt slouží k extrahování výsledků parlamentních voleb České republiky v roce 2017. Odkaz na celkové výsledky voleb je [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).
## Instalace knihoven
Knihovny potřebné ke spuštění tohoto programu jsou uloženy v souboru **`requirements.txt`** Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem následně spustit:

```bash
$ pip3 --version                      # overim verzi manazeru
$ pip3 install -r requirements.txt    # nainstalujeme knihovny
```
## Spuštění projektu
Spuštění souboru **`election_scraper.py`** v rámci příkazové řádky požaduje dva povinné argumenty.
```
python election_scraper.py <odkaz_uzemniho_celku> <vysledny_soubor>
```
Následně se vám stáhnou výsledky a uloží do zadaného souboru .csv.
## Ukázka projektu
Výsledky hlasování pro okres Hradec Králové:
1. argument: "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5201"
2. argument: "vysledky_hradec.csv"

Spuštění programu:
```
python election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5201" "vysledky_hradec.csv"
```
Průběh stahování:
```
Stahuji data z vybraného URL https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5201 ...
Ukládám výsledky do souboru vysledky_prostejov.csv ...
Soubor vysledky_hradec.csv byl vytvořen.
Program election_scraper byl ukončen.
```
Ukázka výstupu z finálního souboru csv:
```
municipality_number,municipality_name,registered_voters,envelopes_issued,total_valid_votes...
569828,Babice,165,109,108,7,1,0,4,-1,0,7,19,3,0,-1,0,1,0,6,-1,-1,-1,0,9,36,0,0,2,-1,1,0,0,12,0,-1
569836,Barchov,227,141,140,21,0,0,9,-1,0,5,16,2,0,-1,2,0,0,19,-1,-1,-1,1,4,46,1,0,3,-1,2,1,1,6,1,-1
569852,Běleč nad Orlicí,269,207,206,38,0,0,8,-1,0,9,1,3,0,-1,7,0,0,16,-1,-1,-1,0,12,76,0,0,10,-1,1,0,0,25,0,-1
569861,Benátky,93,67,67,9,0,0,2,-1,0,9,1,0,0,-1,2,0,0,7,-1,-1,-1,0,5,19,0,0,5,-1,0,0,2,6,0,-1
...
```
