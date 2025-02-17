from fastapi import FastAPI, Query
from typing import Optional
from dto import ScheduleDto, TimeSlotDto
from model import Schedule, TimeSlot
from local_search import find_schedule
from constants import MAX_ITER, MAX_ITER_NO_IMPROVEMENT
import time
    

def create_dto(schedule: Schedule, elapsed_time_ms: float, init_fitness: int, best_fitness: int) -> ScheduleDto:
    schedule_dto = ScheduleDto(
        year_schedules=[],
        init_fitness=init_fitness,
        best_fitness=best_fitness,
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
def get_schedule(
    max_iter: Optional[str] = Query(None, description="Max iterations"),
    max_iter_no_improv: Optional[str] = Query(None, description="Max iterations since last improvement")
):
    start_time: float = time.time()
    
    print(max_iter)
    max_iter = int(max_iter) if max_iter != None else MAX_ITER
    max_iter_no_improv = int(max_iter_no_improv) if max_iter_no_improv != None else MAX_ITER_NO_IMPROVEMENT
    
    # TODO: find schedule
    schedule, init_fitness, best_fitness = find_schedule(max_iter, max_iter_no_improv)

    elapsed_time: float = (time.time() - start_time) * 1000

    response = create_dto(schedule, elapsed_time, init_fitness, best_fitness)

    return response

# uvicorn app:app --reload --port 13000