import asyncio
import random
import pickle

from loguru import logger
from threading import Thread
from utils.proxies import set_proxy
from .task_manager import distributor
from utils.methods import get_payment_methods
from db_model.commands import remove_old_ticket, get_all_tickets
from .engine import distributor_binance, distributor_paxful, distributor_bybit, distributor_okx


class TaskManager(object):
    """
    Менеджер для создания задач, исходя из данных прокси
    """

    def __init__(self, proxy_data: dict, threads_data: tuple, number: int):
        self.proxy = proxy_data
        self.data = threads_data
        self.number = number

    def get_all(self, limit, pg_limit, _DEBUG):
        for i in range(len(self.data)):
            data = self.data[i]

            for thr in data:
                coin = thr[0]
                fiat = thr[1]
                trade = thr[2]

                if _DEBUG:
                    if i == 0:
                        asyncio.create_task(
                            distributor_binance(coin, fiat, trade, self.proxy, limit, pg_limit))
                        logger.debug(f'create-task-binance | {coin, fiat, trade, self.proxy["name"]}')
                    if i == 1:
                        asyncio.create_task(distributor_bybit(coin, fiat, trade, self.proxy, limit, pg_limit))
                        logger.debug(f'create-task-bybit | {coin, fiat, trade, self.proxy["name"]}')
                    if i == 2:
                        asyncio.create_task(distributor_paxful(coin, fiat, trade, self.proxy, limit)),
                        logger.debug(f'create-task-paxful | {coin, fiat, trade, self.proxy["name"]}')
                    if i == 3:
                        asyncio.create_task(distributor_okx(coin, fiat, trade, self.proxy, limit)),
                        logger.debug(f'create-task-okx | {coin, fiat, trade, self.proxy["name"]}')
                else:
                    if i == 0:
                        asyncio.create_task(
                            distributor_binance(coin, fiat, trade, self.proxy, limit, pg_limit))
                    if i == 1:
                        asyncio.create_task(distributor_bybit(coin, fiat, trade, self.proxy, limit, pg_limit))
                    if i == 2:
                        asyncio.create_task(distributor_paxful(coin, fiat, trade, self.proxy, limit)),
                    if i == 3:
                        asyncio.create_task(distributor_okx(coin, fiat, trade, self.proxy, limit))

        if _DEBUG:
            logger.debug(f'current-proxy | {self.proxy["name"], self.proxy["url"]}')


async def loader(conf_data: dict) -> None:
    # чтение данных из файла конфигурации
    _DEBUG = conf_data['DEBUG']

    pg_limit = conf_data['page_limit']
    lap_of_reload = conf_data['lap_of_reload']
    delay = random.randint(conf_data['delay'][0], conf_data['delay'][1])
    limit = random.randint(conf_data['limit'][0], conf_data['limit'][1])

    logger.info(f'>>> Pool created... | Debug mod: {_DEBUG} <<<')
    counter_laps = 1

    # запуск цикла парсинга
    while True:
        try:
            logger.info(f'>>> Lap: {counter_laps} | Total tickets: {await get_all_tickets()} <<<')
            await remove_old_ticket()

            # запуск дистрибьютора (на первый круг и кратный указанному в конфигурации)
            if counter_laps == 1 or counter_laps % lap_of_reload == 0:
                await get_payment_methods()
                await distributor(conf_data=conf_data, counter_to_change=1)

            # конфиг тредов (из дистрибьютора)
            with open('tmp/threads.data', 'rb') as file:
                threads_data = pickle.load(file)

            # список тредов и вызов прокси
            thr_list = list()
            proxies = set_proxy(conf_data=conf_data)

            bin_tasks, byb_tasks, pax_tasks, okx_tasks = threads_data[0], threads_data[1], threads_data[2], \
                                                         threads_data[3]
            len_tasks = max(len(bin_tasks), len(byb_tasks), len(pax_tasks), len(okx_tasks))

            # создание объектов таск_менеджера (bin, byb, pax | bin, byb ...)
            for elem in range(len_tasks):
                data = (bin_tasks[elem], byb_tasks[elem], pax_tasks[elem], okx_tasks[elem])
                thr_list.append(TaskManager(proxy_data=proxies[elem], threads_data=data, number=elem))

            for elem in thr_list:
                thr = Thread(target=elem.get_all(limit, pg_limit, _DEBUG))
                thr.start()
                thr.join()

            # кулдаун между кругами цикла
            await asyncio.sleep(delay)
            counter_laps += 1

        except Exception as ex:
            logger.error(f'loader | {ex}')
