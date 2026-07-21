from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from os import path
from fastapi import Depends, UploadFile, HTTPException, status, Query
from fastapi.responses import FileResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.settings import file_dir, ALLOW_FILE_TYPE
from src.database import get_session
from src.service import DocumentService
from src.model import PageResponse


router = APIRouter()

   
@router.get('/document', response_model=PageResponse)
async def get_documents(
    page: int = Query(default=1, ge=1 ,description='页码'),
    page_size: int = Query(default=30, ge=1, le=100, description='每页条数'),
    session: AsyncSession = Depends(get_session)
):
    service = DocumentService(session)
    return await service.list_paginated(page, page_size)

@router.post('/document')
async def create_upload_file(file: UploadFile, session: AsyncSession = Depends(get_session)):
    if file.content_type not in ALLOW_FILE_TYPE:
        raise HTTPException(
            status_code=400,
            detail="仅支持txt、pdf、doc、docx、xls、xlsx格式的文件"
        )
    
    filename = file.filename or 'default_name'
    content = await file.read()
    service = DocumentService(session)
    _file = await service.add(filename=filename, mime_type=str(file.content_type), content=content)
    if _file is not None:
        return {
        "filename": file.filename, 
        "slug": _file.slug,
        "content_type": file.content_type,
        }
    else:
        raise HTTPException(
            status_code=400,
            detail="上传失败"
        )

@router.get('/document/{slug}')
async def get_document(slug, session: AsyncSession = Depends(get_session)):
    service = DocumentService(session)
    _file = await service.get_by_slug(slug)
    if _file is not None:
        return FileResponse(
                filename=_file.raw_filename,
                path=path.join(file_dir, slug), 
                media_type=_file.mime_type,  
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail='Document not found'
    )


@router.delete('/document/{slug}')
async def delete_image(slug, session: AsyncSession = Depends(get_session)):
    service = DocumentService(session)
    _file = await service.get_by_slug(slug)
    if _file is not None:
        flag = await service.remove_by_slug(slug)
        if flag:
            return {"message": "delete successful"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail='Document not found'
    )