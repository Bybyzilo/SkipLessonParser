import json

from abc import ABC, abstractmethod
from typing import Union, TypeVar, Generic
from httpx import Response, AsyncClient, Client

from skiplessonparser.models import AuthResponseModel, JournalListModel, JournalModel


T = TypeVar("T")
class BaseParserModel(Generic[T]):
    def __init__(self):
        self.meta = self.Meta()
        self._auth_data = self.Auth(self)
        self.journal = self.Journal(self)
    
    
    class Meta:
        def __init__(self):
            self.urls = self.Urls()
            self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36"}
        
        class Urls:
            main_url: str = "https://edu.donstu.ru/"
            get_random_identity: str = "https://edu.donstu.ru/api/UserInfo/Devices/RandomIdentity"
            auth_url = "https://edu.donstu.ru/api/tokenauth"
    
    
    class Auth:
        def __init__(self, gradebook_parser: T):
            self.gradebook_parser = gradebook_parser
    
        def _get_random_identity(self, response: Response) -> str:
            parse_json = json.loads(response.text)
            
            self.gradebook_parser.meta.identity = parse_json['data']['randomIdentity']
            
            return self.gradebook_parser.meta.identity
        
        
        @staticmethod
        def _auth(response: Response, client: Client | AsyncClient):
            
            model = AuthResponseModel.model_validate(response.json())
            auth_token: str = model.data.access_token
            
            client.headers.setdefault('authorization', f'Bearer {auth_token}')
            client.cookies.setdefault('authToken', auth_token)
    
    
    class Journal(ABC):
        def __init__(self, gradebook_parser: T):
            self.gradebook_parser = gradebook_parser
        
        
        @abstractmethod
        def list(self):
            ...
        
        
        @abstractmethod
        def get(self, journal_id: int):
            ...
        
        @staticmethod
        def _get_request_params(year: str, sem: int, **kwargs):
            
            return dict(
                prepID  = kwargs.get('prepID', 'undefined'),
                groupID = kwargs.get('groupID','undefined'),
                typeJournal=1,
                year=year,
                sem=sem,
            )
            
        @staticmethod
        def _get_journal_list_model_by_response(response: Response) -> JournalListModel:
            json_data = response.json()
            return JournalListModel.model_validate(json_data)

        
        @staticmethod
        def _get_journal_model_by_response(response: Response) -> JournalModel:
            json_data = response.json()
            return JournalModel.model_validate(json_data)

        
    
    
    