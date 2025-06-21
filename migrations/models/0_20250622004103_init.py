from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "image" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "path" VARCHAR(255) NOT NULL UNIQUE,
    "filename" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "tags" TEXT[] NOT NULL,
    "description_chosung" VARCHAR(255),
    "tags_chosung" TEXT[],
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
