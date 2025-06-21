import os

from dotenv import load_dotenv

load_dotenv()

from tortoise import Tortoise

TORTOISE_ORM = {
    'connections': {'default': os.getenv('DATABASE_URL', '')},
    'apps': {
        'models': {
            'models': ['aerich.models', 'app.models'],
            'default_connection': 'default',
        }
    },
}


async def connect_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)


async def close_db():
    await Tortoise.close_connections()
