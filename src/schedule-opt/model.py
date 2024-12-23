from pydantic import BaseModel
from typing import Literal


colors: list[str] = [
    "#556B2F", # Dark Olive Green
    "#8B4513", # Saddle Brown
    "#4682B4", # Steel Blue
    "#5F9EA0", # Cadet Blue
    "#7B68EE", # Medium Slate Blue
    "#708090", # Slate Gray
    "#9ACD32", # Yellow-Green
]


class Classroom(BaseModel):
    name: str
    capacity: int
    

class TimeSlot(BaseModel):
    start: int
    end: int
    day: Literal["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi"]


class Teacher(BaseModel):
    name: str
    unavailable_slots: list[TimeSlot]
    undesired_slots: list[TimeSlot]


class Course(BaseModel):
    name: str
    teacher: Teacher
    weekly_hours: int


class AssignedTimeSlot(BaseModel):
    classroom: Classroom
    teacher: Teacher
    course: Course
    time_slot: TimeSlot
 
    
class Schedule(BaseModel):
    year_schedules: list[
        list[AssignedTimeSlot]
    ]
    