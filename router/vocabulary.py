from fastapi import APIRouter, HTTPException
import logging
from crud import add_word_to_vocabulary_query, get_vocabulary
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
            word_info = {
                "word": entry["word"],
                "definition": entry["definition"]
            }
            if book_id in formatted_response:
                formatted_response[book_id].append(word_info)
            else:
                formatted_response[book_id] = [word_info]
        
        logger.info(f"Fetched and formatted vocabulary with {len(vocabulary)} entries")
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