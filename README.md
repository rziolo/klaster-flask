# Klaster Flask - Etap 0: Fundamenty

## Zrealizowane zadania:
1. **Struktura folderów**: Ujednolicony podział na `etl`, `routes`, `templates` i `logs` dla każdej aplikacji.
2. **Shared Layout**: Centralny szablon `base.html` w folderze `shared` oraz ujednolicony CSS w `static`.
3. **Formatowanie**: Dodano mechanizm polskiego formatowania liczb w `shared/utils.py`.
4. **ETL Shared**: Skrypt `kursy_nbp.py` gotowy do pobierania kursów walut dla całego klastra.
5. **Separacja**: Przygotowano strukturę pod pliki `.env` dla każdej aplikacji.

## Ścieżki:
- Główne wejście: `192.168.1.156/aplikacje`
- Pliki współdzielone: `/var/www/html/flask/shared/`
- Statyczne: `/var/www/html/flask/static/`

## Następne kroki:
- Konfiguracja usług systemd dla każdej aplikacji.
- Implementacja logiki CRUD w oparciu o dostarczone schematy baz danych.
