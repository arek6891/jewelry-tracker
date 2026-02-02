# README (Agent Context)

## Status Projektu
Projekt jest w fazie **Production Ready**. Działa stabilnie, posiada system haseł, alertów, benchmarków i historii.

## Kontekst Techniczny
-   **Katalog Roboczy**: `c:\Users\asobczyk\OneDrive - Logwin AG\Bee_app_displays`
-   **Język**: Python 3.13
-   **Framework**: Flask
-   **Baza**: SQLite (`instance/jewelry.db`)

## Ważne Pliki
-   `app.py`: Cała logika backendu.
-   `fix_db.py`: Skrypt ratunkowy do dodawania kolumn do bazy.
-   `docs/`: Folder z dokumentacją dla użytkownika.

## 🛠️ Development Workflow (Rules)
-   **Git & GitHub (CRITICAL)**:
    -   ALWAYS initialize Git and push changes to GitHub after work.
    -   Remote: `https://github.com/arek6891/jewelry-tracker`
    -   **Rule**: Every feature completion or major update must be committed and pushed immediately.
-   **Tools**: Flask (Backend), Pandas (Analytics), Tailwind (UI).

## Do Zrobienia (Roadmapa)
1.  **Deploy**: Jeśli użytkownik poprosi o dostęp dla innych osób, trzeba rozważyć hostowanie w sieci lokalnej (LAN) logwin.
2.  **Backup**: Automatyczny backup bazy danych `jewelry.db`.
