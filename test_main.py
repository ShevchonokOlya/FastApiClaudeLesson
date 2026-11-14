from fastapi.testclient import TestClient
from main import app  # ваше приложение из main.py

client = TestClient(app)  # «клиент» без сервера


def test_get_book():
    r = client.get("/books/1")
    assert r.status_code == 200
    assert r.json()["title"] == "Harry Potter"


def test_get_missing_book():
    r = client.get("/books/999")
    assert r.status_code == 404


def test_get_book_wrong_type():
    r = client.get("/books/abc")
    assert r.status_code == 422


def test_create_returns_201():
    r = client.post("/books", json={"title": "Dune", "author": "Herbert"})
    assert r.status_code == 201


def test_get_no_results():
    r = client.get("/books", params={"author": "Pushkin"})
    assert r.status_code == 200
    assert len(r.json()) == 0


def test_create_no_author_returns_422():
    r = client.post("/books", json={"title": "Dune"})
    assert r.status_code == 422


def test_patch_label_only():
    r = client.post("/books", json={"title": "new_book", "author": "new_author"})
    assert r.status_code == 201
    book_id = r.json()["id"]
    r = client.patch("/books/" + f"{book_id}", json={"title": "Title was changed"})
    result_patch = r.json()
    assert result_patch["author"] == "new_author"
    print(result_patch["title"])


def test_double_delete_returns_204_and_404():
    book_id = client.post("/books", json={"title": "Tmp", "author": "Me"}).json()["id"]
    r = client.delete(f"/books/{book_id}")
    assert r.status_code == 204
    r2 = client.delete(f"/books/{book_id}")
    assert r2.status_code == 404


def test_put_full_change_returns_200():
    book_id = client.post("/books", json={"title": "Tmp put_full_test", "author": "It is  put_full_test"}).json()["id"]

    r = client.put(f"/books/{book_id}", json={"title": "new_book", "author": "new_author"})
    assert r.status_code == 200
    r2 = client.get(f"/books/{book_id}")
    result_put = r2.json()
    assert result_put["title"] == "new_book"
    assert result_put["author"] == "new_author"


def test_put_no_author_returns_422():
    book_id = client.post("/books", json={"title": "Tmp put_full_test", "author": "It is  put_full_test"}).json()["id"]

    before_changes = client.get(f"/books/{book_id}")
    results_before_changes = before_changes.json()
    before_changes_title = results_before_changes["title"]
    before_changes_author = results_before_changes["author"]

    r = client.put(f"/books/{book_id}", json={"title": "new_book"})
    assert r.status_code == 422
    r2 = client.get(f"/books/{book_id}")
    result_put = r2.json()
    assert result_put["title"] == before_changes_title
    assert result_put["author"] == before_changes_author

##kjgkuh


def test_get_author_rowling_returns_200() -> None:
    r = client.get("/books", params={"author": "Rowling"}, timeout=5)
    assert r.status_code == 200
    assert len(r.json()) == 1
