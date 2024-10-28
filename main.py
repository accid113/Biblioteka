import csv
from datetime import datetime
import os
import re


class Ksiazka:
    def __init__(self, id, tytul, autor, rok_wydania, status):
        self.id = id
        self.tytul = tytul
        self.autor = autor
        self.rok_wydania = rok_wydania
        self.status = status


class Czytacz:
    def __init__(self, numer_czytacza, imie, nazwisko, ilosc_ksiazek):
        self.numer_czytacza = numer_czytacza
        self.imie = imie
        self.nazwisko = nazwisko
        self.ilosc_ksiazek = ilosc_ksiazek


class Historia:
    def __init__(self, id, numer_czytacza, czy_udana, data_wypozyczenia, data_oddania):
        self.id = id
        self.numer_czytacza = numer_czytacza
        self.czy_udana = czy_udana
        self.data_wypozyczenia = data_wypozyczenia
        self.data_oddania = data_oddania


def wczytaj_plik(nazwa_pliku):
    if not os.path.exists(nazwa_pliku):
        with open(nazwa_pliku, "w", newline="", encoding="utf-8") as csvfile:
            pass

    dane = []
    with open(nazwa_pliku, newline="", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            dane.append(row)
    return dane


def zapisz_plik(nazwa_pliku, dane):
    with open(nazwa_pliku, "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")
        for row in dane:
            csvwriter.writerow(row)


def zawiera_polskie_znaki(tekst):
    polskie_znaki_pattern = re.compile(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]")
    return bool(polskie_znaki_pattern.search(tekst))


def przyznaj_najmniejsze_id():
    biblioteka = wczytaj_plik("biblioteka.csv")

    if not biblioteka:
        return 1  # Jeśli biblioteka jest pusta, zwróć ID 1 jako najmniejsze dostępne ID

    ids = [int(row[0]) for row in biblioteka]
    min_id = min(ids)
    new_id = min_id - 1 if min_id > 1 else 1

    return new_id


def dodaj_ksiazke():
    biblioteka = wczytaj_plik("biblioteka.csv")
    id = przyznaj_najmniejsze_id()
    tytul = input("Podaj tytul ksiazki: ").lower()
    if zawiera_polskie_znaki(tytul):
        print("Proszę wprowadzić tytuł bez polskich znaków.")
        return
    autor = input("Podaj autora ksiazki: ").lower()
    if zawiera_polskie_znaki(autor):
        print("Proszę wprowadzić tytuł bez polskich znaków.")
        return
    rok_wydania = input("Podaj rok wydania ksiazki: ")
    if rok_wydania > datetime.now().strftime("%Y"):
        print("Ksiazka nie mogla zostac wydana")
        return

    status = "dostepna"
    biblioteka.append([id, tytul, autor, rok_wydania, status])
    zapisz_plik("biblioteka.csv", biblioteka)
    print("ksiazka zostala dodana")


def nowy_czytacz(numer_czytacza):
    czytacze = wczytaj_plik("czytacze.csv")

    while True:
        imie = input("Podaj imię czytacza: ").lower()
        if zawiera_polskie_znaki(imie):
            print("Proszę wprowadzić tytuł bez polskich znaków.")
            return
        nazwisko = input("Podaj nazwisko czytacza: ").lower()
        if zawiera_polskie_znaki(nazwisko):
            print("Proszę wprowadzić tytuł bez polskich znaków.")
            return
        if zawiera_polskie_znaki(imie) or zawiera_polskie_znaki(nazwisko):
            print("Proszę wprowadzić dane bez polskich znaków.")
            continue
        numer_jest_unikalny = True
        imie_nazwisko_jest_unikalne = True

        for czytacz in czytacze:
            if czytacz[0] == numer_czytacza:
                numer_jest_unikalny = False
            if czytacz[1] == imie and czytacz[2] == nazwisko:
                imie_nazwisko_jest_unikalne = False

        if not numer_jest_unikalny:
            print("Numer czytacza już istnieje. Proszę wprowadzić inne dane.")
            numer_czytacza = input("Podaj nowy numer czytacza: ")
        elif not imie_nazwisko_jest_unikalne:
            print("Imię i nazwisko czytacza już istnieją. Proszę wprowadzić inne dane.")
        else:
            break

    ilosc_ksiazek = 0
    czytacz = [numer_czytacza, imie, nazwisko, ilosc_ksiazek]
    return czytacz


def wypozycz_ksiazke():
    biblioteka = wczytaj_plik("biblioteka.csv")
    czytacze = wczytaj_plik("czytacze.csv")
    historia = wczytaj_plik("historia.csv")

    id = input("Podaj ID ksiazki: ")
    numer_czytacza = input("Podaj numer czytacza: ")

    czy_czytacz_istnieje = False
    for czytacz in czytacze:
        if czytacz[0] == numer_czytacza:
            czy_czytacz_istnieje = True
            break

    if not czy_czytacz_istnieje:
        print("Czytacz nie istnieje. Tworzenie nowego czytacza...")
        nowy = nowy_czytacz(numer_czytacza)
        czytacze.append(nowy)
        zapisz_plik("czytacze.csv", czytacze)

    for row in biblioteka:
        if row[0] == id and row[4] == "dostepna":
            row[4] = "wypozyczona"
            zapisz_plik("biblioteka.csv", biblioteka)

            for czytacz in czytacze:
                if czytacz[0] == numer_czytacza:
                    czytacz[3] = int(czytacz[3]) + 1
                    zapisz_plik("czytacze.csv", czytacze)
                    break

            data_wypozyczenia = datetime.now().strftime("%Y-%m-%d")
            historia.append([id, numer_czytacza, "tak", data_wypozyczenia, ""])
            zapisz_plik("historia.csv", historia)
            print("Ksiazka zostala wypozyczona.")
            break
    else:
        print("Ksiazka jest niedostepna lub nie istnieje.")


def zwroc_ksiazke():
    biblioteka = wczytaj_plik("biblioteka.csv")
    czytacze = wczytaj_plik("czytacze.csv")
    historia = wczytaj_plik("historia.csv")

    id = input("Podaj ID ksiazki: ")
    numer_czytacza = input("Podaj numer czytacza: ")

    for row in biblioteka:
        if row[0] == id and row[4] == "wypozyczona":
            row[4] = "dostepna"
            zapisz_plik("biblioteka.csv", biblioteka)

            for czytacz in czytacze:
                if czytacz[0] == numer_czytacza:
                    czytacz[3] = int(czytacz[3]) - 1
                    zapisz_plik("czytacze.csv", czytacze)
                    break

            data_oddania = datetime.now().strftime("%Y-%m-%d")
            for wiersz in historia:
                if wiersz[0] == id and wiersz[1] == numer_czytacza and wiersz[4] == "":
                    wiersz[4] = data_oddania
                    zapisz_plik("historia.csv", historia)
                    break

            print("Ksiazka zostala zwrocona.")
            break
    else:
        print("Ksiazka nie jest wypozyczona lub nie istnieje.")


def wyswietl_historie_ksiazki():
    historia = wczytaj_plik("historia.csv")
    book_id = input("Podaj ID ksiazki: ")

    print("\nHistoria wypozyczen ksiazki:")
    for row in historia:
        if row[0] == book_id:
            print("Numer czytacza: {}, Czy udana: {}, Data wypozyczenia: {}, Data oddania: {}".format(row[1], row[2],
                                                                                                      row[3], row[4]))


def main():
    while True:
        print("\n--- Biblioteka ---")
        print("W czym moge pomoc?")
        print("1. Dodaj ksiazke")
        print("2. Wypozycz ksiazke")
        print("3. Zwroc ksiazke")
        print("4. Wyswietl historie ksiazki")
        print("5. Wyjscie")

        wybor = input("Wybierz opcje: ")

        if wybor == "1":
            dodaj_ksiazke()
        elif wybor == "2":
            wypozycz_ksiazke()
        elif wybor == "3":
            zwroc_ksiazke()
        elif wybor == "4":
            wyswietl_historie_ksiazki()
        elif wybor == "5":
            print("Do widzenia")
            break
        else:
            print("Nieprawidlowy wybor. Sprobuj ponownie.")


if __name__ == "__main__":
    main()
