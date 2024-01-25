import yaml
import asyncio

from loguru import logger
import collectors.launcher as launcher
from db_model.interface_db import create_db

logger.add('tmp/debug.log', format='{time} | {level} | {message}', level='DEBUG',
           rotation='20 mb', compression='zip')


async def startup():
    await create_db()
    with open('configuration.yaml', 'r') as file:
        conf_data = yaml.safe_load(file)

    await launcher.loader(conf_data=conf_data)


if __name__ == '__main__':
    asyncio.run(startup())
