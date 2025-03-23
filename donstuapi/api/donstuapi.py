from httpx import Client, Response

from donstuapi.api.base_models import BaseParserModel
from donstuapi.models import (
    UserAuthModel, JournalListModel, JournalModel, 
    AccountInfoModel, FeedModel, PaymentModel,
    StatisticsMarksCountModel, RecordBookModel
)


class DonstuAPI(BaseParserModel["DonstuAPI"]):
    def __init__(self):
        super().__init__()
        
        self.client = Client()
        self.client.headers = self.meta.headers
        
    
    class Auth(BaseParserModel.Auth):
        def _auto_set_cookies(self) -> None:
            """ Автоматически получает и устанавливает cookies в self.client """
            
            self.donstu.client.get(self.meta.urls.main_url)
        
        
        def _get_random_identity(self) -> str:
            response: Response = self.donstu.client.get(self.meta.urls.get_random_identity)
            
            return super()._get_random_identity(response)

        
        def __call__(self, username: str, password: str) -> UserAuthModel:
            """ Авторизация пользователя и получение токена
            
            Аргументы:
                username, password (str) -> данные для авторизации на lk.edu.ru
            
            Return:
                UserAuthModel -> Модель авторизованного пользователя
            """
            super().__call__(username, password)
            
            self._auto_set_cookies()
            identity: str = self._get_random_identity()
            
            # Отправка запроса на получение токена авторизации
            auth_token_response: Response = self.donstu.client.post(
                self.meta.urls.auth_url, 
                json=self._get_auth_json_data(username, password, identity)
            )
            # Установка токена в cookies
            self._set_auth_token(client=self.donstu.client, response=auth_token_response)
            
            # Получение данных пользователя
            auth_response: Response = self.donstu.client.get(self.meta.urls.auth_url)
            return self._auth_model_init(auth_response)
    
    
    class Account(BaseParserModel.Account):

        @property
        def info(self) -> AccountInfoModel:
            if self._info is None:
                url: str = self.donstu.meta.urls.student_account.format(id=self.user_id)
                response: Response = self.donstu.client.get(url)
                
                self._info: AccountInfoModel = self._get_info_model(response)
                
            return self._info
        
        
        def feed(self) -> FeedModel:
            """ Получение уведомлений и прочей информации """
            
            url: str = self.donstu.meta.urls.feed.format(id=self.user_id)
            response: Response = self.donstu.client.get(url)
            
            return FeedModel.model_validate(response.json())
        
        
        def payments(self) -> PaymentModel:
            """ Получение информации об оплате """
            
            url: str = self.donstu.meta.urls.payment
            response = self.donstu.client.get(url)
            
            return PaymentModel.model_validate(response.json())
        
        
        def statistics_marks_count(self) -> StatisticsMarksCountModel:
            """ Получение статистики оценок """
            
            url = self.donstu.meta.urls.statistics_marks_count.format(id=self.user_id)
            response = self.donstu.client.get(url)
            
            return StatisticsMarksCountModel.model_validate(response.json())
            

    class Journal(BaseParserModel.Journal):
        
        def list(self,
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
            response: Response = self.donstu.client.get(self.meta.urls.journal_list, params=params)
            
            return JournalListModel.model_validate(response.json())
        
        
        def get_discipline_ids(self, *args, **kwargs) -> dict:
            """ Получение названии и id дисциплины в виде словаря (id: name) """
            journal_list: JournalListModel = self.list(*args, **kwargs)
            
            return self._get_discipline_ids(journal_list)


        def get(self, journal_id: int) -> JournalModel:
            """ Получение журнала по определенному предмету
            
            Аргументы:
                journal_id: int ->  ID журнала (можно получить в Journal.list())
            
            Return:
                JournalModel -> Модель журнала со всей информацикй о юзерах (оценки, пропуски)
            """
            
            url = self.meta.urls.journal_by_id.format(id=journal_id)
            response = self.donstu.client.get(url)
            
            return JournalModel.model_validate(response.json())
        
    
    class RecordBook(BaseParserModel.RecordBook):
        
        def info(self) -> RecordBookModel:
            """ Получение информации о зачетной книжке """
            
            url = self.donstu.meta.urls.record_book
            response = self.donstu.client.get(url)
        
            return super()._init_info(response)
            
            
    
    
    