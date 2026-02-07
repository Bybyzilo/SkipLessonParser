import sys
import os
sys.path.extend(['../donstuapi', '../../donstuapi', 'tests'])

import asyncio  # noqa: F401
from donstuapi import DonstuAPI, AioDonstuAPI
from donstuapi.models import UserAuthModel

# from pprint import pprint
from dotenv import load_dotenv

if not load_dotenv('.venv/.env'):
    print("[WARNING] Не удалось загрузить файл с переменными окружения", end='\n\n')



username: str = os.getenv('EMAIL', "")
password: str = os.getenv('PASSWORD', "")



def sync_client():
    donstu = DonstuAPI()
    
    # Авторизация (обязательно)
    auth_data: UserAuthModel | None = donstu.auth(username, password)  # noqa: F841
    #print(auth_data.data.user)
    
    print(donstu.account.user_id)

        
    
    

async def async_client():
    donstu = AioDonstuAPI()
    
    # Авторизация (обязательно)
    auth_data: UserAuthModel = await donstu.auth(username, password) # type: ignore
    # print(auth_data.data.user)
    
    # items: dict[int, str] = await donstu.journal.get_discipline_ids()
    # pprint(items)
    
    # journal = await donstu.journal.get(379884)
    # pprint(journal.data.journalData)
    
    # info = await donstu.account.info
    # print(info)
    
    # print(donstu.account.user_id)
    
    # data = await donstu.recordbook.info()
    # print(data)
    while True:
        name = input("Введите ФИО студента: ")
        __import__("os").system("cls")
        print()
        prepods = await donstu.tools.get_students_by_fio(name)
        for stud in prepods.data.arrStud:
            print(stud.fio, stud.userID, sep = " | ")
            # print(stud.birthday)
            print(stud)
            print("="*50)
        
        # a = await donstu.journal.list()
        # print(a)
    
    


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(async_client())
    # sync_client()
    
    ...