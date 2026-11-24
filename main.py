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


DB_PATH = os.environ.get("BOOKS_DB", "books.db")
app = FastAPI()


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class Database:
    def __enter__(self):
        self.conn = get_conn()  # открыть и запомнить в self
        return self.conn  # попадёт в conn после as

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()  # закрыть, что бы ни случилось


def init_db():
    with Database() as conn:
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


init_db()


def get_book_or_404(conn, book_id: int) -> dict:
    row = conn.execute("SELECT id, title, author FROM books WHERE id = ?", (book_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return dict(row)


@app.post("/books", status_code=201)
def create_book(book: BookIn):
    with Database() as conn:
        cur = conn.execute("INSERT INTO books (title, author) VALUES (?, ?)", (book.title, book.author))
        conn.commit()
        return {"id": cur.lastrowid, "title": book.title, "author": book.author}


@app.patch("/books/{book_id}")
def update_book(book_id: int, changes: BookUpdate):
    with Database() as conn:
        book = get_book_or_404(conn, book_id)  # нет книги — 404
        book.update(changes.model_dump(exclude_unset=True))  # как раньше со списком
        conn.execute(
            "UPDATE books SET title = ?, author = ? WHERE id = ?",
            (book["title"], book["author"], book_id),
        )
        conn.commit()
        return book


@app.put("/books/{book_id}")
def replace_book(book_id: int, new_book: BookIn):
    with Database() as conn:
        get_book_or_404(conn, book_id)
        conn.execute(
            "UPDATE books SET title = ?, author = ? WHERE id = ?",
            (new_book.title, new_book.author, book_id),
        )
        conn.commit()
        return {"id": book_id, "title": new_book.title, "author": new_book.author}


@app.get("/books/{book_id}")
def get_book(book_id: int):
    with Database() as conn:
        return get_book_or_404(conn, book_id)


@app.get("/")
def root():
    return {"message": "Hello from my API"}


@app.get("/books")
def list_books(author: str | None = None, limit: int = 10) -> list:
    with Database() as conn:
        if author is None:
            books = conn.execute("SELECT * FROM books LIMIT ?", (limit,)).fetchall()
        else:
            books = conn.execute("SELECT * FROM books WHERE author = ? LIMIT ?", (author, limit)).fetchall()

        return [dict(book) for book in books]


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    with Database() as conn:
        curr = conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        if curr.rowcount == 0:
            raise HTTPException(status_code=404, detail="Book not found")
