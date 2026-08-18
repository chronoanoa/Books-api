import copy

import pytest

import app.data as data
from app import create_app

_SEED = copy.deepcopy(data.books)
_SEED_NEXT_ID = data._next_id


@pytest.fixture
def client():
    data.books[:] = copy.deepcopy(_SEED)
    data._next_id = _SEED_NEXT_ID

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
