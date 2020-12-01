"""
label_selected.schema
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class Labels(BaseModel):
    slug: str
    type_: int
    color: Optional[Dict[str, Any]]
    name_en: str
    name_ru: str
    category: Optional[str]
    type_stress: int
    is_custom_tag: bool
    property_where: Optional[str]
    property_arousal: Optional[str]
    property_pleasure: Optional[str]
    property_vitality: Optional[str]
    property_stability: Optional[str]

    class Config:
        fields = {"type_": "type"}


class User(BaseModel):
    id: int


class LabelSelected(BaseModel):
    """
    базовая модель label_selected.schema
    """

    id: Optional[int]
    user: User
    rr_id: Optional[int]
    labels: List[Labels]
    user_id: int
    timestamp: str
    unique_id: str
