import json
from typing import Union
from httpx import Response, AsyncClient, Client

from skiplessonparser.models import AuthResponseModel


class BaseParserModel:
    
    def __init__(self):
        self.meta = self.Meta()
    
    
    class Meta:
        def __init__(self):
            self.urls = self.Urls()
            self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36"}
        
        class Urls:
            main_url: str = "https://edu.donstu.ru/"
            get_random_identity: str = "https://edu.donstu.ru/api/UserInfo/Devices/RandomIdentity"
            auth_url = "https://edu.donstu.ru/api/tokenauth"
    
    
    def _get_random_identity(self, response: Response) -> str:
        parse_json = json.loads(response.text)
        
        self.meta.identity = parse_json['data']['randomIdentity']
        
        return self.meta.identity
    
    
    def auth(self, response: Response, client: Client | AsyncClient):
        
        model = AuthResponseModel.model_validate(response.json())
        auth_token: str = model.data.access_token
        
        client.headers.setdefault('authorization', f'Bearer {auth_token}')
        client.cookies.setdefault('authToken', auth_token)
    
    
    