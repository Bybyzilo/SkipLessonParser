from pydantic import BaseModel, Field
from typing import Any


class RolesModel(BaseModel):
    id: int
    name: str
    objectID: Any
    objectTable: Any
    

class UserModel(BaseModel):
    anotherID: int
    bday: bool
    currentRole: int
    eliteStatus: Any
    email: str
    existLinkedAccounts: bool
    fio: str
    first_name: str
    full_name: str = Field(validation_alias='fullName')
    group: str
    group_id: int = Field(validation_alias='groupID')
    last_name: str
    login: str
    middle_name: str
    parentID: int | str | None
    photoLink: str | None
    roles: list[RolesModel]
    shortFIO: str 
    specialityCode: Any
    status: Any
    uid_1c: str
    uid_1c_stud: str
    user_id: int = Field(validation_alias='userID')


class UserAuthData(BaseModel):
    benchmark: Any
    username: str | None = Field(validation_alias='userName')
    user: UserModel
    

class UserAuthModel(BaseModel):
    accessToken: Any
    data: UserAuthData
    expiresIn: int
    msg: str | None
    requertAt: int
    state: int