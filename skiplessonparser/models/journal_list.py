from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class RaspDayIDItem(BaseModel):
    dayID: int
    timeZanID: int
    weekID: int
    timeStart: str
    timeEnd: str
    aud: str


class ReturnListItem(BaseModel):
    id: int
    groupName: str
    dis: str
    type: str
    year: str
    sessionOrSem: int
    dateCount: int
    closedDatesCount: int
    isThereCurDate: bool
    lastDate: str
    maxDateCount: int
    strDates: str
    prepodName: str
    photo: Optional[str]
    raspDayID: List[RaspDayIDItem]
    timeZanID: int
    passes: int
    formID: int


class TimeZan(BaseModel):
    timeZanID: int
    numZan: str
    beginZan: str
    endZan: str
    dayNed: Any
    beginHour: int
    beginMinutes: int
    endHour: int
    endMinutes: int


class RaspItem(BaseModel):
    id: int
    semID: int
    groupID: int
    dayNedID: int
    timeZanID: int
    subGroupNumber: int
    typeNed: int
    dis: str
    prepod: str
    aud: str
    link: str
    year: str
    date: str
    dateChange: str
    kafedraID: int
    weekStart: int
    weekEnd: int
    timeFrom: str
    timeTo: str
    theme: str
    teacherID: int
    typeID: int
    disciplineModuleID: Any
    disciplineModule: Any
    dispLogin: str
    dispDomain: str
    fileName: str
    hide: bool
    audSchoolX_ID: int
    replacedTeacherID: int
    color: str
    loadRowID: int
    paymentIgnore: bool
    audSchoolX_: Any
    isReplace: bool
    course: Any
    isCyclicalItem: bool
    educationSpaceID: Any
    isGraph: bool
    building: str
    dateStart: str
    dateEnd: str
    duration: int
    intTimeFromHour: int
    intTimeFromMinute: int
    intTimeToHour: int
    intTimeToMinute: int
    raspGroupName: Any
    endTime: str
    groupName: Any
    groupsIDs: List
    teachersIDs: Any
    raspItemsIDs: Any
    webinarID: Any
    curGroup: Any
    curKaf: Any
    dayNed: Any
    timeZan: TimeZan
    journalName: str


class FormingInfo(BaseModel):
    errors: List
    existNewJournal: bool
    newJournalsCount: int
    baseFilteredWorkloadCount: int
    semFilteredWorkloadCount: int
    groupsFilteredWorkloadCount: int
    existJournalsCount: int


class Data(BaseModel):
    semsNumberEnabled: bool
    currentSessions: List
    sems: List[int]
    maxSems: int
    isGroupLeader: bool
    fillingProcent: int
    returnList: List[ReturnListItem]
    yearsList: List[str]
    unformedJournal: List
    rasp: List[RaspItem]
    existInstructionTeacher: bool
    showBindingError: bool
    errorsSaveJ: List
    formingInfo: FormingInfo
    nagr: Any


class JournalListModel(BaseModel):
    data: Data
    state: int
    msg: str
    time: int
