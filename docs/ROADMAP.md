# 🗺️ Product Roadmap

## 1. Moduł Kontroli Jakości (QA) oparty na Zdjęciach
System weryfikacji jakości montażu na podstawie przesyłanych zdjęć.
- **Statusy**: Każde zdjęcie otrzymuje status: `Oczekuje`, `Zatwierdzone`, `Odrzucone`.
- **Workflow**:
    - Pracownik przesyła zdjęcie (już zaimplementowane).
    - Lider/QC przegląda galerię i ocenia jakość.
    - W przypadku odrzucenia: wymóg wpisania powodu (np. "Brak etykiety", "Złe złożenie").
- **Raportowanie**: Wyliczanie wskaźnika jakości (% odrzutów) per pracownik lub per zmiana.

## 2. Magazyn Komponentów (Inventory)
Automatyczne śledzenie zużycia materiałów na podstawie zaraportowanej produkcji.
- **Bill of Materials (BOM)**: Definicja z czego składa się produkt (np. 1 wieża = 1 podstawa + 4 haczyki).
- **Automatyzacja**: Raport produkcji (np. +100 wież) automatyczniedejmuje odpowiednią ilość komponentów ze stanu.
- **Alerty Niskiego Stanu**: Powiadomienie (email/dashboard), gdy zapas wystarczy na mniej niż X dni produkcji (uwzględniając aktualne tempo).

## 3. TV Mode & Grywalizacja (Next Up 🚀)
Specjalny widok na duży ekran (telewizor) umieszczony na hali produkcyjnej.
- **Cel**: Motywacja zespołu i transparentność postępów w czasie rzeczywistym.
- **Funkcje**:
    - **Wielkie Liczby**: Aktualny wynik vs Cel Dzienny.
    - **Pasek Postępu**: Wizualizacja % wykonania normy.
    - **Live Pace**: Aktualna prędkość (sztuki/godzinę) vs wymagana prędkość.
    - **Efekty Wizualne**: Zmiana kolorów (Czerwony/Zielony) w zależności od realizacji planu.
    - **Auto-Refresh**: Automatyczne odświeżanie danych co 30-60 sekund bez ingerencji użytkownika.
