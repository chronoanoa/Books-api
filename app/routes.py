from flask import Blueprint, jsonify, request

from app.data import books, get_next_id

books_bp = Blueprint(
    "books",
    __name__
)


def find_book(book_id):
    return next(
        (
            book
            for book in books
            if book["id"] == book_id
        ),
        None
    )


# GET READ

@books_bp.route("/")
def home():
    return "Главная страница библиотеки"


@books_bp.get("/books")
def get_books():
    return jsonify({
        "count": len(books),
        "books": books
    }), 200


@books_bp.get("/books/<int:book_id>")
def get_book_by_id(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({
            "error": "Книга не найдена"
        }), 404

    return jsonify(book), 200


# POST CREATE

@books_bp.post("/books")
def create_book():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Необходимо отправить JSON"
        }), 400

    if "title" not in data:
        return jsonify({
            "error": "Поле title обязательно"
        }), 400

    if "author" not in data:
        return jsonify({
            "error": "Поле author обязательно"
        }), 400

    if "year" not in data:
        return jsonify({
            "error": "Поле year обязательно"
        }), 400

    if "is_available" not in data:
        return jsonify({
            "error": "Поле is_available обязательно"
        }), 400

    title = data["title"]
    author = data["author"]
    year = data["year"]
    is_available = data["is_available"]

    if not isinstance(title, str) or title.strip() == "":
        return jsonify({
            "error": "title должен быть непустой строкой"
        }), 400

    if not isinstance(author, str) or author.strip() == "":
        return jsonify({
            "error": "author должен быть непустой строкой"
        }), 400

    if not isinstance(year, int) or year < 0:
        return jsonify({
            "error": "year должен быть положительным целым числом"
        }), 400

    if not isinstance(is_available, bool):
        return jsonify({
            "error": "is_available должен быть boolean (true/false)"
        }), 400

    new_book = {
        "id": get_next_id(),
        "title": title.strip(),
        "author": author.strip(),
        "year": year,
        "is_available": is_available
    }
    books.append(new_book)

    return jsonify({
        "message": "Книга успешно создана",
        "book": new_book
    }), 201


# PUT UPDATE FULL

@books_bp.put("/books/<int:book_id>")
def update_book(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({
            "error": "Книга не найдена"
        }), 404

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Необходимо отправить JSON"
        }), 400

    required_fields = [
        "title",
        "author",
        "year",
        "is_available"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in data
    ]

    if len(missing_fields) > 0:
        return jsonify({
            "error": "Для PUT необходимо передать все поля",
            "missing": missing_fields
        }), 400

    title = data["title"]
    author = data["author"]
    year = data["year"]
    is_available = data["is_available"]

    if not isinstance(title, str) or title.strip() == "":
        return jsonify({
            "error": "title должен быть непустой строкой"
        }), 400

    if not isinstance(author, str) or author.strip() == "":
        return jsonify({
            "error": "author должен быть непустой строкой"
        }), 400

    if not isinstance(year, int) or year < 0:
        return jsonify({
            "error": "year должен быть положительным целым числом"
        }), 400

    if not isinstance(is_available, bool):
        return jsonify({
            "error": "is_available должен быть boolean (true/false)"
        }), 400

    book["title"] = title.strip()
    book["author"] = author.strip()
    book["year"] = year
    book["is_available"] = is_available

    return jsonify({
        "message": "Книга успешно обновлена",
        "book": book
    }), 200


# PATCH UPDATE PARTIAL

@books_bp.patch("/books/<int:book_id>")
def patch_book(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({
            "error": "Книга не найдена"
        }), 404

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Необходимо отправить JSON"
        }), 400

    allowed_fields = [
        "title",
        "author",
        "year",
        "is_available"
    ]

    received_allowed_fields = [
        field
        for field in allowed_fields
        if field in data
    ]

    if len(received_allowed_fields) == 0:
        return jsonify({
            "error": "Необходимо передать хотя бы одно поле",
            "allowed_fields": allowed_fields
        }), 400

    if "title" in data:
        if not isinstance(data["title"], str) or data["title"].strip() == "":
            return jsonify({
                "error": "title должен быть непустой строкой"
            }), 400
        book["title"] = data["title"].strip()

    if "author" in data:
        if not isinstance(data["author"], str) or data["author"].strip() == "":
            return jsonify({
                "error": "author должен быть непустой строкой"
            }), 400
        book["author"] = data["author"].strip()

    if "year" in data:
        if not isinstance(data["year"], int) or data["year"] < 0:
            return jsonify({
                "error": "year должен быть положительным целым числом"
            }), 400
        book["year"] = data["year"]

    if "is_available" in data:
        if not isinstance(data["is_available"], bool):
            return jsonify({
                "error": "is_available должен быть boolean"
            }), 400
        book["is_available"] = data["is_available"]

    return jsonify({
        "message": "Книга частично обновлена",
        "book": book
    }), 200


# DELETE

@books_bp.delete("/books/<int:book_id>")
def delete_book(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({
            "error": "Книга не найдена"
        }), 404

    books.remove(book)

    return jsonify({
        "message": "Книга успешно удалена",
        "book": book
    }), 200


# ДОПОЛНИТЕЛЬНЫЙ МАРШРУТ (Поиск)

@books_bp.get("/books/search")
def search_books():
    query = request.args.get("title", "").strip().lower()

    if not query:
        return jsonify({
            "error": "Параметр поиска title обязателен (пример: /books/search?title=мастер)"
        }), 400

    results = [
        book
        for book in books
        if query in book["title"].lower()
    ]

    return jsonify({
        "count": len(results),
        "books": results
    }), 200