from httpx import AsyncClient, Response, Cookies

from skiplessonparser.api.base_models import BaseParserModel
from skiplessonparser.models import UserAuthModel


class AioGradebookParser(BaseParserModel):
    def __init__(self):
        super().__init__()
        
        self.client = AsyncClient()
        self.client.headers = self.meta.headers
        
    
    async def _auto_set_cookies(self) -> Cookies:
        """ Автоматически получает и устанавливает cookies в self.client """
        
        await self.client.get(self.meta.urls.main_url)
    
    
    async def _get_random_identity(self) -> str:
        response: Response = await self.client.get(self.meta.urls.get_random_identity)
        
        return super()._get_random_identity(response)

    
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
        
        super().auth(response=response, client=self.client)
        
        auth2_response: Response = await self.client.get(self.meta.urls.auth_url)
        
        model = UserAuthModel.model_validate(auth2_response.json())
        return model
        
        
    
    
    