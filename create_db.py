from asyncio import run
from src.database import create_db

async def main() -> None:
    await create_db()


if __name__ == "__main__":
    run(main())