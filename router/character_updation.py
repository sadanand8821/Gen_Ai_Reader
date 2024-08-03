from fastapi import APIRouter, HTTPException
import logging
import ast
from character_updation import CharacterUpdation
from crud import add_character_description, get_book_path, get_character_description
from database import database

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/{character_name}/{chapterNumber}/{bookId}")
async def getCharacterDescription(character_name: str, chapterNumber, bookId: int):
    character_description = await get_character_description(character_name, bookId)
    if character_description:
        return character_description
    else:
        book_path = await get_book_path(bookId)
        logger.info("Book path: ", book_path)
        character_updation = CharacterUpdation(book_path, character_name, chapterNumber, verbose=True).run()
        logger.info(f"Generated and cached character description for character: {character_name} and bookId: {bookId}")
        logger.info(f"Character description: {character_description}")
        await add_character_description(bookId, character_name, character_description)
        return character_description