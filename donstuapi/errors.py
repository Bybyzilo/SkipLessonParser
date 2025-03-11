

class EmptyAuthDataError(BaseException):
    def __init__(self, message: str | None = None):
        if message is None:
            message = "Укажите данные авторизации"
            
        super().__init__(message)



class AuthError(BaseException): ...
    