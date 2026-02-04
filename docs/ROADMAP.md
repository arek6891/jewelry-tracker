# 🗺️ Product Roadmap

> Ostatnia aktualizacja: 2026-02-04

---

## 📋 Istniejące Plany

### 1. Moduł Kontroli Jakości (QA) oparty na Zdjęciach
System weryfikacji jakości montażu na podstawie przesyłanych zdjęć.
- [ ] **Statusy**: Każde zdjęcie otrzymuje status: `Oczekuje`, `Zatwierdzone`, `Odrzucone`.
- [ ] **Workflow**:
    - Pracownik przesyła zdjęcie (już zaimplementowane).
    - Lider/QC przegląda galerię i ocenia jakość.
    - W przypadku odrzucenia: wymóg wpisania powodu (np. "Brak etykiety", "Złe złożenie").
- [ ] **Raportowanie**: Wyliczanie wskaźnika jakości (% odrzutów) per pracownik lub per zmiana.

### 2. Magazyn Komponentów (Inventory)
Automatyczne śledzenie zużycia materiałów na podstawie zaraportowanej produkcji.
- [ ] **Bill of Materials (BOM)**: Definicja z czego składa się produkt (np. 1 wieża = 1 podstawa + 4 haczyki).
- [ ] **Automatyzacja**: Raport produkcji (np. +100 wież) automatycznie odejmuje odpowiednią ilość komponentów ze stanu.
- [ ] **Alerty Niskiego Stanu**: Powiadomienie (email/dashboard), gdy zapas wystarczy na mniej niż X dni produkcji.

### 3. TV Mode & Grywalizacja (Next Up 🚀)
Specjalny widok na duży ekran (telewizor) umieszczony na hali produkcyjnej.
- [ ] **Wielkie Liczby**: Aktualny wynik vs Cel Dzienny.
- [ ] **Pasek Postępu**: Wizualizacja % wykonania normy.
- [ ] **Live Pace**: Aktualna prędkość (sztuki/godzinę) vs wymagana prędkość.
- [ ] **Efekty Wizualne**: Zmiana kolorów (Czerwony/Zielony) w zależności od realizacji planu.
- [ ] **Auto-Refresh**: Automatyczne odświeżanie danych co 30-60 sekund.

---

## 📊 Nowe Funkcje - Raporty i Statystyki

- [ ] Nowe typy raportów (dzienny, tygodniowy, miesięczny)
- [ ] Rozbudowane statystyki i wykresy wydajności
- [ ] Porównanie wydajności między zespołami
- [ ] Trendy produkcji w czasie

---

## 🔔 Powiadomienia

- [ ] Powiadomienia push w przeglądarce
- [ ] Powiadomienia email (np. opóźnienia w projektach)
- [ ] Alerty SMS dla krytycznych zdarzeń

---

## 📱 Widok Mobilny

- [ ] Dedykowany widok dla tabletów (touch-friendly)
- [ ] Progresywna aplikacja webowa (PWA)
- [ ] Tryb offline z synchronizacją

---

## 🎨 Ulepszenia UX/UI

### Wygląd
- [x] Ciemny motyw (Dark Mode) ✅
- [ ] Personalizacja kolorów i motywów
- [ ] Lepsze animacje i przejścia

### Responsywność
- [ ] Poprawiona responsywność na tabletach
- [ ] Optymalizacja dla różnych rozdzielczości
- [ ] Lepsze wyświetlanie tabel na małych ekranach

### Użyteczność
- [ ] Skróty klawiaturowe
- [ ] Quick actions (szybkie akcje z dashboardu)
- [ ] Undo/Redo dla ostatnich operacji

---

## 🔗 Integracje

### Eksport Danych
- [ ] Eksport do Google Sheets
- [ ] Eksport do CSV
- [ ] Automatyczny backup do chmury

### Systemy Zewnętrzne
- [ ] Integracja z systemami ERP
- [ ] API REST dla zewnętrznych aplikacji
- [ ] Webhook dla automatyzacji

---

## 🔒 Bezpieczeństwo

### Zarządzanie Użytkownikami
- [ ] Role użytkowników (admin/supervisor/worker)
- [ ] Zarządzanie uprawnieniami per funkcja
- [ ] Ograniczenie dostępu do danych wg zespołu

### Audyt i Zgodność
- [ ] Logi audytu (kto, co, kiedy zmieniał)
- [ ] Historia zmian w projektach
- [ ] Backup automatyczny bazy danych

### Uwierzytelnianie
- [ ] Silniejsze szyfrowanie haseł (bcrypt)
- [ ] Wymuszenie zmiany hasła przy pierwszym logowaniu
- [ ] Opcjonalne 2FA (dwuskładnikowe uwierzytelnianie)

---

## ✅ Rozbudowa Quality Check (Moduł QC)

### Inspekcje
- [ ] Szablony inspekcji per typ produktu
- [ ] Lista kontrolna (checklist) dla inspektorów
- [ ] Podpis cyfrowy inspektora

### Zdjęcia i Dokumentacja
- [ ] Galeria zdjęć z historią inspekcji
- [ ] Porównanie zdjęć "przed/po"
- [ ] AI do analizy zdjęć (wykrywanie defektów)

### Raporty QC
- [ ] Raport z inspekcji (PDF)
- [ ] Statystyki jakości per projekt
- [ ] Trendy jakości w czasie

---

## 🚀 Wydajność i Infrastruktura

### Optymalizacja
- [ ] Cache dla często używanych danych
- [ ] Lazy loading dla dużych list
- [ ] Kompresja odpowiedzi serwera

### Deployment
- [ ] Skrypt do produkcyjnego uruchomienia (Gunicorn/uWSGI)
- [ ] Docker container
- [ ] Dokumentacja wdrożenia na serwerze

---

## 📝 Legenda Priorytetów

| Priorytet | Opis |
|-----------|------|
| 🔴 Wysoki | Krytyczne dla biznesu, pilne |
| 🟡 Średni | Ważne ulepszenia, do zrobienia wkrótce |
| 🟢 Niski | Nice-to-have, na przyszłość |

---

## 📅 Historia Zmian Roadmapy

| Data | Zmiana |
|------|--------|
| 2026-02-04 | Dark Mode - dodano ciemny motyw ze switchem w nawigacji i zapisem preferencji |
| 2026-02-04 | Rozbudowa roadmapy o nowe kategorie: UX/UI, bezpieczeństwo, integracje, wydajność |
| - | Utworzenie początkowej wersji z modułami QA, Inventory, TV Mode |
