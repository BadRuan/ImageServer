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
    
image_dir = IMAGE_DIR(raw='./uploads/raw', 
                      preview='./uploads/preview'
                      )
ALLOW_TYPE: List[str] = ["image/jpeg", "image/png", "image/webp"]

settings = Settings()