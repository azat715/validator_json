"""
sleep_created.schema
"""

from typing import List, Optional
from pydantic import BaseModel


class InfoItem(BaseModel):
    type_: str
    value: float

    class Config:
        fields = {"type_": "type"}


class Point(BaseModel):
    x_date: str
    y_value: float


class PhasesInfoItem(BaseModel):
    type_: str
    percent: float
    duration: float

    class Config:
        fields = {"type_": "type"}


class TypeRangeSleepCreated(BaseModel):
    date: str
    type_: str

    class Config:
        fields = {"type_": "type"}


class SleepCreated(BaseModel):
    """
    базовая модель sleep_created.schema
    """

    info: Optional[List[InfoItem]] = None
    points: Optional[List[Point]] = None
    source: str
    timestamp: str
    unique_id: str
    time_start: str
    finish_time: str
    phases_info: Optional[List[PhasesInfoItem]] = None
    type_ranges: Optional[List[TypeRangeSleepCreated]] = None
    activity_type: str
