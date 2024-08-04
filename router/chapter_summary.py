from fastapi import APIRouter, HTTPException
import logging
import ast
from chapter_summary import ChapterSummary
from crud import get_book_path
from database import database
import re


router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/{book_id}/{chapterNumber}")
async def getChapterWiseSummary(book_id: int, chapterNumber: str):
    try:
        logger.info(chapterNumber)
        chapterNumber = re.sub(r'\W+', '', chapterNumber)
        logger.info(chapterNumber)
        
        
        query ="""
            SELECT chapter_summary 
            FROM chapter_summaries 
            WHERE book_id = :book_id AND chapter_number = :chapter_number
        """
        chapter_summary = await database.fetch_one(query)
        if chapter_summary:
            return chapter_summary['chapter_summary']
        else:
            book_path = await get_book_path(book_id)
            chapter_summary = ChapterSummary(book_path, chapterNumber, verbose=True).run()
            logger.info(f"Generated and cached chapter summary for book_id: {book_id} and chapter_number: {chapterNumber}")
            logger.info(f"Chapter summary: {chapter_summary}")
             # Log the type of chapter_summary
            logger.info(f"Type of chapter_summary: {type(chapter_summary)}")
            
            insert_query = """
                INSERT INTO chapter_summaries (book_id, chapter_number, chapter_summary)
                VALUES (:book_id, :chapter_number, :chapter_summary)
            """
            await database.execute(insert_query, values={"book_id": book_id, "chapter_number": chapterNumber, "chapter_summary": chapter_summary})
            return chapter_summary
        
    except Exception as e:
        logger.error(f"Error in getChapterWiseSummary: {e}")
        return {"message": "Internal server error"}