import sys, os
sys.path.extend(['../skiplessonparser', '../../skiplessonparser', 'tests'])

import asyncio
from skiplessonparser import AioGradebookParser
from skiplessonparser.models import UserAuthModel

from pprint import pprint

try:
    import config
except ImportError:
    pass


username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

if not (username and password):
    print("Укажите данные авторизации")
    sys.exit()


async def main():
    parser = AioGradebookParser()
    
    # Авторизация (обязательно)
    auth_data: UserAuthModel = await parser.auth(username, password)
    print(auth_data.data.user)
    
    items: dict[int, str] = await parser.journal.get_discipline_ids()
    pprint(items)

    


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())