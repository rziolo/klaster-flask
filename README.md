# Klaster Flask - Dokumentacja

## Zrealizowane zadania:

### Etap 0: Fundamenty
1. **Struktura folderów**: Ujednolicony podział na `etl`, `routes`, `templates` i `logs`.
2. **Shared Layout**: Centralny szablon `base.html` w folderze `shared` (zintegrowany z Bootstrap 5 i FontAwesome).
3. **Formatowanie**: Mechanizm polskiego formatowania liczb i walut.
4. **ETL Shared**: Skrypt `kursy_nbp.py` dla całego klastra.

### Etap 1: Moduł Zdrowie (ha_vita_pressure) - DZISIAJ
1. **Pełny CRUD**: Implementacja odczytu, tworzenia, edycji i usuwania pomiarów ciśnienia.
2. **Integracja IoT**: 
   - Automatyczne pobieranie geolokalizacji z **Home Assistant API**.
   - Pobieranie danych pogodowych (ciśnienie, temperatura, wilgotność) z **OpenWeatherMap API**.
   - Funkcja "Wprowadź" automatycznie uzupełniająca formularz danymi z czujników.
3. **Interfejs użytkownika**:
   - Tabela z rozdzielonymi parametrami SYS/DIA/Puls.
   - Dynamiczne kolorowanie wartości i nowoczesne ikony akcji (FontAwesome).
   - Szary panel podglądu parametrów otoczenia w formularzu.
4. **Moduł raportowania**: Dedykowany szablon wydruku (Print-ready HTML) zoptymalizowany pod format A4.

## Ścieżki:
- Główne wejście: `192.168.1.156/aplikacje`
- Moduł Zdrowie: `192.168.1.156/zdrowie/pressure_list`
- Pliki współdzielone: `/var/www/html/flask/shared/`

## Następne kroki:
- Implementacja kolejnych modułów zdrowotnych (np. wykresy trendów ciśnienia).
- Migracja pozostałych aplikacji do nowej struktury klastra.
- Automatyzacja backupów bazy danych MySQL.
