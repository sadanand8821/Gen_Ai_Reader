
import logging
from fastapi import APIRouter, HTTPException, Form
import time
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from crud import add_summary_to_book, get_book_path, get_summary_by_book_id
from langchain.memory import ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from router.chatbot import chat, start_conversation
from services import extract_text_and_title_from_epub

router = APIRouter()

logger = logging.getLogger(__name__)


# models.py

class Agent:
    def __init__(self, role, goal, verbose, backstory, llm):
        self.role = role
        self.goal = goal
        self.verbose = verbose
        #self.memory = self.memory
        self.backstory = backstory
        self.llm = llm

class Task:
    def __init__(self, description, expected_output, agent):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent

def avid_summary(book_title, story, readerType):
    google_model=ChatGoogleGenerativeAI(model = "gemini-1.5-flash", 
                            verbose = True,
                            temperature=0.5,
                            google_api_key="",
                             convert_system_message_to_human=True
                            )
    history = ChatMessageHistory()

    # Adding messages to history
    history.add_user_message("Hello, how can I improve my storytelling?")
    history.add_ai_message("Here are some tips to improve your storytelling...")

    # Create messages
    messages = [
        HumanMessage(content="Analyze the provided story text to extract main plot points, characters, and themes."),
        SystemMessage(content="You are an assistant helping to analyze and summarize books."),
        HumanMessage(content="The story text goes here.")
    ]
    avid_book_analyst_agent, avid_creative_writer_agent, avid_editor_agent = agents(google_model, readerType)
    avid_book_analyst_task = tasks(avid_book_analyst_agent, story, book_title)
    avid_analysis_result = google_model.invoke(
    input=[HumanMessage(content=avid_book_analyst_task.description)]
    )
    avid_key_points = avid_analysis_result.content.strip()
    avid_creative_writer_task_description = f'Create an in-depth and engaging summary of the book based on its key plot points, characters, and themes extracted by the Book Analyst AI. The key points are: {avid_key_points}'
    avid_summary_result = google_model.invoke(
        input=[HumanMessage(content=avid_creative_writer_task_description)]
    )
    avid_draft_summary = avid_summary_result.content.strip()  # Extract the result content

    avid_editor_task_description = f"Review and edit the provided summary for clarity, engagement, and accuracy. The summary is: '{avid_draft_summary}'. The output should be a 300 word crisp and engaging summary"
    avid_edited_summary_result = google_model.invoke(
        input=[HumanMessage(content=avid_editor_task_description)]
    )
    avid_final_summary = avid_edited_summary_result.content.strip() 
    return avid_final_summary



def agents(google_model, readerType):
    avid_book_analyst_agent = Agent(
    role="you are a story analyst.",
    goal="To deeply analyze the provided story and extract the main plot points, characters, and themes in an in-depth manner.",
    verbose=True,
    backstory="""As a literary analyst, the agent provides an in-depth understanding of the story's key elements.""",
    llm=google_model
    )

    avid_creative_writer_agent = Agent(
    role="You are a creative writer who crafts in-depth and engaging summaries for avid readers who appreciate nuanced storytelling and advanced English.",
    goal="To craft an in-depth and engaging summary of the book that captures the reader's interest, provides a thorough overview, and includes nuanced storytelling suitable for avid readers.",
    verbose=True,
    backstory="""This agent excels at creating in-depth, captivating summaries that are highly informative and engaging, tailored for avid readers who appreciate complexity and sophisticated language.""",
    llm=google_model
)
    
    regular_creative_writer_agent = Agent(
    role="You are a creative writer who crafts engaging summaries for regular readers who prefer clear and straightforward storytelling.",
    goal="To craft an engaging summary of the book that captures the reader's interest, provides a clear and thorough overview, and uses straightforward language suitable for regular readers.",
    verbose=True,
    backstory="""This agent excels at creating clear and captivating summaries that are highly informative and engaging, tailored for regular readers who prefer simplicity and clarity.""",
    llm=google_model
)
    casual_creative_writer_agent = Agent(
    role="You are a creative writer who crafts brief and engaging summaries for casual readers who prefer quick and easy-to-understand storytelling.",
    goal="To craft a brief and engaging summary of the book that captures the reader's interest, provides a concise overview, and uses simple language suitable for casual readers.",
    verbose=True,
    backstory="""This agent excels at creating brief, captivating summaries that are highly informative and engaging, tailored for casual readers who prefer quick and easy-to-understand storytelling.""",
    llm=google_model
)

    avid_editor_agent = Agent(
    role="you are a meticulous editor with a keen eye for detail and a passion for polished prose.",
    goal="To review and edit the summary for clarity, engagement, and accuracy.",
    verbose=True,
    backstory="""This agent ensures that the final summary is clear, engaging, and grammatically correct.""",
    llm=google_model
)
    if readerType == "avid":
        return avid_book_analyst_agent, avid_creative_writer_agent, avid_editor_agent
    elif readerType == "regular":
        return avid_book_analyst_agent, regular_creative_writer_agent, avid_editor_agent
    else:
        return avid_book_analyst_agent, casual_creative_writer_agent, avid_editor_agent
    

def tasks(avid_book_analyst_agent, story, book_title):
    return Task(
        description=f'Analyze the provided story text to extract main plot points, characters, and themes. The story text is: {story} and the title is {book_title}.',
        expected_output="An in-depth dictionary with keys 'plot', 'characters', and 'themes' containing the extracted information.",
        agent=avid_book_analyst_agent
    )
# Define endpoints
@router.post("/analyze_story/{book_id}/{readerType}")
async def analyze_story(book_id: int, readerType):
    try:
        file_path = await get_book_path(book_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    try:
        summary = await get_summary_by_book_id(book_id)
        print(len(summary))
        if(len(summary) == 4):
            title, story_text = extract_text_and_title_from_epub(file_path)
            avid_summary_final = avid_summary(title, story_text, readerType)
            
            await add_summary_to_book(book_id, avid_summary_final)
            return {"summary": avid_summary_final}
        else:
            return {"summary": summary}
            
        
    except ValueError as e:
        logger.error(f"Error fetching summary for book_id {book_id}: {e}")
        raise HTTPException(status_code=404, detail="Summary not found")
    
    
    # Assume extract_text_and_title_from_epub is defined elsewhere
    # title, story_text = extract_text_and_title_from_epub(file_path)
    # avid_summary_final = avid_summary(title, story_text)
    # return {"summary": avid_summary_final}



 
    

