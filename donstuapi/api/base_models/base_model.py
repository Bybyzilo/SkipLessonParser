# type: ignore
from datetime import datetime

from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from httpx import Response, AsyncClient, Client

from donstuapi.models import (
    journal_list_models, JournalListModel, 
    UserAuthModel, AuthResponseModel,
    AccountInfoModel, GetStudentsByFIO,
    GetPrepodsByFIO
)
from donstuapi import errors
from donstuapi.models.record_book_model import RecordBookModel


T = TypeVar("T")
class BaseParserModel(Generic[T]):
    def __init__(self):
        self.meta = self.Meta()
        self.auth = self.Auth(self)
        self.account = self.Account(self)
        self.journal = self.Journal(self)
        self.recordbook = self.RecordBook(self)
        self.tools = self.Tools(self)
    
    
    class Meta:
        def __init__(self):
            self.urls = self.Urls()
            self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36"}
        
        class Urls:
            main_url = "https://edu.donstu.ru/"
            get_random_identity = "https://edu.donstu.ru/api/UserInfo/Devices/RandomIdentity"
            auth_url = "https://edu.donstu.ru/api/tokenauth"
            
            journal_list = "https://edu.donstu.ru/api/Journals/JournalList"
            journal_by_id = "https://edu.donstu.ru/api/Journals/Journal?journalID={id}"
            
            student_account = "https://edu.donstu.ru/api/UserInfo/Student?studentID={id}"
            feed = "https://edu.donstu.ru/api/Feed?userID={id}"
            payment = "https://edu.donstu.ru/api/UserInfo/Student/Payment"
            statistics_marks_count = "https://edu.donstu.ru/api/EducationalActivity/StatisticsMarksCount?studentID={id}"
            
            record_book = "https://edu.donstu.ru/api/EducationalActivity/ZachBook?studentID=undefined"
            
            get_students_by_fio = "https://edu.donstu.ru/api/Mail/Find/Students?fio={fio}&kafID=0"
            get_prepods_by_fio = "https://edu.donstu.ru/api/Mail/Find/Prepods?fio={fio}"
            
            avg_mark = "https://edu.donstu.ru/api/EducationalActivity/StudentAvgMark?studentID={id}"
            statistics_marks_count = "https://edu.donstu.ru/api/EducationalActivity/StatisticsMarksCount?studentID={id}"
            group_students = "https://edu.donstu.ru/api/Mail/Find/Students?kafID=0&groupID={group_id}"
    
    class Auth(ABC):
        def __init__(self, donstu: T):
            self.donstu = donstu
            self.meta = self.donstu.meta
        
        
        @staticmethod
        def _get_auth_json_data(username: str, password: str, identity):
            return {
                'userName': username,
                'password': password,
                'isParent': False,
                'fingerprint': identity,
                'recaptchaToken': None,
                'redirect': False,
            }
            

        def _get_random_identity(self, response: Response) -> str:
            parse_json = response.json()
            self.donstu.meta.identity = parse_json['data']['randomIdentity']
            
            return self.donstu.meta.identity

        
        @abstractmethod
        def _auto_set_cookies(self):
            ...
        
        
        def __call__(self, username: str, password: str):
            """ Авторизация """
            
            if not (username and password):
                raise errors.EmptyAuthDataError

    
    
        @staticmethod
        def _set_auth_token(client: Client | AsyncClient, response: Response) -> None:
            model = AuthResponseModel.model_validate(response.json())
            if isinstance(model.data, str):
                raise errors.AuthError(model.msg)
            
            auth_token: str = model.data.access_token
            
            client.headers.setdefault('authorization', f'Bearer {auth_token}')
            client.cookies.setdefault('authToken', auth_token)
        
        
        def _auth_model_init(self, response: Response) -> UserAuthModel:
            model = UserAuthModel.model_validate(response.json())
            
            self._auth_model = model
            self.donstu.account.user_id = model.data.user.user_id
            
            return model
    
    
    class Account(ABC):
        def __init__(self, donstu: T):
            self.donstu = donstu
            self.user_id = 0
            
            self._info: AccountInfoModel | None = None
        
        
        def get_important_message(self) -> str | None:
            """ Получение важных сообщений со страницы профиля """

            if self._info is not None:
                return self._info.data.message
            else:
                cls = type(self.donstu).__name__
                print(
                    f"WARNING! To call the '{cls}.account.get_important_message()' "
                    f"method, first get the profile information ('{cls}.account.info')"
                )
                return None
        
        @abstractmethod
        def info(self): ...
        
        @abstractmethod
        def feed(self): ...
        
        @abstractmethod
        def payments(self): ...
        
        @abstractmethod
        def statistics_marks_count(): ...
        
        @staticmethod
        def _get_info_model(response: Response) -> AccountInfoModel:
            model = AccountInfoModel.model_validate(response.json())
            
            return model
        
    
    class Journal(ABC):
        def __init__(self, donstu: T):
            self.donstu = donstu
            self.meta = self.donstu.meta
        
        
        @abstractmethod
        def list(self):
            ...
        
        
        @abstractmethod
        def get(self, journal_id: int):
            ...
        
        
        @staticmethod
        def _get_auto_list_args() -> tuple[str, int]:
            now = datetime.now()
            if now.month > 9:
                sem = 1
                year = "%d-%d" % (now.year, now.year)
            else:
                sem = 2
                year = '%d-%d' % (now.year-1, now.year)
            
            return (year, sem)
            
        
        
        @staticmethod
        def _get_discipline_ids(model: JournalListModel) -> dict[int, str]:
            return_list: journal_list_models.ReturnListItem = model.data.returnList
            
            items = {}
            for item in return_list:
                items[item.id] = item.dis
            
            return items
        
        
        @staticmethod
        def _get_request_params(year: str, sem: int, **kwargs):
            
            return dict(
                prepID  = kwargs.get('prepID', 'undefined'),
                groupID = kwargs.get('groupID','undefined'),
                typeJournal=1,
                year=year,
                sem=sem,
            )
    
    
    class RecordBook(ABC):
        def __init__(self, donstu: T):
            self.donstu = donstu
            self.recordbook_id: int = 0
        
        def _init_info(self, response: Response) -> RecordBookModel:
            """ Docs """
            
            model = RecordBookModel.model_validate(response.json()['data'])
            self.recordbook_id = int(model.id)
            
            return model
    
    class Tools(ABC):
        def __init__(self, donstu: T) :
            self.donstu = donstu
        
        @abstractmethod
        async def get_students_by_fio(self, fio: str) -> GetStudentsByFIO:
            ...
        
        @abstractmethod
        async def get_prepods_by_fio(self, fio: str) -> GetPrepodsByFIO:
            ...
        
        def _init_students_data(self, response: Response) -> GetStudentsByFIO:
            model = GetStudentsByFIO.model_validate(response.json())
            return model
            
        
        def _init_prepods_data(self, response: Response) -> GetPrepodsByFIO:
            model = GetPrepodsByFIO.model_validate(response.json())
            return model


        
    
    
    