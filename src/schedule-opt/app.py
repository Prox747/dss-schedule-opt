from fastapi import FastAPI, Query
from dto import ScheduleDto
import time
    
app = FastAPI()

@app.get("/api/schedule", response_model=ScheduleDto)
def get_schedule():
    
    start_time: float = time.time()
    
    # TODO: find schedule

    elapsed_time: float = (time.time() - start_time) * 1000

    response = ScheduleDto(
        # year_schedules
    )

    return response

# uvicorn app:app --reload --port 13000