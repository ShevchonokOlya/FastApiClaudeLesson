from main import Database


def book_titles(conn):
    res = conn.execute("SELECT title FROM books")
    for row in res:
        yield row["title"]


with Database() as conn:
    for title in book_titles(conn):
        print(title)