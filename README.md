# 📚 Books API

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/flask-3.1-000000?style=flat-square&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/pytest-8-0A6EBD?style=flat-square&logo=pytest&logoColor=white" />
  <img src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square" />
</p>

REST API для библиотеки книг на Flask. Проект поддерживает CRUD, частичное обновление через PATCH, поиск по названию и покрыт автотестами с использованием Flask test client.

---

## ✨ Что внутри

| Возможность | Описание |
|---|---|
| 🔄 CRUD | Создание, чтение, обновление и удаление книг |
| 🩹 PATCH | Частичное обновление любого поля |
| 🔍 Поиск | `?title=мастер` — без учёта регистра |
| 🧪 Тесты | `pytest` + Flask `test_client` |
| 🧰 Postman | Готовая коллекция для ручного тестирования |

---

## 🗂 Структура проекта

```text
Books-api/
├── app/
│   ├── __init__.py          # фабрика приложения и регистрация Blueprint
│   ├── data.py              # хранилище книг в памяти + ID counter
│   └── routes.py            # эндпоинты и валидация
├── postman/
│   └── books_collection.json
├── tests/
│   ├── conftest.py
│   └── test_books.py
├── .gitignore
├── requirements.txt
├── README.md
├── run.py
└── venv/                   # при локальном создании окружения
```

---

## 🚀 Быстрый старт

```bash
cd "C:\Users\dodia\OneDrive\Рабочий стол\Flask\Books-api"
python -m venv venv
venv\Scripts\activate         # Windows
# source venv/bin/activate    # macOS / Linux
pip install -r requirements.txt
python run.py
```

После запуска API будет доступно по адресу `http://127.0.0.1:5000`.

---

## 🧪 Тесты

```bash
pytest
pytest -v
pytest --tb=short
```

В проекте предусмотрены проверки для: получения всех книг, поиска, создания, обновления, частичного обновления, удаления и ошибок валидации.

---

## 🔌 Эндпоинты

| Метод | Путь | Что делает |
|---|---|---|
| `GET` | `/` | Главная страница |
| `GET` | `/books` | Все книги в формате `{ count, books }` |
| `GET` | `/books/<int:book_id>` | Одна книга по `id` |
| `GET` | `/books/search?title=...` | Поиск по названию без учёта регистра |
| `POST` | `/books` | Создать книгу |
| `PUT` | `/books/<int:book_id>` | Полное обновление |
| `PATCH` | `/books/<int:book_id>` | Частичное обновление |
| `DELETE` | `/books/<int:book_id>` | Удалить книгу |

---

## 📦 Модель данных

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
| `year` | `int` | целое число `>= 0`, не допускается `bool` |
| `is_available` | `boolean` | `true` или `false` |

При ошибках API возвращает JSON вида `{"error": "..."}` с кодами `400` / `404`. Пробелы вокруг строк автоматически обрезаются.

---

## 💡 Примеры запросов

### GET /books

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

### POST /books

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

### PATCH /books/1

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

### GET /books/search?title=мастер

```bash
curl "http://127.0.0.1:5000/books/search?title=мастер"
```

```json
{
  "count": 1,
  "books": [
    { "id": 1, "title": "Мастер и Маргарита", "author": "Михаил Булгаков", "year": 1967, "is_available": true }
  ]
}
```

---

## 🧭 Postman

1. Импортируйте файл `postman/books_collection.json`.
2. Запустите сервер командой `python run.py`.
3. Нажмите **Send** — в коллекции уже настроены переменные и базовые проверки статусов.

> В проекте есть отдельный набор тестов для Flask, а коллекция Postman служит удобным способом ручной проверки эндпоинтов.

---

## 🛠 Технические особенности

- Приложение построено на паттерне Flask application factory и Blueprint.
- Данные хранятся в памяти, поэтому после перезапуска сервера список книг сбрасывается.
- Для валидации используются проверки типов, непустых строк, допустимых значений `year` и `is_available`.
- В `run.py` включён режим отладки (`debug=True`), что удобно для разработки, но для продакшена стоит отключить.
- Postman-коллекция в проекте является рабочим шаблоном для проверки API локально.

---

## ✅ Итог

Проект представляет собой компактный и понятный REST API для управления библиотекой книг. Он легко запускается, хорошо покрыт тестами и подходит как основа для дальнейшего расширения функциональности.

<p align="center"><sub>Сделано для людей, которые любят, когда код прост, а книги доступны.</sub></p>

