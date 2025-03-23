from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class FeedItem(BaseModel):
    notificationID: int
    userID: int
    objectID: int
    text: Optional[str]
    html: Optional[str]
    fullDate: str
    category: str
    link: Optional[str]
    linkText: Optional[str]
    isNew: bool
    date: str
    time: str
    questionaryID: Any
    published: bool
    forStudents: bool
    forTeachers: bool
    views: Any
    color: str


class Data(BaseModel):
    time: float
    feed: List[FeedItem]
    categories: List[str]
    showMore: bool
    benchmark: Any


class FeedModel(BaseModel):
    data: Data
    state: int
    msg: str
    time: int