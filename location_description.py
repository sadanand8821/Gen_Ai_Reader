from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from ebooklib import epub
from bs4 import BeautifulSoup
import logging
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)
api_key = os.getenv("GOOGLE_API_KEY")

google_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=api_key,
    convert_system_message_to_human=True
)

class LocationDescription:
    def __init__(self, pathToEpub, verbose=True):
        self.google_model = google_model
        self.pathToEpub = pathToEpub
        self.verbose = verbose
        self.epub_text, self.book_title = self.get_story_text(pathToEpub)
        self.agent_role = "A highly skilled literary analyst specializing in extracting detailed location descriptions from texts."
        self.agent_goal = "To meticulously analyze the provided text and extract comprehensive location descriptions that are vivid enough to create an image."
        self.agent_backstory = """As a literary analyst with years of experience in textual analysis, the agent has developed an unparalleled ability to
        delve into narratives and bring locations to life through words. This agent is trained to recognize subtle details and infer
        characteristics that paint a complete picture of each location. Equipped with an extensive understanding of literary techniques and 
        setting development, the agent excels in transforming textual information into vivid and engaging location profiles."""
        self.agent_task_description = f'Extract 10 vividly described locations from the provided text. The descriptions should be detailed enough to create an image. The text is {self.epub_text}.'
        self.agent_task_expected_output = """ {
            "Locations": [
                {
                    "Place": "Place1",
                    "Description": "Description of how the place is. This description should be as detailed as possible."
                },
                {
                    "Place": "Place2",
                    "Description": "Description of how the place is. This description should be as detailed as possible."
                }
            ]
        }"""

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

        return '\n'.join(text), title

    def run(self):
        location_extraction_agent = Agent(
            role=self.agent_role,
            goal=self.agent_goal,
            backstory=self.agent_backstory,
            verbose=self.verbose,
            llm=self.google_model
        )
        location_extraction_task = Task(
            description=self.agent_task_description,
            expected_output=self.agent_task_expected_output,
            agent=location_extraction_agent
        )
        location_extraction_crew = Crew(
            agents=[location_extraction_agent],
            tasks=[location_extraction_task],
            verbose=self.verbose
        )
        location_description = location_extraction_crew.kickoff()
        return location_description

