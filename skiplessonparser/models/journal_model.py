from __future__ import annotations

from typing import Any, List, Dict, Optional

from pydantic import BaseModel, Field


class JournalValItem(BaseModel):
    id: int
    value: str
    numberValue: Optional[int]
    isMark: bool
    isPass: bool
    isValidPass: bool


# class JournalDatum(BaseModel):
#     field_1690495: str = Field(..., alias='1690495')
#     field_1690496: str = Field(..., alias='1690496')
#     field_1719679: str = Field(..., alias='1719679')
#     field_1719680: str = Field(..., alias='1719680')
#     field_1786126: str = Field(..., alias='1786126')
#     field_1786127: str = Field(..., alias='1786127')
#     field_1803472: str = Field(..., alias='1803472')
#     field_1803473: str = Field(..., alias='1803473')
#     id: str
#     fio: str
#     fullName: str
#     avgMark: Any
#     sumMarks: Any
#     number: int
#     status: str


class Hours(BaseModel):
    hourInJournal: int
    hourInJournalReal: int
    hourInNagr: int


class JournalLegendItem(BaseModel):
    value: str
    description: Optional[str]


class EdgeDates(BaseModel):
    dateMin: str
    dateMax: str


class JournalInfo(BaseModel):
    dis: str
    type: str
    hours: Hours
    teacherName: str
    teacherUserID: int
    year: str
    pointsSystem: Any
    groupName: str
    groupID: int
    educationForm: str
    course: int
    sem: int
    session: Any
    planName: str
    educationLevel: str
    journalLegend: List[JournalLegendItem]
    edgeDates: EdgeDates
    showSettings: bool
    daysLimit: int


class JournalDate(BaseModel):
    dateID: int
    date: str
    hourNumber: int
    confirmedTeacher: bool


class Data(BaseModel):
    isSubGroup: bool
    notFilledSubGroups: bool
    nullValueID: int
    passValueID: int
    journalID: int
    qrCodes: List
    defaultHours: int
    journalVal: List[JournalValItem]
    journalData: Any#Dict # List[JournalDatum]
    journalInfo: JournalInfo
    allowEdit: bool
    allowRPDEdit: bool
    provisionalDate: Any
    journalDates: List[JournalDate]
    lastValueDate: str
    lastUser: Any
    availableValues: List
    nonworkingHolidayDays: List[str]
    syncRasp: bool
    qrTestEnabled: bool
    allowCreateWebinars: bool
    showMarksTab: bool
    hideSumMarks: bool


class JournalModel(BaseModel):
    data: Data
    state: int
    msg: str
    time: int
