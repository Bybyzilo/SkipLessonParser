from __future__ import annotations
from typing import List

from pydantic import BaseModel


class MarkCountStatisticItem(BaseModel):
    mark: int
    markName: str
    count: int
    avg: float


class Data(BaseModel):
    markCountStatistic: List[MarkCountStatisticItem]
    count: int


class StatisticsMarksCountModel(BaseModel):
    data: Data
    state: int
    msg: str
    time: int
