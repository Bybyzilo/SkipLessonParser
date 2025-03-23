from __future__ import annotations
from typing import Any, List

from pydantic import BaseModel, Field


class MarkCountStatisticItem(BaseModel):
    mark: str
    count: int
    percent: float


class AvgCourseStatisticItem(BaseModel):
    course: int
    avg: float


class ZachBookItem(BaseModel):
    key: int
    course: int
    sem: int
    session: int
    dis: str
    mark: str
    hours: int
    vedID: int
    block: str
    controlForm: str
    date: str
    teacherName: str
    year: str
    markNumber: int
    zet: int
    closed: bool


class Mark(BaseModel):
    key: int
    course: int
    sem: int
    session: int
    dis: str
    mark: str
    hours: int
    vedID: int
    block: str
    controlForm: str
    date: str
    teacherName: str
    year: str
    markNumber: int
    zet: int
    closed: bool


class GroupedZachBookItem(BaseModel):
    key: str
    year: str
    session: int
    course: int
    sem: int
    controlForm: str
    marks: List[Mark]
    order: int


class StudentInfo(BaseModel):
    name: str
    group: str
    specialty: str


class RecordBookModel(BaseModel):
    showVedButton: bool
    showPrintForm: bool
    hideZET: bool
    showPersonalCard: bool
    groupID: int
    markCountStatistic: List[MarkCountStatisticItem]
    avgCourseStatistic: List[AvgCourseStatisticItem]
    zachBook: List[ZachBookItem]
    groupedZachBook: List[GroupedZachBookItem]
    studentName: str
    id: str = Field(validation_alias="recordbook")
    studentInfo: StudentInfo
    avgPoint: float
    currentSem: int
    photo: Any
    isZaoch: bool


class _(BaseModel):
    data: Any
    state: int
    msg: str
    time: int
