import sys
import os
sys.path.extend(['../donstuapi', '../../donstuapi', 'tests'])

import asyncio  # noqa: F401
from donstuapi import DonstuAPI, AioDonstuAPI
from donstuapi.models import UserAuthModel

from pprint import pprint
from dotenv import load_dotenv

if not load_dotenv('.venv/.env'):
    print("[WARNING] Не удалось загрузить файл с переменными окружения", end='\n\n')



username: str = os.getenv('EMAIL')
password: str = os.getenv('PASSWORD')



def sync_client():
    donstu = DonstuAPI()
    
    # Авторизация (обязательно)
    auth_data: UserAuthModel = donstu.auth(username, password)  # noqa: F841
    #print(auth_data.data.user)
    
    # Получение списка дисциплин (iD: название)
    items: dict[int, str] = donstu.journal.get_discipline_ids()
    pprint(items)
    
    # Получение определенного журала
    journal = donstu.journal.get(379884)
    pprint(journal.data.journalData)


async def async_client():
    donstu = AioDonstuAPI()
    
    # Авторизация (обязательно)
    auth_data: UserAuthModel = await donstu.auth(username, password)
    print(auth_data.data.user)
    
    items: dict[int, str] = await donstu.journal.get_discipline_ids()
    pprint(items)
    
    journal = await donstu.journal.get(379884)
    pprint(journal.data.journalData)
    


if __name__ == '__main__':
    #asyncio.get_event_loop().run_until_complete(async_client())
    sync_client()
    
    ...