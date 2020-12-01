"""
cmarker_created.schema
"""
from typing import List
from pydantic import BaseModel


class Cmarkers(BaseModel):
    id: int
    date: str
    slug: str


class CmarkerCreated(BaseModel):
    """
    базовая модель cmarker_created.schema
    """

    user_id: int
    cmarkers: List[Cmarkers]
    datetime: str
