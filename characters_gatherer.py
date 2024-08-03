from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI
from ebooklib import epub
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from google.cloud.aiplatform_v1beta1.types.content import SafetySetting 
from vertexai.preview.generative_models import HarmCategory, HarmBlockThreshold 
from google.cloud.aiplatform_v1beta1.types.content import SafetySetting
from dotenv import load_dotenv
import os

api_key = os.getenv("GOOGLE_API_KEY")

google_model=ChatGoogleGenerativeAI(model = "gemini-1.5-flash", 
                            verbose = True,
                            temperature=0.5,
                            google_api_key=api_key,
                            convert_system_message_to_human=True
                            )

llama_model = Ollama(model = "llama3")
phi_model = Ollama(model = "phi3:14b")
gemma_model = Ollama(model="gemma2")


class CharacterList:
    def __init__(self, pathToEpub, verbose=True):
        self.google_model = google_model
        self.llama_model = llama_model
        self.phi_model = phi_model
        self.gemma_model = gemma_model
        self.pathToEpub = pathToEpub
        self.verbose = verbose
        self.epub_text, self.book_title = self.get_story_text(pathToEpub)
        self.agent_role = "You are a story writer who has written all the novels in the world. Each story is your own story and you understand it by heart."
        self.agent_goal = "To meticulously analyze the provided story and extract the names of all characters based on their first appearance."
        self.agent_backstory = """As a literary analyst with years of experience in story analysis, the agent has developed an unparalleled ability
    to identify characters in narratives. This agent excels in recognizing and listing character names from textual information."""
        self.agent_task_description = f'Extract the names of all characters in the provided story. The story is: {self.epub_text}. The story title is {self.book_title}. In some stories the author provides the character list. Make sure you refer to that as well if available. You do not have to provide a summary of your work. Just provide the list of characters.'
        self.agent_task_expected_output = """A python list of strings exactly like the following: ['Character1', 'Character2', 'Character3', ...] where each character is a string."""

    
    def get_story_text(self, pathToEpub):
        book = epub.read_epub(pathToEpub)
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
        character_list_agent = Agent(
            role=self.agent_role,
            goal=self.agent_goal,
            backstory=self.agent_backstory,
            verbose=self.verbose,
            llm=self.google_model
        )

        character_list_task = Task(
            description=self.agent_task_description,
            expected_output=self.agent_task_expected_output,
            agent=character_list_agent
        )
        character_list_crew = Crew(
            agents=[character_list_agent],
            tasks=[character_list_task],
            verbose=self.verbose
        )
        character_list =  character_list_crew.kickoff()
        return character_list
