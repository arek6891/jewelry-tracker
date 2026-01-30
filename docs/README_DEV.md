# README (Agent Context)

## Status Projektu
Projekt jest w fazie **MVP (Minimum Viable Product)**. Działa stabilnie na lokalnej maszynie użytkownika.

## Kontekst Techniczny
-   **Katalog Roboczy**: `c:\Users\asobczyk\OneDrive - Logwin AG\Bee_app_displays`
-   **Język**: Python 3.13
-   **Framework**: Flask
-   **Baza**: SQLite (`instance/jewelry.db`)
    -   Tabela `daily_log` ma kolumnę `quantity` (dodana przez migrację manualną).

## Ważne Pliki
-   `app.py`: Cała logika backendu.
-   `fix_db.py`: Skrypt ratunkowy do dodawania kolumn do bazy (użyj jeśli zmienisz model).
-   `docs/`: Folder z dokumentacją dla użytkownika.

## Do Zrobienia (Roadmapa)
1.  **Deploy**: Jeśli użytkownik poprosi o dostęp dla innych osób, trzeba rozważyć hostowanie w sieci lokalnej (LAN) logwin.
2.  **Bezpieczeństwo**: Hasła są w plain text. Przy wdrożeniu produkcyjnym użyć hashowania.
3.  **Alerty**: Zaimplementować wizualne alerty na dashboardzie (np. czerwony kolor gdy wydajność < 50).
