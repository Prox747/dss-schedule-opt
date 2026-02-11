from pydantic import BaseModel
from typing import Literal

class TimeSlotDto(BaseModel):
    classroom_name: str
    course_name: str
    teacher_name: str
    start: int
    end: int
    day: Literal["lunedi", "martedi", "mercoledi", "giovedi", "venerdi"]
    color_hex: str
    
# we have a list for each year, and we have 3 years
class ScheduleDto(BaseModel):
    year_schedules: list[
        list[TimeSlotDto]
    ]
    init_fitness: int
    best_fitness: int
    query_time_ms: float
    