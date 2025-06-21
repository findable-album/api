import time

from fastapi import APIRouter, File, UploadFile

from app.models import Image
from app.modules.algorithm import search_images
from app.modules.image import delete_image, upload_image

router = APIRouter(prefix='/image', tags=['Image'])


@router.get('')
async def get_all_images():
    return await Image.all()


@router.get('/search')
async def search_image(query: str):
    start_time = time.time()
    result = await search_images(query)
    end_time = time.time()
    print(f'Search took {end_time - start_time} seconds')
    return result


@router.post('/upload')
async def upload(file: UploadFile = File(...)):
    result = await upload_image(file)
    return result


@router.delete('/{image_id}')
async def delete(image_id: int):
    await delete_image(image_id)
    return {'message': 'Image deleted successfully'}
