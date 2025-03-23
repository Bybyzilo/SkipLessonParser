import sys
import os
sys.path.extend(['../donstuapi', '../../donstuapi', 'tests'])

import asyncio  # noqa: F401
from donstuapi import DonstuAPI, AioDonstuAPI
from donstuapi.models import UserAuthModel

from pprint import pprint as print
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
    
    print(donstu.account.user_id)
    
    
    # Получение списка дисциплин (iD: название)
    # items: dict[int, str] = donstu.journal.get_discipline_ids()
    # pprint(items)
    
    # # Получение определенного журала
    # journal = donstu.journal.get(379884)
    # pprint(journal.data.journalData)

donstu = AioDonstuAPI()
async def async_client():
    global donstu
    
    # Авторизация (обязательно)
    auth_data: UserAuthModel = await donstu.auth(username, password) # noqa: F841
    # print(auth_data.data.user)
    
    # items: dict[int, str] = await donstu.journal.get_discipline_ids()
    # pprint(items)
    
    # journal = await donstu.journal.get(379884)
    # pprint(journal.data.journalData)
    
    # info = await donstu.account.info
    # print(info)
    
    print(donstu.account.user_id)
    
    data = await donstu.recordbook.info()
    print(data)
    
    


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(async_client())
    #sync_client()
    
    ...