from models import TicketsTable, ExchangeTable
from asyncpg import UniqueViolationError


async def add_ticket_to_db(**kwargs) -> None:
    try:
        await TicketsTable(**kwargs).create()
    except UniqueViolationError:
        print('ticket not added')


async def add_exch_to_db(**kwargs) -> None:
    try:
        await ExchangeTable(**kwargs).create()
    except UniqueViolationError:
        print('key not added')


async def remove_ticket(**kwargs):
    await TicketsTable(**kwargs).delete()


async def remove_exch(**kwargs):
    await ExchangeTable(**kwargs).delete()


async def get_all_tickets():
    return await TicketsTable.query.gino.all()


async def get_all_exch():
    return await ExchangeTable.query.gino.all()
