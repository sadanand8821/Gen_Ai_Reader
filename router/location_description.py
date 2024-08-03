from fastapi import APIRouter, HTTPException
import logging
import ast

from crud import get_book_path, get_location
from location_description import LocationDescription

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/{book_id}")
async def getLocationDescription(book_id: int):
    location_list = await get_location(book_id)
    if (len(location_list) == 0):
        book_path = await get_book_path(book_id)
        location_list = LocationDescription(book_path, verbose=True).run()
        logger.info(f"Generated and cached location description for bookId: {book_id}")
        logger.info(f"Location description: {location_list}")
        return location_list
    else:
        return location_list