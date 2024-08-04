from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager
import chapter_summary
from database import database
from logging_config import logger
from router import books, character_description, character_list, character_updation, chatbot, combined, location_description, summary, vocabulary, chapter_summary
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your frontend's domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(vocabulary.router, prefix="/vocabulary", tags=["vocabulary"])
app.include_router(combined.router, prefix="/combined", tags=["combined"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
app.include_router(summary.router, prefix="/summary", tags=["summary"])
app.include_router(character_list.router, prefix="/character_list", tags=["character_list"])
app.include_router(character_description.router, prefix="/character_description", tags=["character_description"])
app.include_router(character_updation.router, prefix="/character_updation", tags=["character_updation"])
app.include_router(chapter_summary.router, prefix="/chapter_summary", tags=["chapter_summary"])
app.include_router(location_description.router, prefix="/location", tags=["location"])
import os
from dotenv import load_dotenv

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        load_dotenv()  # Load environment variables from .env file

        api_key = os.getenv("GOOGLE_API_KEY")
        print(api_key) 
        await database.connect()
        logger.info("Database connected successfully")
        yield
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
    finally:
        try:
            await database.disconnect()
            logger.info("Database disconnected successfully")
        except Exception as e:
            logger.error(f"Error disconnecting from the database: {e}")

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)