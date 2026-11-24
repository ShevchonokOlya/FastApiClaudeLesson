from main import Database


def book_titles(conn):
    res = conn.execute("SELECT title FROM books").fetchall()
    for row in res:
        yield row["title"]


with Database() as conn:
    for title in book_titles(conn):
        print(title)