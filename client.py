import requests

BASE = "http://127.0.0.1:8000"
#lesson6
# r = requests.get(BASE + "/books", params={"author": "Tolkien"}, timeout=5)
# r.raise_for_status()
# for book in r.json():
#     print(book["title"])

#lesson7


#lesson7
r = requests.post(BASE + "/books", json={"title": "Dune", "author": "Herbert"}, timeout=5)
r.raise_for_status()
book_id = r.json()["id"]
print("created", r.status_code, r.json())


put1 = requests.put(BASE + "/books", json={'id': 4 ,"title": "Dune PUT", "author": "Herbert PUT"}, timeout=5)
put1.raise_for_status()
print()
book_put = put1.json()["id"]
print("Put id 4", put1.status_code, put1.json())

#case1 PATCH normal income data
r1 = requests.patch(BASE + "/books/4", json={"title": "Dune PATCH FULL", "author": "Herbert PATCH FULL"}, timeout=5)
r1.raise_for_status()
book_id1 = r1.json()["id"]
print(requests.get(BASE + "/books", timeout=5).json())
#200 expected

#case2 PATCH partial (not full) income data
r2 = requests.patch(BASE + "/books/4", json={"title": "Patch  ONLY title"}, timeout=5)
r2.raise_for_status()
book_id2 = r2.json()["id"]
print()
print(f"Patched book id{book_id2} ", r2.status_code, r2.json())
print(requests.get(BASE + "/books", timeout=5).json())
#200 expected


#case3 PATCH partial (not full) income data
r3 = requests.patch(BASE + "/books/4", json={"author": "Patch  ONLY author"}, timeout=5)
r3.raise_for_status()
book_id3 = r2.json()["id"]
print()
print(f"Patched book id{book_id3} ", r3.status_code, r3.json())
print(requests.get(BASE + "/books", timeout=5).json())
#200 expected

#case4 PATCH incorrect index
p4 = requests.patch(BASE + "/books/67",  json={"title": "Dune", "author": "Herbert"}, timeout=5)
print()
print(f"Patched book not existing id 67 - we have error {p4.status_code}" )
print(requests.get(BASE + "/books", timeout=5).json())
#404 expected

#case1 DELETE normal income data
d1 = requests.delete(BASE + "/books/4" , timeout=5)
#result_d1 = d1.json()
print()
print(f"DELETED the book with id = 4 CODE", d1.status_code )
print(requests.get(BASE + "/books", timeout=5).json())
#204 expected

#case2 REPEAT DELETE command normal income data
d2 = requests.delete(BASE + "/books/4", timeout=5)
result_d2 = d2.json()
print()
print(f"DELETED the book second time with id = 4 CODE",  d2.status_code, d2.json())
print(requests.get(BASE + "/books", timeout=5).json())
#404 error expected

#case 4 GET id 4
g1 = requests.get(BASE + "/books/4", timeout=5)
result = g1.json()
print()
print(f"GET id = 4 CODE",  g1.status_code, result)
#404 error expected

#case 5 put book id 3
put_book = requests.put(BASE + "/books/3", json={"title": "Replaced book title", "author": "Replaced book author"}, timeout=5)
result_p = put_book.json()
print()
print(f"PUT id = 3 CODE", put_book.status_code, result_p)
#200 CODE expected

#case 5 put book id 3
put_book_2 = requests.put(BASE + "/books/3", json={ "title": "Replaced book ONLY title"}, timeout=5)
print()
print(f"PUT id = 3 CODE",  put_book_2.status_code , "no author")
#4xx error expected - client wrong