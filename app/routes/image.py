from fastapi import APIRouter, File, UploadFile

from app.modules.algorithm import search_images
from app.modules.image import upload_image

router = APIRouter(prefix='/image', tags=['Image'])


@router.get('/search')
async def search_image(query: str):
    return await search_images(query)


@router.post('/upload')
async def upload(file: UploadFile = File(...)):
    return await upload_image(file)
