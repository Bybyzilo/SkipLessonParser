from httpx import AsyncClient, Response, Cookies

from skiplessonparser.api.base_models import BaseParserModel
from skiplessonparser.models import UserAuthModel, JournalListModel, JournalModel


class AioGradebookParser(BaseParserModel["AioGradebookParser"]):
    def __init__(self):
        super().__init__()
        
        self.client = AsyncClient()
        self.client.headers = self.meta.headers
        
    
    class Auth(BaseParserModel.Auth):
        async def _auto_set_cookies(self) -> Cookies:
            """ Автоматически получает и устанавливает cookies в self.client """
            
            await self.gradebook_parser.client.get(self.meta.urls.main_url)
        
        
        async def _get_random_identity(self) -> str:
            response: Response = await self.gradebook_parser.client.get(self.meta.urls.get_random_identity)
            
            return super()._get_random_identity(response)

        
        async def __call__(self, username: str, password: str) -> UserAuthModel:
            """ Auth user """
            
            await self._auto_set_cookies()
            identity: str = await self._get_random_identity()
            
            json_data = {
                'userName': username,
                'password': password,
                'isParent': False,
                'fingerprint': identity,
                'recaptchaToken': None,
                'redirect': False,
            }
            
            response: Response = await self.gradebook_parser.client.post(self.meta.urls.auth_url, json=json_data)
            
            self._auth(response=response, client=self.gradebook_parser.client)
            
            auth2_response: Response = await self.gradebook_parser.client.get(self.meta.urls.auth_url)
            
            model = UserAuthModel.model_validate(auth2_response.json())
            return model


    class Journal(BaseParserModel.Journal):
        
        async def list(self,
                    year: str | None = None, 
                    sem:  int | None = None,
            **kwargs) -> JournalListModel:
            """ Получение списка предметов
            
            Аргументы:
                year: str (format: "2024-2025") -> учебные года
                sem: int -> Номер семестра (1 или 2)
            
            Return:
                JournalListModel -> Модель журнала со всеми предметами и информаци о них
            """
            
            if (year is None) and (sem is None):
                year, sem = self._get_auto_list_args()
            
            params = self._get_request_params(year, sem, **kwargs)
            response: Response = await self.gradebook_parser.client.get("https://edu.donstu.ru/api/Journals/JournalList", params=params)
            
            model: JournalListModel = self._get_journal_list_model_by_response(response)
            return model
        
        
        async def get_discipline_ids(self, *args, **kwargs):
            journal_list: JournalListModel = await self.list(*args, **kwargs)
            
            return self._get_discipline_ids(journal_list)


        async def get(self, journal_id: int) -> JournalModel:
            """ Получение журнала по определенному предмету
            
            Аргументы:
                journal_id: int ->  ID журнала (можно получить в Journal.list())
            
            Return:
                JournalModel -> Модель журнала со всей информацикй о юзерах (оценки, пропуски)
            """
            
            response = await self.gradebook_parser.client.get("https://edu.donstu.ru/api/Journals/Journal?journalID=%d" % journal_id)
            
            model: JournalModel = self._get_journal_model_by_response(response)
            return model
        
    
    
    