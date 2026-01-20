from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science' },
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science' },
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history' },
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math' },
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math' },
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math' },
]

@app.get("/welcome")
async def root():
    return {"message": "Hello World"}

@app.get("/books")
async def read_all_books():
    return BOOKS

# http://127.0.0.1:8000/books/title%20one
@app.get("/books/{book_title}")
async def read_book_by_id(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return None

@app.get("/books/")
async def read_all_books_by_category(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# query parameters
@app.get("/books/book_author/")
async def read_book_author(book_author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}/")
async def read_book_by_author_and_category(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# path parameters
@app.get("/books/book/{book_author}/")
async def read_book_by_author(book_author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/")
async def create_book(book = Body()):
    BOOKS.append(book)
    return book

@app.put("/books/")
async def update_book(book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book.get('title').casefold():
            BOOKS[i] = book
    return book

@app.delete("/books/{book_title}")
async def delete_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            BOOKS.remove(book)
            break

@app.delete("/books/delete/{book_title}/")
async def delete_book_by_title(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
