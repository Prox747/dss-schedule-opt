from pydantic import BaseModel
from typing import Literal, Optional


class TimeSlot(BaseModel):
    start: int
    end: int
    day: Optional[Literal["lunedi", "martedi", "mercoledi", "giovedi", "venerdi"]] = None
    

class Teacher(BaseModel):
    name: str
    unavailable_slots: list[TimeSlot]
    undesired_slots: list[TimeSlot]
    
    def get_total_unavailable_hours(self) -> int:
        hours_total = 0
        for time_slot in self.unavailable_slots:
            hours_total += (time_slot.end - time_slot.start)
            
        return hours_total
        
Level = Literal[1, 2, 3, 4, 5, 6, 7]

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
    