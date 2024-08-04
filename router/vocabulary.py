from fastapi import APIRouter, HTTPException
import logging
from crud import add_word_to_vocabulary_query, get_book_title, get_character_names, get_location_names, get_specific_character, get_specific_location, get_vocabulary
from services import fetch_meaning_from_api

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/")
async def read_vocabulary():
    try:
        vocabulary = await get_vocabulary()
        formatted_response = {}
        for entry in vocabulary:
            book_id = entry['book_id']
            book_title = await get_book_title(book_id)  # Fetch the book title
            logger.info(f"Processing entry: {entry}")
            logger.info(f"Book title: {book_title}")
            word_info = {
                "word": entry["word"],
                "definition": entry["definition"]
            }
            if book_title in formatted_response:
                formatted_response[book_title].append(word_info)
            else:
                formatted_response[book_title] = [word_info]
        
        logger.info(f"Fetched and formatted vocabulary with {len(vocabulary)} entries")
        logger.info(f"Formatted response: {formatted_response}")
        return formatted_response
    except Exception as e:
        logger.error(f"Error fetching vocabulary: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/meaning/{word}")
async def get_word_meaning(word):
    return await fetch_meaning_from_api(word)

@router.get("/add/{book_id}/{word}/")
async def add_word_to_vocabulary(book_id: int, word: str):
    try:
        definition = await fetch_meaning_from_api(word)
        await add_word_to_vocabulary_query(book_id, word, definition)
        logger.info(f"Added word '{word}' to vocabulary for book_id {book_id}")
        return {"message": "Word added successfully"}
    except Exception as e:
        logger.error(f"Error adding word '{word}' to vocabulary for book_id {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/word_type/{book_id}/{word}")
async def get_word_type(book_id: int, word: str):
    character_list = await get_character_names(book_id)
    location_list = await get_location_names(book_id)
    if word in character_list:
        character = await get_specific_character(book_id, word)
        return {
            "word_type": "character",
            "desc": character["description"],
            "image_path": character.get("image_path"),
            "word": character["name"]
        }
    elif word in location_list:
        location = await get_specific_location(book_id, word)
        return {
            "word_type": "location",
            "desc": location["description"],
            "image_path": location.get("image_path"),
            "word": location["location_name"]
        }
    else:
        meaning = await fetch_meaning_from_api(word)
        return {
            "word_type": "normalword",
            "desc": meaning,
            "image_path": None,
            "word": word
        }
