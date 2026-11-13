from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


BOOKS = [
    {"id": 1, "title": "Harry Potter", "author": "Rowling"},
    {"id": 2, "title": "The Hobbit", "author": "Tolkien"},
    {"id": 3, "title": "The Lord of the Rings", "author": "Tolkien"},
    {"id": 4, "title": "Dune", "author": "Herbert"}
]

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

app = FastAPI()

@app.post("/books", status_code=201)
def create_book(book: BookIn):
    new_id = max(b["id"] for b in BOOKS) + 1
    new_book = {"id": new_id, "title": book.title, "author": book.author}
    BOOKS.append(new_book)
    return new_book

def find_book(book_id: int) -> dict:
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.patch("/books/{book_id}")
def update_book(book_id: int, changes: BookUpdate):
    book = find_book(book_id)
    book.update(changes.model_dump(exclude_unset=True))
    return book

@app.put("/books")
def put_book(new_book: BookPUT):
    income_book = new_book.model_dump(exclude_unset=True)
    book_id = income_book['id']
    title = income_book['title']
    author = income_book['author']
    for book in BOOKS:
        if book["id"] == book_id:
            book.update({"title": title, "author": author})
            return book
    BOOKS.append({"id": book_id, "title": title, "author": author})
    return income_book


@app.put("/books/{book_id}")
def replace_book(book_id:int, new_book: BookIn):

    book = find_book(book_id)
    book.update(new_book.model_dump(exclude_unset=True))
    return book



@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    book = find_book(book_id)
    BOOKS.remove(book)

@app.get("/books/{book_id}")
def get_book(book_id: int):
    return find_book(book_id)

@app.get("/")
def root():
    return {"message": "Hello from my API"}

@app.get("/books")
def list_books(author: str | None = None, limit: int = 10) -> list:
    result = BOOKS if author is None else [b for b in BOOKS if b["author"] == author]
    return result[:min(limit, len(BOOKS))]




