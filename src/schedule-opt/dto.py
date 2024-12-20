from pydantic import BaseModel

class TimeSlotDto(BaseModel):
    classroom_name: str
    course_name: str
    teacher_name: str
    start: int
    end: int
    
# we have a list for each year, and we have 3 years
class ScheduleDto(BaseModel):
    year_schedules: list[
        list[TimeSlotDto]
    ]
    query_time_ms: int
    