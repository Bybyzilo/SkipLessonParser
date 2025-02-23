import sys, os
sys.path.extend(['../skiplessonparser', '../../skiplessonparser', 'tests'])

import asyncio
from skiplessonparser import AioGradebookParser
from skiplessonparser.models import UserAuthModel

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
    
    auth_data: UserAuthModel = await parser.auth(username, password)
    #print(auth_data.data.user)
    
    journal = await parser.journal.get('2024-2025', 2)
    print(journal)
    
    # journal = await parser.journal.get(journal_id=334392) # 334392 -> Деловая коммуникация
    
    # print(journal)

    


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())