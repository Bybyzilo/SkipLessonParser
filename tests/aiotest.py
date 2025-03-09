import sys, os
sys.path.extend(['../skiplessonparser', '../../skiplessonparser', 'tests'])

import asyncio
from skiplessonparser import AioGradebookParser
from skiplessonparser.models import UserAuthModel

from pprint import pprint

try:
    import config
except ImportError:
    print("[i] Не найден файл config.py с данными авторизации пользователя на lk.donstu.ru", end='\n\n')


username: str = os.getenv('USERNAME')
password: str = os.getenv('PASSWORD')

# if not (username and password):
#     print("Укажите данные авторизации")
#     sys.exit()


async def main():
    parser = AioGradebookParser()
    
    # Авторизация (обязательно)
    auth_data: UserAuthModel = await parser.auth(username, password)
    print(auth_data.data.user)
    
    items: dict[int, str] = await parser.journal.get_discipline_ids()
    pprint(items)
    
    journal = await parser.journal.get(379884)
    pprint(journal.data.journalData)

    


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())