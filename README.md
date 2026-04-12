# Klaster Flask - Dokumentacja

## Zrealizowane zadania:

### Etap 0: Fundamenty
1. **Struktura folderów**: Ujednolicony podział na `etl`, `routes`, `templates` i `logs`.
2. **Shared Layout**: Centralny szablon `base.html` w folderze `shared` (zintegrowany z Bootstrap 5 i FontAwesome).
3. **Formatowanie**: Mechanizm polskiego formatowania liczb i walut.
4. **ETL Shared**: Skrypt `kursy_nbp.py` dla całego klastra.

### Etap 1: Moduł Zdrowie (ha_vita_pressure)
1. **Pełny CRUD**: Implementacja odczytu, tworzenia, edycji i usuwania pomiarów ciśnienia.
2. **Integracja IoT**:
   - Automatyczne pobieranie danych pogodowych i geolokalizacji.
   - Funkcja "Wprowadź" uzupełniająca dane z czujników.
3. **Moduł raportowania**: Dedykowany szablon wydruku zoptymalizowany pod format A4.

### Etap 2: Moduł Finanse (Home Budget) - DZISIAJ
1. **Migracja Architektury**:
   - Przeniesienie logiki do fabryki aplikacji (`create_app`).
   - Implementacja wielofolderowego systemu szablonów (`ChoiceLoader`) łączącego zasoby lokalne i współdzielone.
2. **Kompletna ewidencja (CRUD)**:
   - **Stan Kont (ROR)**: Zarządzanie saldami bankowymi, lokatami, obligacjami oraz walutami (EUR/USD) z przelicznikiem kursów.
   - **Wydatki**: Rozbudowana ewidencja z podziałem na żywność, opłaty, medycynę i koszty auta.
   - **Przychody**: Rejestracja wpływów z ZUS, giełdy, odsetek i urzędów.
3. **Zaawansowana Analiza i Raporty**:
   - **Bilans Miesięczny**: Automatyczne zestawienie przychodów vs wydatków oraz narastający stan majątku (ROR).
   - **Koszty Samochodu**: Raport zużycia paliwa, przebiegu oraz kosztu eksploatacji na 1 km.
4. **Interfejs Użytkownika**:
   - Kompaktowy, responsywny Dashboard (`index.html`) z szybkim dostępem do danych i analiz.
   - Excelowy styl tabel z polskim formatowaniem walut (spacja jako separator, przecinek dla groszy).
   - Modale dla uwag tekstowych w celu zachowania czytelności tabel.

## Ścieżki:
- Główne wejście (Menu): `192.168.1.156/aplikacje`
- Moduł Zdrowie: `192.168.1.156/zdrowie/pressure_list`
- Moduł Finanse: `192.168.1.156/finanse`
- Pliki współdzielone: `/var/www/html/flask/shared/`

## Następne kroki:
- Automatyzacja backupów bazy danych MySQL dla wszystkich modułów.
- Implementacja wykresów trendów (Chart.js) w module Bilansu.
- Rozbudowa modułu inwestycyjnego o dane giełdowe online.
