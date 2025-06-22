import os
import uuid

from fastapi import UploadFile

from app.core.openai_client import get_openai_client
from app.models import Image
from app.modules.algorithm.extract_chosung import extract_chosung
from app.modules.image.description import analyze_image_with_openai

IMAGE_DIR = 'static/images'


async def upload_image(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1]
    filename = f'{uuid.uuid4().hex}{ext}'
    filepath = os.path.join(IMAGE_DIR, filename)

    os.makedirs(IMAGE_DIR, exist_ok=True)

    with open(filepath, 'wb') as f:
        f.write(file.file.read())

    client = get_openai_client()
    image_description = analyze_image_with_openai(filepath, client)

    description = image_description.get('description', '')
    tags = image_description.get('tags', [])

    description_chosung = extract_chosung(description) if description else None
    tags_chosung = [extract_chosung(tag) for tag in tags]

    image = await Image.create(
        path=f'/{IMAGE_DIR}/{filename}',
        filename=file.filename,
        description=description,
        tags=tags,
        description_chosung=description_chosung,
        tags_chosung=tags_chosung,
    )

    return image


async def delete_image(image_id: int) -> None:
    image = await Image.get(id=image_id)

    filepath = os.path.join(IMAGE_DIR, os.path.basename(image.path))
    if os.path.exists(filepath):
        os.remove(filepath)

    await image.delete()
