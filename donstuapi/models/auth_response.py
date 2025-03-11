from pydantic import BaseModel, Field
from typing import Any


class AuthResponseDataToDataModel(BaseModel):
    username: str = Field(validation_alias='userName')
    requertAt: str
    access_token: str = Field(validation_alias='accessToken')
    refresh_token: str = Field(validation_alias='refreshToken')
    uid_1c: str
    id: int
    recaptcha: Any = None


class AuthResponseDataModel(BaseModel):
    state: int
    msg: str | None
    data: AuthResponseDataToDataModel
    access_token: str = Field(validation_alias='accessToken')
    requertAt: int
    expiresIn: str | float


class AuthResponseModel(BaseModel):
    data: AuthResponseDataModel | str
    state: int
    msg: str | None
    time: int | float | None = None