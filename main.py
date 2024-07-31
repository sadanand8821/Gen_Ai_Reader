from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager
from database import database
from logging_config import logger
from router import books, character_description, character_list, chatbot, combined, summary, vocabulary

app = FastAPI()
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(vocabulary.router, prefix="/vocabulary", tags=["vocabulary"])
app.include_router(combined.router, prefix="/combined", tags=["combined"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
app.include_router(summary.router, prefix="/summary", tags=["summary"])
#app.include_router(character_description.router, prefix="/character_description", tags=["character_description"])
app.include_router(character_list.router, prefix="/character_list", tags=["character_list"])
app.include_router(character_description.router, prefix="/character_description", tags=["character_description"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
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
    uvicorn.run(app, host="0.0.0.0", port=8000)