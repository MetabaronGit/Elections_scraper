import sys
import requests
import bs4


def get_soup(url: str) -> bs4.BeautifulSoup:
    html_doc = requests.get(url).content
    return bs4.BeautifulSoup(html_doc, "html.parser")



def main():
    url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5201"
    file_name = "vysledky_hradec.csv"

    try:
        url = sys.argv[1]
        file_name = sys.argv[2]
        print(url)
        print(file_name)
    except Exception:
        print("Špatně zadané argumenty.")
        # exit()

    soup = get_soup(url)
    tabs = soup.find_all("div", class_="t3")
    for tab in tabs:
        linky = tab.find_all("a")
        for link in linky:
            print(link.attrs["href"])

        cisla_obci = tab.find_all("td", class_="cislo")
        for cislo_obce in cisla_obci:
            print(cislo_obce.text)

        jmena_obci = tab.find_all("td", headers="t1sa1 t1sb2")
        for jmeno_obce in jmena_obci:
            print(jmeno_obce.text)

        print(len(cisla_obci), len(jmena_obci), len(linky))
    # print(file_name)


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
