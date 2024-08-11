from fastapi import HTTPException
from database import database
from schemas import BookCreateSchema
import logging

logger = logging.getLogger(__name__)


# Get All Books
async def get_books():
    query = "SELECT * FROM books"
    rows = await database.fetch_all(query)
    return [dict(row) for row in rows]

async def get_book_path(book_id: int) -> str:
    query = "SELECT file_path FROM books WHERE b_id = :book_id"
    row = await database.fetch_one(query, {"book_id": book_id})
    if row is None:
        raise ValueError(f"No book found with ID: {book_id}")
    return row["file_path"]



async def get_unique_book_ids() -> list:
    query = "SELECT DISTINCT book_id FROM characters"
    try:
        rows = await database.fetch_all(query)
        print(rows)
        unique_book_ids = [row["book_id"] for row in rows]
        return unique_book_ids
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Get Words From the Vocab List
async def get_vocabulary():
    query = "SELECT * FROM vocabulary"
    rows = await database.fetch_all(query)

    return [dict(row) for row in rows]

# Get CHaracters
async def get_characters_by_book_id(book_id: int):
    query = "SELECT name, description, image_path FROM characters WHERE book_id = :book_id"
    rows = await database.fetch_all(query, {"book_id": book_id})
    return [dict(row) for row in rows]

# Get Locations
async def get_locations_by_book_id(book_id: int):
    query = "SELECT location_name AS name, description, image_path FROM location WHERE book_id = :book_id"
    rows = await database.fetch_all(query, {"book_id": book_id})
    return [dict(row) for row in rows]


# Add Word to Vocabulary
async def add_word_to_vocabulary_query(book_id: int, word: str, definition: str):
    # Check if the word already exists for the given book_id
    check_query = "SELECT * FROM vocabulary WHERE book_id = :book_id AND word = :word"
    existing_word = await database.fetch_one(check_query, {"book_id": book_id, "word": word})
    
    if existing_word:
        return {"message": "Word already exists for this book_id"}
    
    # Insert the new word if it doesn't exist
    insert_query = "INSERT INTO vocabulary (book_id, word, definition) VALUES (:book_id, :word, :definition)"
    await database.execute(insert_query, {"book_id": book_id, "word": word, "definition": definition})
    return {"message": "Word added successfully"}


# Get Summary of book
async def get_summary_by_book_id(book_id: int):
    query = "SELECT summary FROM books WHERE b_id = :book_id"
    row = await database.fetch_one(query, {"book_id": book_id})
    return row["summary"]

# Add Summary to book
async def add_summary_to_book(book_id: int, summary: str):
    query = "UPDATE books SET summary = :summary WHERE b_id = :book_id"
    await database.execute(query, {"book_id": book_id, "summary": summary})
    return {"message": "Summary added successfully"}

# Get Book Title
async def get_book_title(book_id: int):
    query = "SELECT book_title FROM books WHERE b_id = :book_id"
    row = await database.fetch_one(query, {"book_id": book_id})
    return row["book_title"]

# Add New Book
async def create_book(book: BookCreateSchema):
    query = """
    INSERT INTO books (book_title, author, file_path, last_read, summary, cover_image_path)
    VALUES (:book_title, :author, :file_path, :last_read, :summary, :cover_image_path)
    RETURNING b_id, book_title, author, file_path, last_read, summary, cover_image_path
    """
    values = {
        "book_title": book.book_title,
        "author": book.author,
        "file_path": book.file_path,
        "last_read": book.last_read,
        "summary": book.summary,
        "cover_image_path": book.cover_image_path
    }
    new_book = await database.fetch_one(query, values)
    return new_book


# Get Character Description

async def get_character_description(character_name: str, book_id: int):
    query = "SELECT description FROM characters WHERE name = :character_name AND book_id = :book_id"
    row = await database.fetch_one(query, {"character_name": character_name, "book_id": book_id})
    if row is None:
        return None
    return row["description"]


# Add Character Description

async def add_character_description(book_id: int, character_name: str, description: str):
    query = """
    INSERT INTO characters (book_id, name, description)
    VALUES (:book_id, :name, :description)
    ON CONFLICT (book_id, name) DO UPDATE
    SET description = :description
    """
    await database.execute(query, {"book_id": book_id, "name": character_name, "description": description})
    return {"message": "Character description added successfully"}


async def get_location(book_id: int):
    query = "SELECT location_name, description FROM location WHERE book_id = :book_id"
    rows = await database.fetch_all(query, {"book_id": book_id})
    logger.info(f"Rows: {rows}")
    logger.info(rows == None)
    return [dict(row) for row in rows]


# Add Cover Image Path

async def add_cover_image_path(book_id: int, cover_image_path: str):
    query = "UPDATE books SET cover_image_path = :cover_image_path WHERE b_id = :book_id"
    await database.execute(query, {"book_id": book_id, "cover_image_path": cover_image_path})
    return {"message": "Cover image path added successfully"}


async def get_location_names(book_id: int):
    query = "SELECT location_name FROM location WHERE book_id = :book_id"
    rows = await database.fetch_all(query, {"book_id": book_id})
    return [row["location_name"] for row in rows]

async def get_character_names(book_id: int):
    query = "SELECT name FROM characters WHERE book_id = :book_id"
    rows = await database.fetch_all(query, {"book_id": book_id})
    return [row["name"] for row in rows]

async def get_specific_character(book_id: int, character_name: str):
    query = "SELECT name, description, image_path FROM characters WHERE book_id = :book_id AND name = :character_name"
    row = await database.fetch_one(query, {"book_id": book_id, "character_name": character_name})
    return dict(row)

async def get_specific_location(book_id: int, location_name: str):
    query = "SELECT location_name, description, image_path FROM location WHERE book_id = :book_id AND location_name = :location_name"
    row = await database.fetch_one(query, {"book_id": book_id, "location_name": location_name})
    return dict(row)

