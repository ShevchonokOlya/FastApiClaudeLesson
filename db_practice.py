import sqlite3

conn = sqlite3.connect("books.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL)
    """)
conn.commit()

# cur = conn.execute(
#     "INSERT INTO books (title, author) VALUES (?, ?)",
#     ("Harry Potter", "Rowling"),
# )
# conn.commit()
# print("new id:", cur.lastrowid)

# rows = conn.execute("SELECT id, title, author FROM books").fetchall()
# print(rows)
# print(conn.execute("SELECT id, title, author FROM books WHERE id = ?", (1,)).fetchone())
# print(conn.execute("SELECT id, title, author FROM books WHERE id = ?", (99,)).fetchone())

#
# cur = conn.execute("UPDATE books SET title = ? WHERE id = ?", ("Harry Potter 2", 1))
# conn.commit()
# print("changed rows:", cur.rowcount)

#
# cur = conn.execute("DELETE FROM books WHERE id = ?", (2,))
# conn.commit()
# print("deleted rows:", cur.rowcount)
# print(conn.execute("SELECT * FROM books").fetchall())


conn.row_factory = sqlite3.Row
row = conn.execute("SELECT id, title, author FROM books WHERE id = ?", (1,)).fetchone()
print(dict(row))