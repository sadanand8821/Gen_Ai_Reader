from fastapi import APIRouter, HTTPException
import logging

from grpc import Status
from pydantic import BaseModel

from crud import create_book, get_books
from schemas import BookCreateSchema, BookSchema





router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/all/")
async def read_books():
    try:
        books = await get_books()
        logger.info(f"Fetched {len(books)} books")
        return books
    except Exception as e:
        logger.error(f"Error fetching books: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/{book_id}")
async def read_book(book_id: int):
    try:
        books = await get_books()
        book = [book for book in books if book["b_id"] == book_id]
        if book:
            logger.info(f"Fetched book with id {book_id}")
            return book[0]
        else:
            logger.error(f"Book with id {book_id} not found")
            raise HTTPException(status_code=404, detail="Book not found")
    except Exception as e:
        logger.error(f"Error fetching book with id {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    

# Add New Book
@router.post("/add/", response_model=BookSchema)
async def add_book(book: BookCreateSchema):
    try:
        new_book = await create_book(book)
        logger.info(f"Added new book with ID {new_book['b_id']}")
        return new_book
    except Exception as e:
        logger.error(f"Error adding book: {e}")
        raise HTTPException(status_code=Status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error adding book")