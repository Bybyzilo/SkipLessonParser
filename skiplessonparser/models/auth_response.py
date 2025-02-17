from pydantic import BaseModel, Field
from typing import Any, Optional


class AuthResponseDataToDataModel(BaseModel):
    username: str = Field(validation_alias='userName')
    requertAt: str
    access_token: str = Field(validation_alias='accessToken')
    refresh_token: str = Field(validation_alias='refreshToken')
    uid_1c: str
    id: int
    recaptcha: Any


class AuthResponseDataModel(BaseModel):
    state: int
    msg: Optional[str]
    data: AuthResponseDataToDataModel
    access_token: str = Field(validation_alias='accessToken')
    requertAt: int
    expiresIn: str | float


class AuthResponseModel(BaseModel):
    data: AuthResponseDataModel
    state: int
    msg: Optional[str]
    time: int | float