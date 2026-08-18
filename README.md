# Books RESTful API

A Python Flask-based RESTful API for managing a book library. This project supports full CRUD (Create, Read, Update, Delete) operations and includes a Postman collection for testing.

---

## 📁 Project Structure

```text
books-api/
├── app/
│   ├── __init__.py    # Flask app initialization & Blueprints
│   ├── data.py        # In-memory book storage/data
│   └── routes.py      # API endpoints (GET, POST, PUT, PATCH, DELETE)
├── postman/           # Postman collection export
├── .gitignore         # Ignored files (venv, cache)
├── requirements.txt   # Project dependencies
└── run.py             # Entry point to run the Flask application
