from pydantic import BaseModel
from typing import Literal, Optional


class TimeSlot(BaseModel):
    start: int
    end: int
    day: Optional[Literal["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi"]] = None
    

class Teacher(BaseModel):
    name: str
    unavailable_slots: list[TimeSlot]
    undesired_slots: list[TimeSlot]


class Course(BaseModel):
    name: str
    teacher: Teacher
    weekly_hours: int
    year: int


class AssignedTimeSlot(BaseModel):
    classroom: str
    course: Course
    time_slot: TimeSlot
    color_hex: str
 
    
class Schedule(BaseModel):
    year_schedules: list[
        list[AssignedTimeSlot]
    ]
    