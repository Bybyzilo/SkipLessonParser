from pydantic import BaseModel
from typing import Any


class StudentsListData(BaseModel):
    arrStud: list["ArrStud"]

class ArrStud(BaseModel):
    id: int
    userID: int
    fio: str
    fioEng: str
    groupID: int
    groupName: str
    photoLinkID: str
    zachBook: str | None
    birthday: Any

class GetStudentsByFIO(BaseModel):
    data: StudentsListData
    state: int
    msg: str
    time: float
    
    def __await__(self):
        ...