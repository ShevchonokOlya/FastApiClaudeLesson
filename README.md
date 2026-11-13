# Books API

A small REST API for a book library, built with FastAPI.

## Features
- CRUD for books: create, read, update, delete
- Filter books by author: `GET /books?author=Tolkien`
- Data validation with Pydantic
- Tests with pytest

## How to run
    pip install -r requirements.txt
    fastapi dev main.py

Open http://127.0.0.1/docs to see the API documentation.

## How to test
    pytest

## Endpoints
| Method | Path             | Description                  |
|--------|------------------|------------------------------|
| GET    | /books           | List books, filter by author and limit |
| GET    | /books/{book_id} | Get one book                 |
| GET    | /                | Root                         |
| POST   | /books           | Create a book                |
| PUT    | /books           | Create or replace a book (id in body)   |
| PUT    | /books/{book_id} | Replace the book             |
| PATCH  | /books/{book_id} | Change part of a book        |
| DELETE | /books/{book_id} | Delete a book                |

## Tests
11 tests, all passing

### Author: Olga