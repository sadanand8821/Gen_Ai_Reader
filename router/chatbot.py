from fastapi import APIRouter, HTTPException, Form
import datetime
import time
import logging
from typing import Dict, Any
import google.generativeai as genai
from google.generativeai import caching
import os
from dotenv import load_dotenv

from crud import get_book_path, get_vocabulary
from services import extract_text_and_title_from_epub

api_key = os.getenv("GOOGLE_API_KEY")

model = genai.GenerativeModel('gemini-1.5-flash-001')
genai.configure(api_key=api_key)


router = APIRouter()

logger = logging.getLogger(__name__)

tough_list = get_vocabulary()
print(tough_list)
initial_content = ""
initial_context = f"You are Maya, an expert reader of story books and novels. You will be my read-along buddy while I read this book. Help me understand the characters, plots, vocabulary, writing style in the book better as we go along. Give me spoiler-free content and confirm with me before giving content that contains major spoilers. Try to include some words from {tough_list}, if applicable."

# Global variables to maintain the model and context
model = None
cache = None
context = initial_content

def update_cache(context, user_input, model_response):
    new_content = f"{context}\nUser: {user_input}\nAssistant: {model_response}"
    updated_cache = caching.CachedContent.create(
        model="models/gemini-1.5-flash-001",
        display_name="multi_turn_conversation_updated",
        system_instruction=initial_context,
        contents=[new_content],
        ttl=datetime.timedelta(minutes=10),
    )
    return updated_cache, new_content

@router.post("/start/{book_id}")
async def start_conversation(book_id: int):
    global cache, context, model
    file_path = await get_book_path(book_id)
    title, story_text = extract_text_and_title_from_epub(file_path)
    tough_list = await get_vocabulary()
    system_instructions = f"You are Maya, an expert reader of story books and novels. You will be my read-along buddy while I read this book. Help me understand the characters, plots, vocabulary, writing style in the book better as we go along. Give me spoiler-free content and confirm with me before giving content that contains major spoilers. Try to include some words from {tough_list}, if applicable as these are words I have added to my vocabulary and I want to reinforce these words."
    print(tough_list)
    cache = caching.CachedContent.create(
        model="models/gemini-1.5-flash-001",
        display_name="multi_turn_conversation",
        system_instruction=initial_context,
        contents=[story_text],
        ttl=datetime.timedelta(minutes=10),
    )
    model = genai.GenerativeModel.from_cached_content(cached_content=cache)
    context = story_text
    return {"message": "Conversation started with book", "book_id": book_id}



@router.post("/chat/{book_id}")
async def chat(book_id, user_input: str = Form(...)):
    global cache, context, model
    if model is None or cache is None:
        start_conversation(book_id=book_id)
        #raise HTTPException(status_code=400, detail="Conversation not started. Please start the conversation with a book first.")
    try:
        response = model.generate_content([user_input])
        # if 'safety_ratings' in response.json():
        #     safety_ratings = response.json().get('safety_ratings')
        #     if safety_ratings.get('blocked'):
        #         raise ValueError("Response was blocked due to safety ratings.")
        # if not response.parts:
        #     raise HTTPException(status_code=500, detail="No valid response parts returned. Please try again or check for issues.")
        
        model_response = response.text
        usage_metadata = response.usage_metadata
        token_usage = {
            "prompt_token_count": usage_metadata.prompt_token_count,
            "candidates_token_count": usage_metadata.candidates_token_count,
            "total_token_count": usage_metadata.total_token_count,
            "cached_content_token_count": usage_metadata.cached_content_token_count
        }
        
        cache, context = update_cache(context, user_input, model_response)
        model = genai.GenerativeModel.from_cached_content(cached_content=cache)
        
        return {
            "user_input": user_input,
            "model_response": model_response,
            "token_usage": token_usage
        }
    except Exception as e:
        logger.error(f"Error during chat: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")