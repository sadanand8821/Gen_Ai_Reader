from pydantic import BaseModel

class BookSchema(BaseModel):
    b_id: int
    book_title: str
    author: str
    file_path: str
    last_read: float
    summary: str
    cover_image_path: str

    class Config:
        orm_mode = True

class BookCreateSchema(BaseModel):
    book_title: str
    author: str
    file_path: str
    last_read: float = 0.0
    summary: str
    cover_image_path: str