"""
workout_created.schema
"""

from typing import Optional
from pydantic import BaseModel


class TypeRangesWorkoutCreated(BaseModel):
    cardio: int
    fat_burn: int
    hardcore: int
    warm_up: int


class WorkoutCreated(BaseModel):
    """
    базовая модель workout_created.schema
    """

    activity_name: str
    activity_type: str
    source: str
    time_end: str
    time_start: str
    timestamp: str
    unique_id: str
    met: int = None
    pulse: int = None
    steps: int = None
    calories: int = None
    distance: int = None
    duration: int = None
    pace_avg: int = None
    pulse_max: Optional[int] = None
    pulse_min: Optional[int] = None
    speed_avg: int = None
    resting_hr: int = None
    type_ranges: TypeRangesWorkoutCreated = None
    exercise_time: int = None
    calories_basal: int = None
    calories_active: int = None
    steps_speed_avg: int = None
    steps_speed_max: int = None
