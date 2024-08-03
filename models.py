# from sqlalchemy import Table, Column, Integer, String, Float, Text, ForeignKey
# from pydantic import BaseModel, ValidationError

# books = Table(
#     "books",
#     Column("b_id", Integer, primary_key=True, index=True),
#     Column("book_title", String(255)),
#     Column("author", String(255)),
#     Column("file_path", String(255), nullable=False),
#     Column("last_read", Float, default=0.0),
#     Column("summary", Text),
# )

# characters = Table(
#     "characters",
#     Column("character_id", Integer, primary_key=True, index=True),
#     Column("book_id", Integer, ForeignKey("books.b_id")),
#     Column("name", String(255), nullable=False),
#     Column("description", Text),
#     Column("image_path", String(255)),
# )

# location = Table(
#     "location",
#     Column("location_id", Integer, primary_key=True, index=True),
#     Column("book_id", Integer, ForeignKey("books.b_id")),
#     Column("location_name", String(255), nullable=False),
#     Column("description", Text),
#     Column("image_path", String(255)),
# )



class Agent:
    def __init__(self, role, goal, verbose, backstory, llm):
        self.role = role
        self.goal = goal
        self.verbose = verbose
        self.backstory = backstory
        self.llm = llm

class Task:
    def __init__(self, description, expected_output, agent):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent