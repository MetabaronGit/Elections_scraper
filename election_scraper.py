import sys
import requests
from bs4 import BeautifulSoup as BS
import csv
import time

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
    candidates = soup.find_all("td", class_="cislo", headers="t1sa1 t1sb1")
    candidates += soup.find_all("td", class_="cislo", headers="t2sa1 t2sb1")
    valid_candidates_list = [candidate.text.strip() for candidate in candidates]

    # platné hlasy jednotlivých kandidátů
    valid_votes = soup.find_all("td", class_="cislo", headers="t1sa2 t1sb3")
    valid_votes += soup.find_all("td", class_="cislo", headers="t2sa2 t2sb3")
    valid_votes_list = [votes.text.strip().replace("\xa0", "") for votes in valid_votes]

    result["valid_candidates"] = dict(zip(valid_candidates_list, valid_votes_list))

    return result


def create_csv(file_name: str, header: list, data: list) -> None:
    """Zapíše údaje do nového souboru csv"""
    with open(file_name, "w") as f:
        f_writer = csv.writer(f)
        f_writer.writerow(header)
        f_writer.writerows(data)
    print("csv vytvořen")


def create_csv_content(final_result: dict, valid_candidates: int) -> list:
    """Zkonvertuje data do formátu pro zápis do csv souboru"""
    result = []
    for municipality_nr in final_result:
        line = []
        line.append(municipality_nr)
        line.append(final_result.get(municipality_nr)["municipality_name"])
        line.append(final_result.get(municipality_nr)["registered_voters"])
        line.append(final_result.get(municipality_nr)["envelopes_issued"])
        line.append(final_result.get(municipality_nr)["total_valid_votes"])

        # zapíše počty hlasů jednotlivých kandidátů, pokud strana nekandidovala, zapíše se -1
        for candidate in range(1, valid_candidates + 1):
            try:
                line.append(final_result.get(municipality_nr)["valid_candidates"][str(candidate)])
            except:
                line.append("-1")

        result.append(line)

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
    # print(all_valid_candidates)

    # vytvoření hlavičky pro csv soubor
    csv_header = ["municipality_number",
                  "municipality_name",
                  "registered_voters",
                  "envelopes_issued",
                  "total_valid_votes"]
    for valid_candidate_nr in range(1, len(all_valid_candidates) + 1):
        csv_header.append(all_valid_candidates.get(str(valid_candidate_nr)))
    # print(csv_header)

    final_result = dict()
    soup = get_soup(url)

    # seznam obcí ve vybraném okrese ze vstupní URL key=č.obce, value=odkaz na výsledky
    municipalities = get_municipalities(soup)
    for municipality_nr in municipalities:
        final_result[municipality_nr] = get_municipality_election_results(URL_ROOT +
                                                                          municipalities.get(municipality_nr))
        time.sleep(0.2)
        break

    print("vytvářím csv")
    print(final_result)
    data = create_csv_content(final_result, len(all_valid_candidates))
    create_csv(file_name, csv_header, data)


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
