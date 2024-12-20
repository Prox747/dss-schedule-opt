from pydantic import BaseModel

class Classroom(BaseModel):
    name: str
    capacity: int
    

class TimeSlot(BaseModel):
    start: int
    end: int


class Teacher(BaseModel):
    name: str
    unavailable_slots: list[TimeSlot]
    undesired_slots: list[TimeSlot]


class Course(BaseModel):
    name: str
    teacher: Teacher


class AssignedTimeSlot(BaseModel):
    classroom: Classroom
    teacher: Teacher
    course: Course
    time_slot: TimeSlot
 
    
class Schedule(BaseModel):
    year_schedules: list[
        list[AssignedTimeSlot]
    ]
    