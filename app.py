import ssl
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from enum import Enum
import uvicorn

app = FastAPI()


class BookGenre(str, Enum):
    ACTION = "action"
    COMEDY = "comedy"
    DRAMA = "drama"


class Book(BaseModel):
    id: int
    # pydantic model with validation not necessary but useful
    title: str = Field(..., min_length=1, description="Title cannot be empty")
    author: str = Field(..., min_length=1, description="Author cannot be empty")
    genre: BookGenre
    rating: Optional[float] = Field(
        None, ge=0, le=10, description="Rating must be between 0 and 10"
    )


my_books: dict[int, Book] = {
    100: Book(
        id=100,
        title="The Alchemist",
        author="Paulo Coelho",
        rating=9.5,
        genre=BookGenre.DRAMA,
    )
}


@app.get("/")
def read_root():
    return "Hello World!"


@app.post("/books", response_model=Book, status_code=201)
def create_book(book: Book):
    # # check that author name is not empty
    # if book.author == "" or book.title == "":
    #     # code 400 indicates client error
    #     raise HTTPException(status_code=400, detail="Author or title cannot be empty")

    # # check that rating is between 0 and 10
    # if book.rating is not None and (book.rating < 0 or book.rating > 10):
    #     raise HTTPException(status_code=400, detail="Rating must be between 0 and 10")

    # check if book id already exists
    if book.id in my_books:
        raise HTTPException(status_code=400, detail="Book with this id already exists")

    my_books[book.id] = book

    return book


@app.get("/books")
def get_books(
    genre: Optional[BookGenre] = Query(None, description="Filter by genre"),
    rating_greater_than: Optional[float] = Query(
        None, description="Filter by minimum rating"
    ),
):
    return {
        k: v
        for k, v in my_books.items()
        if (genre is None or v.genre == genre)
        and (
            rating_greater_than is None
            or (v.rating is not None and v.rating > rating_greater_than)
        )
    }


@app.get("/books/{book_id}")
def get_book(book_id: int):
    # check that book id exists
    if book_id not in my_books:
        raise HTTPException(status_code=404, detail="Book not found")

    return my_books[book_id]


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    # check that book id exists
    if book_id not in my_books:
        raise HTTPException(status_code=404, detail="Book not found")

    _ = my_books.pop(book_id)

    return None


if __name__ == "__main__":
    # Define the SSL context with your certificate and key
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    # Run FastAPI with HTTPS
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_context=context)
