# async def get_word_meaning_from_db(word: str, book_id: int) -> str:
#     query = """
#     SELECT definition FROM vocabulary
#     WHERE word = :word AND book_id = :book_id
#     """
#     try:
#         row = await database.fetch_one(query, values={"word": word, "book_id": book_id})
#         if row:
#             logger.info(f"Found definition for word '{word}' in book_id {book_id}")
#             return row["definition"]
#         else:
#             logger.info(f"No definition found for word '{word}' in book_id {book_id}")
#             return None
#     except Exception as e:
#         logger.error(f"Error retrieving definition for word '{word}' in book_id {book_id}: {e}")
#         return None

# async def get_book_path(book_id: int) -> str:
#     query = "SELECT file_path FROM books WHERE b_id = :book_id"
#     result = await database.fetch_one(query, values={"book_id": book_id})
#     if result:
#         logger.info(f"Fetched book path for book_id: {book_id}")
#         return result["file_path"]
#     else:
#         logger.error(f"Book with id {book_id} not found")
#         raise HTTPException(status_code=404, detail="Book not found")
    
# async def get_unique_book_ids() -> list:
#     query = "SELECT DISTINCT book_id FROM characters"
#     try:
#         rows = await database.fetch_all(query)
#         print(rows)
#         unique_book_ids = [row["book_id"] for row in rows]
#         logger.info(f"Fetched unique book IDs: {unique_book_ids}")
#         return unique_book_ids
#     except Exception as e:
#         logger.error(f"Error retrieving unique book IDs: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# @app.get("/character-list/{bookId}")
# async def getCharacterLis(bookId: int):

#     if bookId in get_unique_book_ids():
#         query = "SELECT name FROM characters WHERE book_id = :bookId"
#         try:
#             rows = await database.fetch_all(query, values={"bookId": bookId})
#             characters = [row["name"] for row in rows]
#             logger.info(f"Retrieved {len(characters)} characters for bookId: {bookId}")
#             return {"character_list": characters}
#         except Exception as e:
#             logger.error(f"Error retrieving characters for bookId: {bookId}: {e}")
#             raise HTTPException(status_code=500, detail="Internal Server Error")
    
#     book_path = await get_book_path(bookId)
#     character_list = CharacterList(pathToEpub=book_path,verbose=True).run()
#     character_lists[bookId] = character_list
    
#     logger.info(f"Generated and cached character list for bookId: {bookId} and the character list is: {character_list}")
#     # Insert character names into the database
#     await insert_characters_into_db(bookId, character_list)


# async def insert_characters_into_db(book_id: int, character_list: list):
#     query = """
#     INSERT INTO characters (book_id, name)
#     VALUES (:book_id, :name)
#     ON CONFLICT (book_id, name) DO NOTHING
#     """
#     try:
#         actual_list = ast.literal_eval(character_list)
#         for character in actual_list:
#             try:
#                 await database.execute(query, values={"book_id": book_id, "name": character})
#                 logger.info(f"Inserted character '{character}' for book_id {book_id} into the database")
#             except Exception as e:
#                 logger.error(f"Error inserting character '{character}' into the database: {e}")

#         # Proceed with storing `actual_list` in the database
#     except SyntaxError as e:
#         print(f"SyntaxError: {e}")
#         # Handle the error or reformat the string



# @app.get("/meaning/{word}/{book_id}")
# async def get_word_meaning(word: str, book_id: int):
#     current_vocab_list = await get_words_by_book_id(book_id)
#     if word in current_vocab_list:
#         meaning = await get_word_meaning_from_db(word, book_id)
#         if meaning:
#             return {"word": word, "meaning": meaning}
#         else:
#             logger.info(f"Fetching meaning for word: {word}")
#             definition = await fetch_meaning_from_api(word)
#             if definition:
#                 words.append({"word": word, "definition": definition})
#                 await insert_word_into_db(word, definition, book_id)
#                 return {"word": word, "definition": definition}
#             raise HTTPException(status_code=404, detail="Word not found")
            


#     # If not found, fetch from the API
    

# async def fetch_meaning_from_api(word: str) -> str:
#     DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
#     response = requests.get(f"{DICTIONARY_API_URL}{word}")
#     if response.status_code == 200:
#         data = response.json()
#         logger.info(f"Received response from dictionary API: {data}")
#         if isinstance(data, list) and data:
#             meanings = data[0].get("meanings", [])
#             if meanings:
#                 definition = meanings[0].get("definitions", [])[0].get("definition", "No definition found")
#                 logger.info(f"Extracted definition: {definition}")
#                 return definition
#     return None

# async def insert_word_into_db(word: str, definition: str, book_id: int):
#     query = """
#     INSERT INTO vocabulary (word, definition, book_id)
#     VALUES (:word, :definition, :book_id)
#     ON CONFLICT (word) DO NOTHING
#     """
#     try:
#         await database.execute(query, values={"word": word, "definition": definition, "book_id": book_id})
#         logger.info(f"Inserted word '{word}' into vocabulary for book_id {book_id}")
#     except Exception as e:
#         logger.error(f"Error inserting word into vocabulary: {e}")


# async def get_characters_by_book_id(book_id: int):
#     query = """
#     SELECT name FROM characters
#     WHERE book_id = :book_id
#     """
#     try:
#         rows = await database.fetch_all(query, values={"book_id": book_id})
#         character_list = [row["name"] for row in rows]
#         logger.info(f"Retrieved {len(character_list)} characters for book_id {book_id}")
#         return character_list
#     except Exception as e:
#         logger.error(f"Error retrieving characters for book_id {book_id}: {e}")
#         return []
    
# async def get_words_by_book_id(book_id: int):
#     query = """
#     SELECT word FROM vocabulary
#     WHERE book_id = :book_id
#     """
#     try:
#         rows = await database.fetch_all(query, values={"book_id": book_id})
#         word_list = [row["word"] for row in rows]
#         logger.info(f"Retrieved {len(word_list)} words for book_id {book_id}")
#         return word_list
#     except Exception as e:
#         logger.error(f"Error retrieving words for book_id {book_id}: {e}")
#         return []

# @app.get("/characters/{book_id}")
# async def get_characters(book_id: int):
#     characters = await get_characters_by_book_id(book_id)
#     if not characters:
#         raise HTTPException(status_code=404, detail="Characters not found")
#     return {"book_id": book_id, "characters": characters}

# @app.get("/words/{word}/{book_id}")
# async def get_word_type(word: str, book_id: int):
#     current_character_list = await get_characters_by_book_id(book_id)
#     current_vocab_list = await get_words_by_book_id(book_id)
#     if word in current_character_list:
#         return {"word": word, "type": "character"}
#     elif word in current_vocab_list:
#         return {"word": word, "type": "vocabulary"}
#     else:
#         get_word_meaning(word=word, book_id=book_id)
    







# @router.post("/create_summary/")
# async def create_summary(book_id: int):
#     try:
#         file_path = await get_book_path(book_id)
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
    
#     # Assume extract_text_and_title_from_epub is defined elsewhere
#     title, story_text = extract_text_and_title_from_epub(file_path)

#     avid_book_analyst_task = Task(
#         description=f'Analyze the provided story text to extract main plot points, characters, and themes. The story text is: {story_text} and the title is {title}.',
#         expected_output="An in-depth dictionary with keys 'plot', 'characters', and 'themes' containing the extracted information.",
#         agent=avid_book_analyst_agent
#     )

#     analysis_result = avid_book_analyst_agent.llm.generate(prompts=[avid_book_analyst_task.description])
#     key_points = analysis_result.generations[0][0].text.strip()  # Assuming the result is a list of strings

#     avid_creative_writer_task = Task(
#         description=f'Create an in-depth and engaging summary of the book {title} for avid readers based on its key plot points, characters, and themes extracted by the Book Analyst AI. The key points are: {key_points}',
#         expected_output="An in-depth and engaging summary that provides a thorough overview of the book.",
#         agent=avid_creative_writer_agent
#     )

#     start_time = time.time()
#     summary_result = avid_creative_writer_agent.llm.generate(prompts=[avid_creative_writer_task.description])
#     draft_summary = summary_result.generations[0][0].text.strip()  # Assuming the result is a list of strings
