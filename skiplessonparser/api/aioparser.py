from httpx import AsyncClient, Response, Cookies

from skiplessonparser.api.base_models import BaseParserModel
from skiplessonparser.models import UserAuthModel, JournalListModel, JournalModel


class AioGradebookParser(BaseParserModel["AioGradebookParser"]):
    def __init__(self):
        super().__init__()
        
        self.client = AsyncClient()
        self.client.headers = self.meta.headers
        
    
    async def _auto_set_cookies(self) -> Cookies:
        """ Автоматически получает и устанавливает cookies в self.client """
        
        await self.client.get(self.meta.urls.main_url)
    
    
    async def _get_random_identity(self) -> str:
        response: Response = await self.client.get(self.meta.urls.get_random_identity)
        
        return self._auth_data._get_random_identity(response)

    
    async def auth(self, username: str, password: str) -> UserAuthModel:
        """  """
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
        
        response: Response = await self.client.post(self.meta.urls.auth_url, json=json_data)
        
        self._auth_data._auth(response=response, client=self.client)
        
        auth2_response: Response = await self.client.get(self.meta.urls.auth_url)
        
        model = UserAuthModel.model_validate(auth2_response.json())
        return model


    class Journal(BaseParserModel.Journal):
        async def list(self, year: str, sem: int, **kwargs) -> JournalListModel:
            """ Получение списка предметов
            
            Аргументы:
                year: str (format: "2024-2025") -> учебные года
                sem: int -> Номер семестра (1 или 2)
            
            Return:
                JournalListModel -> Модель журнала со всеми предметами и информаци о них
            """
            
            params = self._get_request_params(year, sem, **kwargs)
            response: Response = await self.gradebook_parser.client.get("https://edu.donstu.ru/api/Journals/JournalList", params=params)
            
            model: JournalListModel = self._get_journal_list_model_by_response(response)
            return model


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
        
    
    
    