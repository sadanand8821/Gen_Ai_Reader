from fastapi import APIRouter, HTTPException
import logging
import ast
from database import database
from characters_gatherer import CharacterList
from crud import get_book_path, get_characters_by_book_id, get_unique_book_ids

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/{bookId}")
async def getCharacterList(bookId: int):
    if bookId in await get_unique_book_ids():
        print(True)
        try:
            rows = await get_characters_by_book_id(bookId)
            print(rows)
            characters = [row["name"] for row in rows]
            logger.info(f"Retrieved {len(characters)} characters for bookId: {bookId}")
            return {"character_list": characters}
        except Exception as e:
            logger.error(f"Error retrieving characters for bookId: {bookId}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    book_path = await get_book_path(bookId)
    character_list = CharacterList(pathToEpub=book_path,verbose=True).run()
    
    logger.info(f"Generated and cached character list for bookId: {bookId} and the character list is: {character_list}")
    # Insert character names into the database
    await insert_characters_into_db(bookId, character_list)


async def insert_characters_into_db(book_id: int, character_list: list):
    query = """
    INSERT INTO characters (book_id, name)
    VALUES (:book_id, :name)
    ON CONFLICT (book_id, name) DO NOTHING
    """
    try:
        logger.info(f"Type of character_list: {type(character_list)}")
        logger.info(f"Content of character_list: {character_list}")
        
        # Check if character_list is a string and convert it to a list
        if isinstance(character_list, str):
            try:
                actual_list = ast.literal_eval(character_list)
                if not isinstance(actual_list, list):
                    raise ValueError("Parsed character_list is not a list")
            except (SyntaxError, ValueError) as e:
                logger.error(f"Error parsing character_list: {e}")
                raise HTTPException(status_code=400, detail="Invalid character list format")
        else:
            actual_list = character_list
        
        for character in actual_list:
            try:
                await database.execute(query, values={"book_id": book_id, "name": character})
                logger.info(f"Inserted character '{character}' for book_id {book_id} into the database")
            except Exception as e:
                logger.error(f"Error inserting character '{character}' into the database: {e}")
        return actual_list

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")