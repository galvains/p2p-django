import os

from loguru import logger
from gino.schema import GinoSchemaVisitor

from db_model.models import db
from db_model.commands import add_exchanges

POSTGRES_DB = os.getenv('CLR_DB_NAME')
POSTGRES_USER = os.getenv('CLR_DB_USER')
POSTGRES_PASSWORD = os.getenv('CLR_DB_PASS')
DB_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@database:5432/{POSTGRES_DB}'


async def create_db():
    try:
        db.gino: GinoSchemaVisitor
        await db.set_bind(DB_URI)

        await db.gino.drop_all()
        await db.gino.create_all()

        await add_exchanges()
    except Exception as ex:
        logger.error(ex)
