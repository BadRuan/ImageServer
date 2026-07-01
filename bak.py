from asyncio import run
from sqlmodel import select
from src.database import get_session, create_db
from src.model import ImageRecord

async def create():
    await create_db()

async def test_insert_data():
    async with get_session() as session:
        for i in range(11, 121):
            image = ImageRecord(
                raw_filename= f'original_name_{i}',
                slug=ImageRecord.gen_slug(),
                mime_type= 'jpg',
                size_bytes= 100
            )
            session.add(image)
        await session.commit()
    
async def list_all():
    async with get_session() as session:
        stmt = select(ImageRecord).limit(10)
        results = await session.exec(stmt)
        for i in results:
            print(i.raw_filename)


if __name__ == "__main__":
    # run(create())
    run(test_insert_data())
    # run(list_all())
    ...