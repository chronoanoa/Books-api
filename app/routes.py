from flask import Blueprint, jsonify, request

from app.data import books, get_next_id

books_bp = Blueprint("books", __name__)

FIELDS = ("title", "author", "year", "is_available")


def find_book(book_id):
    return next((book for book in books if book["id"] == book_id), None)


def validate_book(data, partial=False):
    if data is None:
        return {"error": "Необходимо отправить JSON"}, None

    if partial:
        if not any(field in data for field in FIELDS):
            return {"error": "Необходимо передать хотя бы одно поле", "allowed_fields": list(FIELDS)}, None
    else:
        missing = [field for field in FIELDS if field not in data]
        if missing:
            return {"error": f"Отсутствуют обязательные поля: {', '.join(missing)}"}, None

    cleaned = {}

    if "title" in data:
        title = data["title"]
        if not isinstance(title, str) or not title.strip():
            return {"error": "title должен быть непустой строкой"}, None
        cleaned["title"] = title.strip()

    if "author" in data:
        author = data["author"]
        if not isinstance(author, str) or not author.strip():
            return {"error": "author должен быть непустой строкой"}, None
        cleaned["author"] = author.strip()

    if "year" in data:
        year = data["year"]
        if not isinstance(year, int) or isinstance(year, bool) or year < 0:
            return {"error": "year должен быть положительным целым числом"}, None
        cleaned["year"] = year

    if "is_available" in data:
        is_available = data["is_available"]
        if not isinstance(is_available, bool):
            return {"error": "is_available должен быть boolean (true/false)"}, None
        cleaned["is_available"] = is_available

    return None, cleaned


@books_bp.route("/")
def home():
    return "Главная страница библиотеки"


@books_bp.get("/books")
def get_books():
    return jsonify({"count": len(books), "books": books}), 200


@books_bp.get("/books/search")
def search_books():
    query = request.args.get("title", "").strip().lower()

    if not query:
        return jsonify({"error": "Параметр поиска title обязателен (пример: /books/search?title=мастер)"}), 400

    results = [book for book in books if query in book["title"].lower()]

    return jsonify({"count": len(results), "books": results}), 200


@books_bp.get("/books/<int:book_id>")
def get_book_by_id(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({"error": "Книга не найдена"}), 404

    return jsonify(book), 200


@books_bp.post("/books")
def create_book():
    data = request.get_json(silent=True)
    error, cleaned = validate_book(data)

    if error:
        return jsonify(error), 400

    cleaned["id"] = get_next_id()
    books.append(cleaned)

    return jsonify({"message": "Книга успешно создана", "book": cleaned}), 201


@books_bp.put("/books/<int:book_id>")
def update_book(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({"error": "Книга не найдена"}), 404

    data = request.get_json(silent=True)
    error, cleaned = validate_book(data)

    if error:
        return jsonify(error), 400

    book.update(cleaned)

    return jsonify({"message": "Книга успешно обновлена", "book": book}), 200


@books_bp.patch("/books/<int:book_id>")
def patch_book(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({"error": "Книга не найдена"}), 404

    data = request.get_json(silent=True)
    error, cleaned = validate_book(data, partial=True)

    if error:
        return jsonify(error), 400

    book.update(cleaned)

    return jsonify({"message": "Книга частично обновлена", "book": book}), 200


@books_bp.delete("/books/<int:book_id>")
def delete_book(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({"error": "Книга не найдена"}), 404

    books.remove(book)

    return jsonify({"message": "Книга успешно удалена", "book": book}), 200
