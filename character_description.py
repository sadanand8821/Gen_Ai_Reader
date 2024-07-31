from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from ebooklib import epub
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
import logging

logger = logging.getLogger(__name__)




google_model=ChatGoogleGenerativeAI(model = "gemini-1.5-flash", 
                            verbose = True,
                            temperature=0.5,
                            google_api_key="",
                            convert_system_message_to_human=True
                            )


class CharacterDescription:
    def __init__(self, pathToEpub, character_name, verbose=True):
          self.google_model = google_model
          self.pathToEpub = pathToEpub
          self.verbose = verbose
          self.epub_text, self.book_title = self.get_story_text(pathToEpub)
          self.character_name = character_name
          self.agent_role = "You are a story writer who has written all the novels in the world. Each story is your own story and you understand it by heart"
          self.agent_goal = "To provide a spoiler-free description of given character as if written by a fellow regular reader. Spoiler free means that the description should not reveal the plot of the story."

          self.agent_backstory = """As a literary analyst with years of experience in textual analysis, the agent has developed an unparalleled ability to bring
    a character to life through words. This agent has been trained to recognize subtle details and infer traits that paint a complete picture
    of given character. Equipped with an extensive understanding of literary techniques and character development, the agent excels
    in transforming textual information into vivid and engaging character profile for regular readers. The novels might also have some pages
    about the writer and his other books. Don't get confused by that"""
          self.agent_task_description = f'Provide a brief introduction of {self.character_name} for new readers of {self.epub_text} as if written by a fellow regular reader The introduction of {self.character_name} should be concise and to the point. The introduction should not reveal the plot of the story. The title of the book is {self.book_title}.'
          self.agent_task_expected_output = """[Character1, Character2, Character3, ...] where each character is a string."""




    def get_story_text(self, pathToEpub):
        book = epub.read_epub(pathToEpub)
        title = ""
        metadata = book.get_metadata('DC', 'title')
        if metadata:
            title = metadata[0][0]
        text = []

        for item in book.get_items():
            if item.media_type in {'application/xhtml+xml', 'text/html'}:
                soup = BeautifulSoup(item.get_body_content(), 'html.parser')
                text.append(soup.get_text())
                

          
        

        return '\n'.join(text),title
    

    
    def run(self):
         character_description_agent = Agent(
            role=self.agent_role,
            goal=self.agent_goal,
            backstory=self.agent_backstory,
            verbose=self.verbose,
            llm=self.google_model
         )
         character_description_task = Task(
            description=self.agent_task_description,
            expected_output=self.agent_task_expected_output,
            agent=character_description_agent
         )
         character_description_crew = Crew(
            agents=[character_description_agent],
            tasks=[character_description_task],
            verbose=self.verbose
         )
         character_description = character_description_crew.kickoff()
         return character_description