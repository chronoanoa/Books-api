books = [
    {
        "id": 1,
        "title": "Мастер и Маргарита",
        "author": "Михаил Булгаков",
        "year": 1967,
        "is_available": True
    },
    {
        "id": 2,
        "title": "1984",
        "author": "Джордж Оруэлл",
        "year": 1949,
        "is_available": False
    }
]

_next_id = 3

def get_next_id():
    global _next_id
    current_id = _next_id
    _next_id += 1
    return current_id