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
                            google_api_key="AIzaSyCOxH_uyvwcxgIZAM3GXM94v1Z-n2A08-4",
                            convert_system_message_to_human=True
                            )
class ChapterSummary:
    def __init__(self, pathToEpub, chapter_number, verbose=True):
            self.google_model = google_model
            self.pathToEpub = pathToEpub
            self.verbose = verbose
            self.epub_text, self.book_title = self.get_story_text(pathToEpub)
            self.chapter_number = chapter_number
            self.agent_role = "You are a story writer who has written all the novels in the world. Each story is your own story and you understand it by heart"
            self.agent_goal = f"To provide a detailed and insightful summary of chapter {chapter_number} of the given book as if written by a fellow regular reader. The summary should be spoiler-free and should not reveal the plot of the story."
            self.agent_backstory = """As a literary analyst with years of experience in textual analysis, the agent has developed an unparalleled ability to bring a story to life through words. This agent has been trained to recognize subtle details and infer themes that paint a complete picture of the story. Equipped with an extensive understanding of literary techniques and narrative structure, the agent excels in transforming textual information into vivid and engaging chapter summaries for regular readers."""
            self.agent_task_description = f'Provide a detailed and insightful summary of chapter {chapter_number} of the book {self.book_title} as if written by a fellow regular reader. The summary should be concise and to the point.'
            self.agent_task_expected_output = """Summary of the given chapter."""


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
        chapter_summary_agent = Agent(
             role=self.agent_role,
             goal=self.agent_goal,
             backstory=self.agent_backstory,
             verbose=self.verbose,
             llm=self.google_model
        )
        chapter_summary_task = Task(
            description=self.agent_task_description,
            expected_output=self.agent_task_expected_output,
            agent=chapter_summary_agent
        )
        chapter_summary_crew = Crew(
             agents=[chapter_summary_agent],
             tasks=[chapter_summary_task],
             verbose=self.verbose
        )
        chapter_summary = chapter_summary_crew.kickoff()
        return chapter_summary