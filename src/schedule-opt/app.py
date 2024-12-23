from fastapi import FastAPI, Query
from dto import ScheduleDto, TimeSlotDto
from model import Schedule, TimeSlot
from local_search import find_schedule
import time
    

def create_dto(schedule: Schedule, elapsed_time_ms: float) -> ScheduleDto:
    schedule_dto = ScheduleDto(
        year_schedules=[],
        query_time_ms=elapsed_time_ms
    )
    
    for year_schedule in schedule.year_schedules:
        year_schedule_dto: list[TimeSlotDto] = []
        
        for slot in year_schedule:
            year_schedule_dto.append(TimeSlotDto(
                classroom_name=slot.classroom,
                course_name=slot.course.name,
                teacher_name=slot.course.teacher.name,
                start=slot.time_slot.start,
                end=slot.time_slot.end,
                day=slot.time_slot.day,
                color_hex=slot.color_hex
            ))
        
        schedule_dto.year_schedules.append(year_schedule_dto)
    
    return schedule_dto
    
    
app = FastAPI()

@app.get("/api/schedule", response_model=ScheduleDto)
def get_schedule():
    
    start_time: float = time.time()
    
    # TODO: find schedule
    schedule: Schedule = find_schedule()

    elapsed_time: float = (time.time() - start_time) * 1000

    response = create_dto(schedule, elapsed_time)

    return response

# uvicorn app:app --reload --port 13000