from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sqlite3


class BookIn(BaseModel):
    title: str
    author: str


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None


class BookPUT(BaseModel):
    id: int
    title: str
    author: str


DB_PATH = os.environ.get("BOOKS_DB", "books.db")
app = FastAPI()


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO books (title, author) VALUES (?, ?)",
                [
                    ("Harry Potter", "Rowling"),
                    ("The Hobbit", "Tolkien"),
                    ("The Lord of the Rings", "Tolkien"),
                ],
            )
        conn.commit()
    finally:
        conn.close()

init_db()

def get_book_or_404(conn, book_id: int) -> dict:
    row = conn.execute("SELECT id, title, author FROM books WHERE id = ?", (book_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return dict(row)


@app.post("/books", status_code=201)
def create_book(book: BookIn):
    conn = get_conn()
    try:
        cur = conn.execute("INSERT INTO books (title, author) VALUES (?, ?)", (book.title, book.author))
        conn.commit()
        return {"id": cur.lastrowid, "title": book.title, "author": book.author}
    finally:
        conn.close()


@app.patch("/books/{book_id}")
def update_book(book_id: int, changes: BookUpdate):
    conn = get_conn()
    try:
        book = get_book_or_404(conn, book_id)  # нет книги — 404
        book.update(changes.model_dump(exclude_unset=True))  # как раньше со списком
        conn.execute(
            "UPDATE books SET title = ?, author = ? WHERE id = ?",
            (book["title"], book["author"], book_id),
        )
        conn.commit()
        return book
    finally:
        conn.close()


#
# @app.put("/books")
# def put_book(new_book: BookPUT):
#     income_book = new_book.model_dump(exclude_unset=True)
#     book_id = income_book['id']
#     title = income_book['title']
#     author = income_book['author']
#     for book in BOOKS:
#         if book["id"] == book_id:
#             book.update({"title": title, "author": author})
#             return book
#     BOOKS.append({"id": book_id, "title": title, "author": author})
#     return income_book


@app.put("/books/{book_id}")
def replace_book(book_id: int, new_book: BookIn):
    conn = get_conn()
    try:
        get_book_or_404(conn, book_id)
        conn.execute(
            "UPDATE books SET title = ?, author = ? WHERE id = ?",
            (new_book.title, new_book.author, book_id),
        )
        conn.commit()
        return {"id": book_id, "title": new_book.title, "author": new_book.author}
    finally:
        conn.close()


@app.get("/books/{book_id}")
def get_book(book_id: int):
    conn = get_conn()
    try:
        return get_book_or_404(conn, book_id)
    finally:
        conn.close()


@app.get("/")
def root():
    return {"message": "Hello from my API"}


@app.get("/books")
def list_books(author: str | None = None, limit: int = 10) -> list:
    conn = get_conn()
    try:
        if author:
            books = conn.execute("SELECT * FROM books WHERE author = ? LIMIT ?",
                                 (author,limit)).fetchall()
        else:
            books = conn.execute(
                "SELECT * FROM books LIMIT ?",(limit, )
            ).fetchall()

        return [dict(book) for book in books]
    finally:
        conn.close()


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    conn = get_conn()
    try:
        curr = conn.execute("DELETE FROM books WHERE id = ?",(book_id,))
        conn.commit()
        if curr.rowcount == 0:
            raise HTTPException(status_code=404, detail="Book not found")
    finally:
        conn.close()
