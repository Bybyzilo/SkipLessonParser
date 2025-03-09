from httpx import AsyncClient, Response, Cookies

from skiplessonparser.api.base_models import BaseParserModel
from skiplessonparser.models import UserAuthModel, JournalListModel, JournalModel


class AioGradebookParser(BaseParserModel["AioGradebookParser"]):
    def __init__(self):
        super().__init__()
        
        self.client = AsyncClient()
        self.client.headers = self.meta.headers
        
    
    class Auth(BaseParserModel.Auth):
        async def _auto_set_cookies(self) -> None:
            """ Автоматически получает и устанавливает cookies в self.client """
            
            await self.gradebook_parser.client.get(self.meta.urls.main_url)
        
        
        async def _get_random_identity(self) -> str:
            response: Response = await self.gradebook_parser.client.get(self.meta.urls.get_random_identity)
            
            return super()._get_random_identity(response)

        
        async def __call__(self, username: str, password: str) -> UserAuthModel:
            """ Авторизация пользователя и получение токена
            
            Аргументы:
                username, password (str) -> данные для авторизации на lk.edu.ru
            
            Return:
                UserAuthModel -> Модель авторизованного пользователя
            """
            super().__call__(username, password)
            
            await self._auto_set_cookies()
            identity: str = await self._get_random_identity()
            
            # Отправка запроса на получение токена авторизации
            auth_token_response: Response = await self.gradebook_parser.client.post(
                self.meta.urls.auth_url, 
                json=self._get_auth_json_data(username, password, identity)
            )
            # Установка токена в cookies
            self._set_auth_token(client=self.gradebook_parser.client, response=auth_token_response)
            
            # Получение данных пользователя
            auth_response: Response = await self.gradebook_parser.client.get(self.meta.urls.auth_url)
            return self._auth_model(auth_response)


    class Journal(BaseParserModel.Journal):
        
        async def list(self,
                    year: str | None = None, 
                    sem:  int | None = None,
            **kwargs) -> JournalListModel:
            """ Получение списка дисциплин
            
            Аргументы:
                year: str | None (format: "2024-2025") -> учебные года
                sem:  int | None -> Номер семестра (1 или 2)
                
                * Если 'year' или 'sem' не указаны (None), то они устаналиваются автоматически
            
            Return:
                JournalListModel -> Модель журнала со всеми предметами и информацией о них
            """
            
            if (year is None) and (sem is None):
                year, sem = self._get_auto_list_args()
            
            params = self._get_request_params(year, sem, **kwargs)
            response: Response = await self.gradebook_parser.client.get(self.meta.urls.journal_list, params=params)
            
            model: JournalListModel = self._get_journal_list_model_by_response(response)
            return model
        
        
        async def get_discipline_ids(self, *args, **kwargs) -> dict:
            """ Получение названии и id дисциплины в виде словаря (id: name) """
            journal_list: JournalListModel = await self.list(*args, **kwargs)
            
            return self._get_discipline_ids(journal_list)


        async def get(self, journal_id: int) -> JournalModel:
            """ Получение журнала по определенному предмету
            
            Аргументы:
                journal_id: int ->  ID журнала (можно получить в Journal.list())
            
            Return:
                JournalModel -> Модель журнала со всей информацикй о юзерах (оценки, пропуски)
            """
            
            response = await self.gradebook_parser.client.get(self.meta.urls.journal_by_id.format(id=journal_id))
            
            model: JournalModel = self._get_journal_model_by_response(response)
            return model
        
    
    
    