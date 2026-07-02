from asyncio import run
from src.database import create_db
from src.model import ImageRecord

if __name__ == "__main__":
    run(create_db())
    