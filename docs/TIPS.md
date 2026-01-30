# Tipy i Instrukcja Uruchomienia

## 🚀 Jak Uruchomić Aplikację
1.  Otwórz terminal (PowerShell lub CMD).
2.  Przejdź do folderu projektu:
    ```powershell
    cd "c:\Users\asobczyk\OneDrive - Logwin AG\Bee_app_displays"
    ```
3.  Uruchom serwer:
    ```powershell
    python app.py
    ```
4.  Otwórz przeglądarkę i wejdź na adres:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🔑 Dane Logowania
-   **Login**: `admin`
-   **Hasło**: `logwin`

## 💡 Tipy dla Ciebie (Użytkownika)
-   **Export Excel**: Przycisk znajduje się na stronie "History" u góry. Raport zawiera wszystkie logi.
-   **Wykresy**: Aktualizują się automatycznie po dodaniu wpisu. Jeśli wykres jest pusty, dodaj pierwszy log z ilością > 0.
-   **Brak Internetu**: Aplikacja działa lokalnie, nie potrzebuje internetu (poza pobraniem stylów Tailwind przy pierwszym uruchomieniu, potem są one w cache przeglądarki, choć najlepiej mieć dostęp).

## 🛠 Tipy Techniczne (Dla Developera/AI)
## 4. Technical Concepts 🧠

### Regression Analysis (Admin Panel)
- **Logic**: We use Least Squares Regression (`numpy.linalg.lstsq`) to separate the contribution of Men vs Women.
- **Equation**: `(MenCount * M_Rate) + (WomenCount * W_Rate) = TotalQuantity`.
- **Note**: This requires at least 2 log entries with different staff compositions to solve accurately. More data = better accuracy.

### Database Migrations
- **Current Strategy**: `init_db()` checks for table existence.
- **New Columns**: We manually handle column additions (e.g., `completion_notes`) using `sqlite3` raw SQL in `init_db`.
- **Recommendation**: For future complex changes, switch to `Flask-Migrate` (Alembic).

### Production Deployment 🚀
- **WSGI**: Don't run `python app.py` in production. Use `gunicorn` or `waitress` (Windows).
    ```bash
    pip install waitress
    waitress-serve --port=8080 app:app
    ```
- **Security**:
    - Change `SECRET_KEY` in `app.py`.
    - Ensure `debug=False`.
    - Use HTTPS (reverse proxy via Nginx/IIS).

## 5. Security Note 🔐
- **Passwords**: Currently stored as **hashed PBKDF2** (Good!).
- **Admin Access**: `/admin/*` routes are protected by `@login_required` and `role == 'admin'` check.

-   **Port**: Serwer działa na porcie 5000. Jeśli zajęty, zmień w `app.run(port=...)`.
