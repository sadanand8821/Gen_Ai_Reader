from fastapi import APIRouter, HTTPException
import logging
from crud import get_characters_by_book_id, get_locations_by_book_id

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/{book_id}")
async def read_combined(book_id: int):
    try:
        characters = await get_characters_by_book_id(book_id)
        locations = await get_locations_by_book_id(book_id)
        combined_response = {
            "characters": characters,
            "locations": locations
        }
        logger.info(f"Fetched and formatted combined data for book_id {book_id}")
        return combined_response
    except Exception as e:
        logger.error(f"Error fetching combined data for book_id {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")