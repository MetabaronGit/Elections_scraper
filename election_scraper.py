import sys
import requests
from bs4 import BeautifulSoup as BS

URL_ROOT = "https://volby.cz/pls/ps2017nss/"
URL_VALID_CANDIDATES = "ps11?xjazyk=CZ&xv=1&xt=2"


def get_soup(url: str) -> BS:
    """Vrátí BeautifulSoup objekt zadané URL."""
    html_doc = requests.get(url).text
    return BS(html_doc, "html.parser")


def get_municipalities(soup: BS) -> dict:
    """Vrátí slovník se seznamem všech čísel obcí v okrese včetně odkazů na jejich volební výsledky."""
    result = dict()

    table = soup.find_all("td", class_="cislo")
    for line in table:
        municipality_number = line.text # cislo obce
        url_municipality_result = line.find("a").attrs["href"]  # odkay na vysledky v obci
        result[str(municipality_number)] = str(url_municipality_result)

    return result


def get_all_valid_candidates(url: str) -> dict:
    """Vrátí slovník se seznamem čísel a jmen všech platných kandidátů."""
    result = dict()
    soup = get_soup(url)
    table = soup.find_all("th", class_="leg_sloupec")
    for line in table:
        candidate = line.text.split(" ", 1)
        if candidate[0].isdecimal():
            result[candidate[0]] = candidate[1]
    return result


def get_municipality_election_results(url: str) -> dict:
    """Vrátí slovník s výsledkovými údaji obce ze zadané URL"""
    result = dict()
    soup = get_soup(url)

    # nazev obce
    data = soup.find_all("h3")
    municipality_name = data[2].text[6:].strip()
    result["municipality_name"] = municipality_name

    # volici v seznamu
    registered_voters = soup.find("td", class_="cislo", headers="sa2").text.strip()
    result["registered_voters"] = registered_voters.replace("\xa0", "")

    # vydane obalky
    envelopes_issued = soup.find("td", class_="cislo", headers="sa3").text.strip()
    result["envelopes_issued"] = envelopes_issued.replace("\xa0", "")

    # platne hlasy celkem
    total_valid_votes = soup.find("td", class_="cislo", headers="sa6").text.strip()
    result["total_valid_votes"] = total_valid_votes.replace("\xa0", "")

    # seznam kandidátů
    voters = soup.find_all("td", class_="cislo", headers="t1sa1 t1sb1")
    voters += soup.find_all("td", class_="cislo", headers="t2sa1 t2sb1")
    registered_voters_list = [voter.text.strip() for voter in voters]

    # platné hlasy jednotlivých kandidátů
    valid_votes = soup.find_all("td", class_="cislo", headers="t1sa2 t1sb3")
    valid_votes += soup.find_all("td", class_="cislo", headers="t2sa2 t2sb3")
    valid_votes_list = [votes.text.strip().replace("\xa0", "") for votes in valid_votes]

    result["registered_voters"] = dict(zip(registered_voters_list, valid_votes_list))

    print(result)
    exit()

    return result


    return result



def main():
    url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
    file_name = "vysledky_prostejov.csv"

    try:
        url = sys.argv[1]
        file_name = sys.argv[2]
        print(url)
        print(file_name)
    except Exception:
        print("Špatně zadané argumenty.")
        # exit()

    # seznam všech platných kandidátů key=číslo, value=jméno
    all_valid_candidates = get_all_valid_candidates(URL_ROOT + URL_VALID_CANDIDATES)
    print(all_valid_candidates)


    final_result = dict()
    soup = get_soup(url)

    # seznam obcí ve vybraném okrese ze vstupní URL key=č.obce, value=odkaz na výsledky
    municipalities = get_municipalities(soup)
    for municipality_nr in municipalities:
        final_result[municipality_nr] = get_municipality_election_results(URL_ROOT +
                                                                          municipalities.get(municipality_nr))
    print(final_result)


if __name__ == "__main__":
    main()

# úvodní stránka
# https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ
# výběr okresů z tabulek dle krajů

# 1. parametr: odkaz vybraného okresu (Hradec Králové)
# https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5201
# 2.parametr: jméno csv souboru
# csv soubor
# kód obce = č.obce, pod ním je odkaz na tabulku s výsledky (Babice)
# https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=8&xobec=569828&xvyber=5201
# https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=8&xobec={cislo_obce}&xvyber=5201
# název obce =obec

# z odkazu č. obce
# voliči v seznamu = č.
# vydané obálky = č.
# platné hlasy = č.
# kandidující strany = list názvů

# výstup:
# dictionary {kod_obce:{nazev_obce: str
#                       volici_v_seznamu: int
#                       vydane_obalky: int
#                       platne_hlasy: int
#                       kandidujici_strany: {cislo_strany: platne_hlasy int, ...}
#                       },
#              ...}
