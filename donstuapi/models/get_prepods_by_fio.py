from __future__ import annotations

from typing import List

from pydantic import BaseModel


class ArrPrepItem(BaseModel):
    id: int
    userID: int
    teacherID: int | None
    fio: str
    fioEng: str
    photoLinkID: str | None
    email: str | None


class Data(BaseModel):
    arrPrep: List[ArrPrepItem]


class GetPrepodsByFIO(BaseModel):
    data: Data
    state: int
    msg: str
    time: float
