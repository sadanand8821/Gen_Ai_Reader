import logging
import requests
from ebooklib import epub
from bs4 import BeautifulSoup
import ebooklib
import sys

logger = logging.getLogger(__name__)
async def fetch_meaning_from_api(word: str) -> str:
    DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    response = requests.get(f"{DICTIONARY_API_URL}{word}")
    if response.status_code == 200:
        data = response.json()
        logger.info(f"Received response from dictionary API: {data}")
        if isinstance(data, list) and data:
            meanings = data[0].get("meanings", [])
            if meanings:
                definition = meanings[0].get("definitions", [])[0].get("definition", "No definition found")
                logger.info(f"Extracted definition: {definition}")
                return definition
            

def extract_text_and_title_from_epub(epub_path: str):
    book = epub.read_epub(epub_path)
    text_content = []
    # Extract title
    title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else 'No title found'
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            text_content.append(soup.get_text())

    return title, '\n'.join(text_content)
   