from loguru import logger
from asyncpg import UniqueViolationError
from datetime import datetime, timedelta

from db_model.models import TicketsTable, ExchangeTable, db


async def add_exchanges() -> None:
    try:
        await add_exchange_to_db(id=1, name='Binance')
        await add_exchange_to_db(id=2, name='Bybit')
        await add_exchange_to_db(id=3, name='Paxful')
        await add_exchange_to_db(id=4, name='OKX')
    except Exception as ex:
        logger.error(f'add-exchanges | {ex}')


async def add_ticket_to_db(**kwargs) -> None:
    try:
        if kwargs['exchange_id'] == 3:
            existing_record = await TicketsTable.query.where(TicketsTable.link == kwargs['link']).gino.first()
            if not existing_record:
                await TicketsTable(**kwargs).create()
        else:
            existing_record = await TicketsTable.query.where(TicketsTable.nick_name == kwargs['nick_name']).where(
                TicketsTable.price == kwargs['price']).gino.first()
            if not existing_record:
                await TicketsTable(**kwargs).create()
    except UniqueViolationError as ex:
        logger.error(f'add-ticket-to-db | {ex}')


async def add_exchange_to_db(**kwargs) -> None:
    try:
        await ExchangeTable(**kwargs).create()
    except UniqueViolationError as ex:
        logger.error(f'add-exchange-to-db | {ex}')


async def remove_old_ticket():
    try:
        one_min_ago = datetime.now() - timedelta(minutes=1)
        await TicketsTable.delete.where(TicketsTable.time_create < one_min_ago).gino.status()
    except Exception as ex:
        logger.error(f'remove-old-ticket | {ex}')


async def get_all_tickets():
    try:
        count = await db.func.count(TicketsTable.id).gino.scalar()
        return count
    except Exception as ex:
        logger.error(f'get-all-tickets | {ex}')
