def test_get_all_books(client):
    resp = client.get("/books")

    assert resp.status_code == 200
    body = resp.get_json()
    assert body["count"] == len(body["books"])
    assert body["count"] >= 2


def test_get_book_by_id(client):
    resp = client.get("/books/1")

    assert resp.status_code == 200
    assert resp.get_json()["id"] == 1


def test_get_book_not_found(client):
    resp = client.get("/books/9999")

    assert resp.status_code == 404


def test_search_books(client):
    resp = client.get("/books/search?title=1984")

    assert resp.status_code == 200
    assert resp.get_json()["count"] == 1


def test_search_books_missing_query(client):
    resp = client.get("/books/search")

    assert resp.status_code == 400


def test_create_book(client):
    payload = {
        "title": " Война и мир ",
        "author": "Лев Толстой",
        "year": 1869,
        "is_available": True,
    }
    resp = client.post("/books", json=payload)

    assert resp.status_code == 201
    body = resp.get_json()
    assert body["book"]["title"] == "Война и мир"
    assert body["book"]["id"] >= 3


def test_create_book_missing_fields(client):
    resp = client.post("/books", json={"title": "x"})

    assert resp.status_code == 400


def test_create_book_rejects_bool_year(client):
    payload = {"title": "x", "author": "y", "year": True, "is_available": True}
    resp = client.post("/books", json=payload)

    assert resp.status_code == 400


def test_create_book_rejects_empty_title(client):
    payload = {"title": "   ", "author": "y", "year": 2000, "is_available": True}
    resp = client.post("/books", json=payload)

    assert resp.status_code == 400


def test_create_book_without_json(client):
    resp = client.post("/books", data="not json")

    assert resp.status_code == 400


def test_put_book(client):
    payload = {"title": "new", "author": "a", "year": 1990, "is_available": False}
    resp = client.put("/books/1", json=payload)

    assert resp.status_code == 200
    assert resp.get_json()["book"]["title"] == "new"


def test_put_book_not_found(client):
    payload = {"title": "new", "author": "a", "year": 1990, "is_available": False}
    resp = client.put("/books/9999", json=payload)

    assert resp.status_code == 404


def test_patch_book_partial(client):
    resp = client.patch("/books/1", json={"year": 2001})

    assert resp.status_code == 200
    assert resp.get_json()["book"]["year"] == 2001


def test_patch_book_no_known_fields(client):
    resp = client.patch("/books/1", json={"foo": "bar"})

    assert resp.status_code == 400


def test_delete_book(client):
    resp = client.delete("/books/2")

    assert resp.status_code == 200
    assert client.get("/books/2").status_code == 404


def test_delete_book_not_found(client):
    resp = client.delete("/books/9999")

    assert resp.status_code == 404
