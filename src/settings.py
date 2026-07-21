from typing import List, NamedTuple
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///database.db'
    debug: bool = False
    
    class Config:
        env_file = '.env'
        env_fule_encoding = 'utf-8'

class IMAGE_DIR(NamedTuple):
    raw: str
    preview: str
    
image_dir = IMAGE_DIR(raw='./uploads/image/raw', 
                      preview='./uploads/image/preview'
)
file_dir = './uploads/document/'

ALLOW_IMAGE_TYPE: List[str] = ["image/jpeg", "image/png", "image/webp"]
ALLOW_FILE_TYPE: List[str] = [
    "application/msword",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "text/plain",
    "application/pdf"
]

settings = Settings()