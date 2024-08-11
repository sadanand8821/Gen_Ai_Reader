import logging
import requests
from ebooklib import epub
from bs4 import BeautifulSoup
import ebooklib
import sys
import os

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

def get_cover_image(path_to_epub, book_title, output_folder='/Users/sadanandsingh/Desktop/GenAIEBookReader/eBookReaderUI/src/app/mock/coverImages'):
    book = epub.read_epub(path_to_epub)
    cover_image = None
    cover_name = book_title
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # First try the standard cover item type
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_COVER:
            cover_image = item.get_content()
            cover_name = item.get_name().split('/')[-1]
            break

    # If not found, look for common cover image names
    if not cover_image:
        common_cover_names = ['cover', 'cover-image', 'coverpage', 'coverimage']
        for item in book.get_items():
            if any(name in item.get_name().lower() for name in common_cover_names):
                cover_image = item.get_content()
                cover_name = item.get_name().split('/')[-1]
                break

    # If a cover image is found, save it to the specified folder
    if cover_image:
        cover_path = os.path.join(output_folder, cover_name)
        with open(cover_path, 'wb') as f:
            f.write(cover_image)
        return cover_path
    else:
        print("No cover image found in the EPUB file.")
        return None

   