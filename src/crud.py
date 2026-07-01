from typing import List, Optional
from sqlmodel import select, func, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from .model import ImageRecord, PageResponse


class ImageCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def list_paginated(self, page: int, page_size: int) -> PageResponse[ImageRecord]:
        count_stmt = select(func.count()).select_from(ImageRecord)
        total = await self.session.exec(count_stmt)
        total_count: int = total.one()
        
        offset = (page - 1) * page_size
        
        data_stmt = (
            select(ImageRecord)
            .offset(offset)
            .limit(page_size)
            .order_by(desc(ImageRecord.id))
        )
        results = await self.session.exec(data_stmt)
        items: List[ImageRecord] = list(results.all())
        return PageResponse(
            total=total_count,
            page=page,
            page_size=page_size,
            items=items
        )
    
    async def get_by_slug(self, slugname: str) -> Optional[ImageRecord]:
        stmt = select(ImageRecord).where(ImageRecord.slug == slugname)
        result = await self.session.exec(stmt)
        image = result.first()
        return image
    
    async def get_by_id(self, id: int) -> Optional[ImageRecord]:
        stmt = select(ImageRecord).where(ImageRecord.id == id)
        result = await self.session.exec(stmt)
        image = result.first()
        return image
    
    async def add(self, raw_filename: str, slug: str, mime_type: str, size: int) -> Optional[ImageRecord]:
        image_record = ImageRecord(
            raw_filename=raw_filename,
            slug=slug,
            mime_type=mime_type,
            size_bytes=size
        )
        item = self.session.add(image_record) 
        await self.session.commit()
        return item
    
    async def remove_by_slug(self, slugname: str) -> bool:
        image = await self.get_by_slug(slugname)
        if image is not None:
            await self.session.delete(image)
            await self.session.commit()
            return True
        return False

    async def remove_by_id(self, id: int) -> bool:
        image = await self.get_by_id(id)
        if image is not None:
            await self.session.delete(image)
            await self.session.commit()
            return True
        return False