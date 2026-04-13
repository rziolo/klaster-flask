# Klaster Flask - Dokumentacja

## Zrealizowane zadania:

### Etap 0: Fundamenty (System-Wide)
1. **Dynamiczna Fabryka Aplikacji**: Ujednolicony `app.py` obsługujący dynamiczne ładowanie modułów (`inwestycje`, `zdrowie`, `finanse`) bez konfliktów tras.
2. **Struktura folderów**: Ujednolicony podział na `etl`, `routes`, `templates` i `logs` w każdym module.
3. **Shared Layout**: Centralny szablon `base.html` w folderze `shared` (zintegrowany z Bootstrap 5 i FontAwesome).
4. **Modułowa logika**: Wydzielenie procesów pomocniczych do plików `utils.py` dla lepszej czytelności kodu.

### Etap 1: Moduł Zdrowie (ha_vita_pressure)
1. **Pełny CRUD**: Implementacja odczytu, tworzenia, edycji i usuwania pomiarów ciśnienia.
2. **Integracja IoT**: Automatyczne pobieranie danych pogodowych i geolokalizacji.
3. **Raporty**: Szablon wydruku zoptymalizowany pod A4 dla lekarza.

### Etap 2: Moduł Finanse (Home Budget)
1. **Ewidencja ROR, Wydatków i Przychodów**: Pełne zarządzanie finansami domowymi z przelicznikiem walut.
2. **Analiza Samochodowa**: Raport zużycia paliwa i kosztów eksploatacji (PLN/km).
3. **Bilans**: Zestawienie miesięczne przychodów i wydatków z narastającym saldem majątku.

### Etap 3: Moduł Inwestycje (Stock Portfolio) - AKTUALIZACJA
1. **Zarządzanie Portfelem (Obroty)**:
   - Implementacja logicznego podziału na **Pozycje Bieżące** (otwarte) oraz pełną **Historię**.
   - Sortowanie dynamiczne: widok bieżący sortowany alfabetycznie po Tickerze (`ASC`), historia po dacie zakupu.
   - Zaawansowane formatowanie walutowe (PLN) w tabelach i widokach szczegółowych.
2. **Ujednolicenie Słowników (UI/UX)**:
   - Wprowadzenie list rozwijanych (**Dropdown**) dla pól Ticker i Platforma we wszystkich formularzach CRUD.
   - Dynamiczne pobieranie dostępnych rynków i platform bezpośrednio z bazy danych.
3. **System Monitoringu ETL**:
   - Dashboard aktualności danych bazujący na skanowaniu plików CSV (`import_gpw`, `import_zagr`, `stooq`).
   - Dynamiczne statusy kolorystyczne (Zielony/Czerwony) w zależności od daty ostatniego importu.
4. **Interaktywny Podgląd Danych**:
   - Funkcja `get_csv_preview_html`: Podgląd surowych plików importu bezpośrednio w oknie modalnym.
   - Integracja z bazą MySQL dla tabel `dane` (historyczne) i `dane_dzienne`.

## Ścieżki:
- Główne wejście (Menu): `192.168.1.156/aplikacje`
- Moduł Zdrowie: `192.168.1.156/zdrowie`
- Moduł Finanse: `192.168.1.156/finanse`
- Moduł Inwestycje: `192.168.1.156/inwestycje`

## Następne kroki:
- Automatyzacja backupów bazy danych MySQL dla wszystkich modułów.
- Implementacja wykresów trendów (Chart.js) dla notowań giełdowych.
- Rozszerzenie ETL o automatyczne pobieranie danych ze Stooq API.
