from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import List, TypeVar, Generic

class ImageRecord(SQLModel, table=True):
    __tablename__: str = "image_records"

    id: int = Field(primary_key=True, default=None)
    slug: str = Field(max_length=50, unique=True)
    raw_filename: str = Field(max_length=255)
    mime_type: str = Field(max_length=50)
    size_bytes: int
    view: int = Field(default=0)
    uploaded_at: datetime = Field(default_factory=datetime.now)
    
    @staticmethod
    def gen_slug():
        return uuid4().hex
    

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="页码 从1开始")
    page_size: int = Field(default=10, ge=1, le=100, description="每页条数 最大100")

T = TypeVar("T")

class PageResponse(BaseModel, Generic[T]):
    total: int = Field(description="总记录数")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页条数")
    items: List[T] = Field(description="当前页数据列表")