Project: Books RESTful API
A Python Flask-based RESTful API for managing a book library, located in C:\Users\dodia\OneDrive\Рабочий стол\Flask\Books-api. It is a Git repository.

📁 Project Structure
Books-api/
├── app/
│   ├── __init__.py    # Flask app factory & Blueprint registration
│   ├── data.py        # In-memory book storage + ID counter
│   └── routes.py      # API endpoints (GET/POST/PUT/PATCH/DELETE + search)
├── postman/
│   └── books_collection.json   # Postman collection export (placeholder/skeleton)
├── .gitignore
├── requirements.txt
├── README.md
└── run.py             # Entry point


🛠 Tech Stack
Language: Python 3.11.9 (installed on your machine)
Framework: Flask 3.1.3 (with Werkzeug, Jinja2, etc. pinned in requirements.txt)
Architecture pattern: Application factory (create_app) + Blueprints (books_bp)
Storage: In-memory Python list (no database)
Testing: Postman collection (currently a skeleton — most requests point to postman-echo.com, not the local API)

🔌 API Endpoints (defined in app/routes.py)
| Method | Route | Purpose |
|--------|-------|---------|
| GET | / | Home page ("Главная страница библиотеки") |
| GET | /books | List all books (returns count + array) |
| GET | /books/<int:book_id> | Get a single book by ID (404 if missing) |
| POST | /books | Create a book — validates title, author, year (positive int), is_available (bool) → 201 |
| PUT | /books/<int:book_id> | Full update — all fields required |
| PATCH | /books/<int:book_id> | Partial update — at least one allowed field required |
| DELETE | /books/<int:book_id> | Delete a book |
| GET | /books/search?title=<query> | Case-insensitive substring search by title |

📚 Data Model (app/data.py)
Each book: { id, title, author, year, is_available }. Seeded with two books:
"Мастер и Маргарита" — Михаил Булгаков (1967, available)
"1984" — Джордж Оруэлл (1949, not available)

IDs are auto-incremented via a module-level _next_id counter and get_next_id().

✅ Notable Characteristics
Thorough input validation in POST/PUT/PATCH — checks types, non-empty strings, positive integers, and booleans, returning descriptive Russian-language error messages with proper HTTP status codes (400/404/200/201).
Clean separation of concerns: data storage, app factory, and routes are in separate modules.
Error messages are in Russian (e.g., "Книга не найдена", "Поле title обязательно").
debug=True is enabled in run.py (fine for development, should be disabled in production).

⚠️ Observations / Potential Issues
Postman collection is mostly empty — the "Get all books" and "Post new book" requests point to postman-echo.com rather than localhost:5000, and the other requests (Get by id, Put, Patch, Delete, Search) have no URL/body configured. It's essentially a starter template, not real tests.
In-memory storage — data resets on every server restart; no persistence layer.
Route ordering caveat — /books/search is registered after /books/<int:book_id>. In Flask this still works because search isn't an int and won't match the <int:book_id> converter, but it's worth being aware of.
No tests beyond the Postman skeleton — no pytest/unittest files.

▶️ How to run
cd "C:\Users\dodia\OneDrive\Рабочий стол\Flask\Books-api"
pip install -r requirements.txt
python run.py

Then the API is available at http://127.0.0.1:5000.
