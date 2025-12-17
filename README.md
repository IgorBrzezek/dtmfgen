# DTMF WAV Generator — README

## Spis treści
- [Opis projektu](#opis-projektu)
- [Najważniejsze funkcje](#najważniejsze-funkcje)
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Szybki start](#szybki-start)
- [Tryby pracy](#tryby-pracy)
  - [Tryb pojedynczego pliku](#tryb-pojedynczego-pliku)
  - [Tryb wsadowy (CSV)](#tryb-wsadowy-csv)
- [Parametry wiersza poleceń](#parametry-wiersza-poleceń)
- [Format pliku CSV](#format-pliku-csv)
- [Przykłady użycia](#przykłady-użycia)
- [Jak to działa — w skrócie](#jak-to-działa--w-skrócie)
- [Dobre praktyki i wskazówki](#dobre-praktyki-i-wskazówki)
- [Rozwiązywanie problemów](#rozwiązywanie-problemów)
- [FAQ](#faq)
- [Informacje o projekcie](#informacje-o-projekcie)
- [Licencja](#licencja)

---

## Opis projektu
**DTMF WAV Generator** to narzędzie konsolowe do generowania plików audio (WAV) z tonami DTMF (Touch-Tone), używanymi w telefonii. Umożliwia tworzenie sekwencji tonów dla cyfr `0–9`, znaków specjalnych `*` i `#`, a także klawiszy rozszerzonych `A–D`. Program może działać zarówno w trybie pojedynczej generacji, jak i w trybie wsadowym na podstawie pliku CSV.

## Najważniejsze funkcje
- Generowanie tonów DTMF dla pełnego zestawu klawiszy (0–9, *, #, A–D).
- Zapis do formatu **WAV** w konfiguracji: **mono**, **16-bit**, regulowany **sampling rate**.
- Regulacja **długości tonu** i **przerw (ciszy)** między kolejnymi znakami.
- Obsługa **nadpisywania** istniejących plików lub bezpieczne pomijanie.
- **Tryb wsadowy**: przetwarzanie wielu pozycji z pliku CSV.
- Czytelne komunikaty o postępie, czasie generacji i rozmiarze pliku.

## Wymagania
- **Python 3.8+** (zalecana wersja 3.10 lub nowsza).
- Standardowe biblioteki Pythona (brak dodatkowych zależności): `argparse`, `wave`, `math`, `struct`, `os`, `sys`, `time`.
- System operacyjny: Windows, macOS lub Linux.

## Instalacja
1. Skopiuj plik `dtmfgen.py` do wybranego katalogu projektu.
2. Upewnij się, że masz zainstalowany Python 3.8+ i uruchomienie skryptów z wiersza poleceń jest możliwe.

> **Uwaga:** Na systemach Unix warto nadać plikowi prawa wykonywania: `chmod +x dtmfgen.py`.

## Szybki start
Najprostsze uruchomienie (domyślne ustawienia czasu trwania tonu i przerwy):
```bash
python dtmfgen.py -DIAL 123
```
Wynikiem będzie plik `dialed.wav` w bieżącym katalogu.

## Tryby pracy
### Tryb pojedynczego pliku
W tym trybie podajesz sekwencję do wybicia (dialingu). Możesz dostosować nazwę wyjściowego pliku, czas trwania tonu, długość ciszy i częstotliwość próbkowania.

### Tryb wsadowy (CSV)
Umożliwia przetworzenie wielu wpisów z przygotowanego pliku tekstowego w formacie CSV. Każdy wiersz opisuje jeden docelowy plik WAV i parametry generacji.

## Parametry wiersza poleceń
- `-DIAL <SEKWENCJA>` — sekwencja znaków do wygenerowania. Dozwolone: cyfry `0–9`, `*`, `#`, `A–D`. Dopuszczalne są przecinki w celu grupowania; podczas generacji są ignorowane.
- `-o, --output <PLIK>` — nazwa pliku wyjściowego (domyślnie `dialed.wav`).
- `-t, --tone <SEK>` — czas trwania pojedynczego tonu w sekundach (domyślnie `0.2`).
- `-s, --silence <SEK>` — długość ciszy pomiędzy kolejnymi znakami w sekundach (domyślnie `0.1`).
- `--freq <HZ>` — częstotliwość próbkowania (domyślnie `44100`).
- `--overwrite` — nadpisywanie istniejących plików bez pytania.
- `--list <PLIK_CSV>` — ścieżka do pliku CSV dla przetwarzania wsadowego.
- `-h` — skrócona pomoc (zwięzłe użycie).
- `--help` — pełna dokumentacja w konsoli (rozszerzony opis, przykłady).

## Format pliku CSV
W trybie wsadowym każdy wiersz ma cztery pola oddzielone przecinkami:
```
<plik_wyjściowy>, <sekwencja>, <czas_tonu>, <czas_ciszy>
```
**Przykład:**
```
dial1.wav, 12345, 0.2, 0.1
moj_numer.wav, 060123456, 0.5, 0.2
```
Linie puste oraz linie zaczynające się od `#` są ignorowane.

## Przykłady użycia
- **Domyślne czasy i nazwa pliku:**
  ```bash
  python dtmfgen.py -DIAL 1,2,3
  ```
- **Własna nazwa i nadpisywanie:**
  ```bash
  python dtmfgen.py -DIAL 060123456 -o dialed.wav --overwrite
  ```
- **Dłuższe tony i przerwy:**
  ```bash
  python dtmfgen.py -DIAL *#90A -t 0.5 -s 0.2
  ```
- **Tryb wsadowy z CSV:**
  ```bash
  python dtmfgen.py --list lista.csv
  ```

## Jak to działa — w skrócie
- Każdy znak sekwencji jest mapowany na parę częstotliwości DTMF (jedna z grupy niskiej, druga z wysokiej). Program sumuje dwie sinusoidy, normalizuje amplitudę i zapisuje wynik jako 16‑bitowe próbki mono.
- Długość tonu (`-t`) określa liczbę generowanych próbek dla danego znaku, a długość ciszy (`-s`) wstawia przerwy między kolejnymi znakami (nie dodaje ciszy po ostatnim znaku).
- Plik wynikowy jest tworzony w formacie WAV z podanym `--freq` (domyślnie 44,1 kHz).

## Dobre praktyki i wskazówki
- **Unikaj przesterowania**: pozostaw standardową amplitudę i nie modyfikuj kodu zwiększając poziomy — pliki będą kompatybilne z większością odtwarzaczy.
- **Spójne czasy**: dla symulacji wybierania numerów telefonicznych typowe wartości to 0.2 s dla tonu i 0.1 s dla przerwy.
- **Czytelne sekwencje**: możesz używać przecinków do grupowania cyfr; program i tak je usunie.
- **Nazewnictwo plików**: dla wsadów używaj jednoznacznych nazw, np. `client01.wav`, `client02.wav`.

## Rozwiązywanie problemów
- *„Plik już istnieje”*: użyj `--overwrite`, lub podaj inną nazwę przez `-o`.
- *„Błąd: You must provide -DIAL sequence or a --list file.”*: uruchom z parametrem `-DIAL` albo `--list`.
- *„Error: List file '<nazwa>' not found.”*: sprawdź ścieżkę do pliku CSV.
- *„Skipping invalid line” w trybie wsadowym*: upewnij się, że wiersz CSV ma 4 pola i poprawne wartości liczbowe dla czasu.
- Plik wynikowy jest pusty lub za krótki: sprawdź wartości `-t`, `-s` i `--freq`.

## FAQ
**Czy mogę użyć znaków innych niż 0–9, *, #, A–D?**
Nie, generator wspiera wyłącznie standardowy zestaw DTMF.

**Czy mogę zmienić głośność?**
Głośność jest stała (maksymalna dla 16‑bit), aby zachować zgodność i uniknąć zniekształceń; w razie potrzeby zmień poziom głośności w odtwarzaczu lub edytorze audio.

**Czy powstaje cisza po ostatnim znaku?**
Nie, cisza jest wstawiana tylko pomiędzy kolejnymi znakami sekwencji.

## Informacje o projekcie
- Autor: Igor Brzeżek
- Wersja: 1.1.0 (17.12.2025)
- Kontakt: igor.brzezek@gmail.com
- Strona: https://github.com/IgorBrzezek

## Licencja
Jeżeli nie określono inaczej, projekt jest udostępniany na zasadach standardowej licencji autora. W przypadku potrzeby publikacji lub modyfikacji, skontaktuj się z autorem.
