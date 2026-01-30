# 💎 Jewelry Tower Tracker - Project Information

## Cel Projektu
Aplikacja zastępująca ręczne wpisywanie danych do Excela. Służy do monitorowania ilości zmontowanych wież z biżuterią, zarządzania personelem i śledzenia wydajności (Towers per Person) w czasie rzeczywistym.

## Główne Funkcje
-   **Core**:
  - User Authentication (Login/Register/Logout).
  - Personnel Management (Men/Women/Mixed Teams).
  - Activity Logging (Folding, QC, Packaging).
- **Advanced Productivity**:
  - **Dynamic Targets**: Set daily output goals per person type (Men vs Women).
  - **Regression Analysis**: System calculates *actual* productivity from historical data.
  - **Smart Alerts**: Dashboard warns if current run rate is insufficient to meet deadlines.
- **Project Management**:
  - **Project Goals**: Define target quantity and deadline.
  - **Visual Timeline**: Daily progress visualization.
  - **Notes System**: Full conversation history for every project.
  - **History Archive**: Track on-time performance and delays.
- **Reporting**:
  - Export to Excel.
  - Interactive Charts (Weekly Output, Productivity Trends).

## Stack Technologiczny
-   **Backend**: Python 3 (Flask)
-   **Baza Danych**: SQLite (lokalny plik `instance/jewelry.db`)
-   **Frontend**: HTML, Tailwind CSS (CDN), Vanilla JS
-   **Export**: Pandas + OpenPyXL

## Struktura Plików
-   `app.py`: Główna logika aplikacji, routing i modele bazy danych.
-   `templates/`: Pliki HTML (widoki).
-   `static/`: Pliki CSS/JS (obecnie puste, style są w HTML).
-   `instance/jewelry.db`: Baza danych.
