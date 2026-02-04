# Dziennik Zmian (Changelog)

## [1.1.0] - 2026-02-04
### Added
- **Parts Stock (Inventory) Module**:
    - Complete material tracking system.
    - Component management (SKU, Name, Unit).
    - Excel Import (Add-only mode with user tracking).
    - Bill of Materials (BOM) configuration.
    - Automatic stock deduction on production log.
    - Admin manual correction with reason logging.
    - History log of all stock movements.
- **Dark Mode**: Full implementation with toggle and persistence.
- **Calendar**: Fixed 404 error on calendar route.

### Changed
- UI updated to support Dark Mode across all templates.
- Navigation bar updated with Parts Stock link.

## [1.0.0] - 2026-01-30
### Dodano
-   Inicjalizacja projektu w technologii Python (Flask) [Zastępstwo za Node.js].
-   **Baza Danych**: Utworzenie tabel `User`, `Action`, `DailyLog` w SQLite.
-   **Autoryzacja**: System logowania (Domyślne konto: `admin` / `admin`).
-   **Dashboard**:
    -   Liczniki: Total Quantity, Total Staff, Productivity.
    -   Wykres: Tygodniowa produkcja (Bar chart) + Wydajność (Line chart).
### [1.0.1] - 2026-02-02
### Changed
-   **Dashboard**:
    -   Restored "TV Mode" button to navbar.
    -   Fixed layout issues where Alerts and Projects were overlapping.
    -   Improved button alignment and responsive behavior.
-   **Quality Check (QC)**:
    -   Refactored `qc_project.html` to use Tabs ("New Inspection" vs "Reference Templates").
    -   Separated upload functionality from read-only template viewing.

### Added
-   **Templates Tab**: New view in QC screen for users to see reference images without editing controls.
-   **LAN Access**: Added `run_lan.py` and documentation to easily run the app on the local network (Intranet).

## [1.0.0] - 2026-01-30
- **Admin Benchmark Panel**:
    - Admin-only route `/admin/benchmarks`.
    - Interface to set "Target Productivity" (Towers/Day) for Men and Women.
    - Regression Logic (Least Squares) to calculate "Actual Productivity" from historical logs.
- **Project Notes System**:
    - `ProjectNote` database model.
    - "📝 Notes" button on Dashboard for active projects.
    - Full conversation history in "Archived History" view.
- **Copyright Footer**: Added legal copyright notice to `base.html`.
- **Project History**:
    - Dedicated page to view archived projects.
    - Status tracking (On Time vs Delayed).

### Changed
- **Dashboard**: Added links to Admin Panel and simplified button layout.
- **Database**: Added `benchmark_config` and `project_note` tables.

### Fixed
- **Mobile Responsiveness**: Improved table scrolling on small screens.
- **Completion Modal**: Fixed z-index and event handling issues.
-   **Formularz**: Dodanie pola `quantity` (ilość wież) do formularza logowania.
-   **Historia**: Tabela wpisów z filtrowaniem (ostatnie wpisy).
-   **Export**: Endpoint `/export` generujący raport Excel.

### Zmieniono
-   Aktualizacja schematu bazy danych (migracja): dodanie kolumny `quantity` do tabeli `daily_log` w celu śledzenia outputu.
