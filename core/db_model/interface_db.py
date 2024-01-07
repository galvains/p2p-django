import os

from models import db
from gino.schema import GinoSchemaVisitor

# from db_api.add_startup import add_all_servers

from loguru import logger

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
        # await add_all_servers()
    except Exception as ex:
        logger.error(ex)


def db_insert(connection, data: dict) -> None:
    try:
        with connection.cursor() as cursor:

            if data['exchange_id'] == 3:
                cursor.execute(f"""INSERT INTO app_ticketstable (nick_name, price, orders, available, max_limit, min_limit,
                                rate, pay_methods, currency, coin, trade_type, link, time_create, exchange_id)
                                SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s WHERE NOT EXISTS(
                                SELECT 1 FROM app_ticketstable
                                WHERE nick_name = %s AND link = %s)""",
                               (data['nick_name'], data['price'], data['orders'], data['available'],
                                data['max_limit'], data['min_limit'], data['rate'], data['pay_methods'],
                                data['currency'], data['coin'], data['trade_type'], data['link'],
                                data['exchange_id'], data['nick_name'], data['link']))
            else:
                cursor.execute(f"""INSERT INTO app_ticketstable (nick_name, price, orders, available, max_limit, min_limit,
                                rate, pay_methods, currency, coin, trade_type, link, time_create, exchange_id)
                                SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s WHERE NOT EXISTS(
                                SELECT 1 FROM app_ticketstable
                                WHERE nick_name = %s AND price = %s)""",
                               (data['nick_name'], data['price'], data['orders'], data['available'],
                                data['max_limit'], data['min_limit'], data['rate'], data['pay_methods'],
                                data['currency'], data['coin'], data['trade_type'], data['link'],
                                data['exchange_id'], data['nick_name'], data['price']))

            connection.commit()

    except Exception as ex:
        logger.error(f'DB-INSERT | {ex}')
        connection.rollback()
