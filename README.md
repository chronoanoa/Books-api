<p align="center">
  <h1 align="center">📚 Books API</h1>
  <p align="center">Библиотека книг на Flask — быстро, минималистично, без магии.</p>
  <p align="center">
    <img src="https://img.shields.io/badge/python-3.11-3776AB?style=flat-square&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/flask-3.1-000000?style=flat-square&logo=flask&logoColor=white" />
    <img src="https://img.shields.io/badge/tests-passing-2ea043?style=flat-square" />
    <img src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square" />
  </p>
</p>

---

> RESTful API для библиотеки книг. Хранит данные в памяти, полностью покрыт тестами и открывается одной командой.

---

## ✨ Что внутри

| Возможность | Описание |
|---|---|
| 🔄 CRUD | Создание, чтение, обновление и удаление книг |
| 🩹 `PATCH` | Частичное обновление любого поля |
| 🔍 Поиск | `?title=мастер` — без учёта регистра |
| 🧪 Тесты | `pytest` + Flask `test_client` |
| 🧰 Postman | Готовая коллекция с переменными и проверками |

---

## 🗂 Структура

```text
books-api/
├── app/
│   ├── __init__.py          # фабрика приложения и регистрация Blueprint
│   ├── data.py              # хранилище книг в памяти
│   └── routes.py            # эндпоинты + общая валидация
├── postman/
│   └── books_collection.json
├── tests/
│   ├── conftest.py
│   └── test_books.py
├── requirements.txt
└── run.py
```

---

## 🚀 Быстрый старт

```bash
# 1 — клонируй и зайди в папку
git clone <repo-url> && cd books-api

# 2 — окружение
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3 — зависимости
pip install -r requirements.txt

# 4 — поехали
python run.py
```

Сервер поднимется на [`http://127.0.0.1:5000`](http://127.0.0.1:5000).

---

## 🧪 Тесты

```bash
pytest          # 16 тестов, < 1 cек
pytest -v       # с названиями
pytest --tb=short
```

---

## 🔌 Эндпоинты

| Метод | Путь | Что делает |
|---|---|---|
| `GET` | `/` | Главная страница |
| `GET` | `/books` | Все книги `{ count, books }` |
| `GET` | `/books/<id>` | Одна книга по id |
| `GET` | `/books/search?title=...` | Поиск по названию |
| `POST` | `/books` | Создать книгу |
| `PUT` | `/books/<id>` | Полное обновление |
| `PATCH` | `/books/<id>` | Частичное обновление |
| `DELETE` | `/books/<id>` | Удалить книгу |

---

## 📦 Модель

```json
{
  "id": 1,
  "title": "Мастер и Маргарита",
  "author": "Михаил Булгаков",
  "year": 1967,
  "is_available": true
}
```

| Поле | Тип | Правила |
|---|---|---|
| `title` | `string` | непустая строка |
| `author` | `string` | непустая строка |
| `year` | `int` | `>= 0`, `true`/`false` не принимаются |
| `is_available` | `boolean` | `true` или `false` |

Ошибки отдают `{"error": "..."}` с кодами `400` / `404`. Пробелы у строк отрезаются.

---

## 💡 Примеры

<details>
<summary><code>GET /books</code></summary>

```bash
curl http://127.0.0.1:5000/books
```

```json
{
  "count": 2,
  "books": [
    { "id": 1, "title": "Мастер и Маргарита", "author": "Михаил Булгаков", "year": 1967, "is_available": true },
    { "id": 2, "title": "1984", "author": "Джордж Оруэлл", "year": 1949, "is_available": false }
  ]
}
```

</details>

<details>
<summary><code>POST /books</code></summary>

```bash
curl -X POST http://127.0.0.1:5000/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Война и мир","author":"Лев Толстой","year":1869,"is_available":true}'
```

```json
{
  "message": "Книга успешно создана",
  "book": { "id": 3, "title": "Война и мир", "author": "Лев Толстой", "year": 1869, "is_available": true }
}
```

</details>

<details>
<summary><code>PATCH /books/1</code></summary>

```bash
curl -X PATCH http://127.0.0.1:5000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"is_available": false}'
```

```json
{
  "message": "Книга частично обновлена",
  "book": { "id": 1, "title": "Мастер и Маргарита", "author": "Михаил Булгаков", "year": 1967, "is_available": false }
}
```

</details>

<details>
<summary><code>GET /books/search?title=мастер</code></summary>

```bash
curl "http://127.0.0.1:5000/books/search?title=мастер"
```

```json
{ "count": 1, "books": [{ "id": 1, "title": "Мастер и Маргарита", "author": "Михаил Булгаков", "year": 1967, "is_available": true }] }
```

</details>

---

## 🧭 Postman

1. Импортируй `postman/books_collection.json`.
2. Запусти сервер (`python run.py`).
3. Жми **Send** — в коллекции уже настроены переменные `base_url` и `book_id`, созданы проверки на статусы и сохранение `id` после `POST`.

---

## 🛠 Стек

Python 3.11 · Flask 3.1 · Werkzeug · pytest 8

---

<p align="center"><sub>Сделано для людей, которые любят, когда код прост, а книги доступны.</sub></p>
