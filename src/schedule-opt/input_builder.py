import json
from model import Teacher, Course, TimeSlot, AssignedTimeSlot, Schedule
from constants import DAYS, START_TIME, END_TIME, CLASSROOMS, COLORS

# Load JSON data and convert to Teacher objects
def extract_teachers(json_file_path) -> list[Teacher]:
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        
    teachers: list[Teacher] = []
    
    for teacher_name, details in data.items():
        undesired_slots = details.get("undesired_time_slots", [])
        unavailable_slots = details.get("unavailable_time_slots", [])
        undesired_slots, unavailable_slots = [
            TimeSlot(
                start=slot.split("-")[0],
                end=slot.split("-")[1]
            )
            for slot in undesired_slots
        ],[
            TimeSlot(
                start=slot.split("-")[0],
                end=slot.split("-")[1]
            )
            for slot in unavailable_slots
        ]
        
        teachers.append(
            Teacher(
                name=teacher_name,
                undesired_slots=undesired_slots,
                unavailable_slots=unavailable_slots
        ))
    
    return teachers


def extract_courses(json_file_path: str, teachers: list[Teacher]) -> list[Course]:
    courses: list[Course] = []
    
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        
    for course_name, details in data.items():
        teacher_name = details.get("teacher", "")
        
        courses.append(Course(
            name=course_name,
            teacher= next((teacher for teacher in teachers if teacher.name == teacher_name)),
            weekly_hours=details.get("weekly_hours", 0),
            year=details.get("year", 0)
        ))
    
    return courses


# Function to create the years_schedule
def build_first_schedule(year1_courses: list[Course],
                         year2_courses: list[Course],
                         year3_courses: list[Course],) -> Schedule:
    courses_by_year = [year1_courses, year2_courses, year3_courses]
    schedule = Schedule(
        year_schedules=[]
    )
    
    # for each year
    for i in range(0, 3):
        year_schedule: list[AssignedTimeSlot] = []
        current_day = 0
        current_time = START_TIME
        color_index = 0
    
        for course in courses_by_year[i]:
            hours_remaining = course.weekly_hours
            
            while hours_remaining > 0:
                slot_end = current_time + 2  # Each slot is 2 hours
                
                if slot_end > END_TIME:  # If we exceed the day's end, move to the next day
                    current_day = (current_day + 1) % len(DAYS)
                    current_time = START_TIME
                    continue

                # Assign the time slot
                time_slot = TimeSlot(
                    start=current_time,
                    end=slot_end,
                    day=DAYS[current_day]
                )
                year_schedule.append(AssignedTimeSlot(
                    classroom=CLASSROOMS[i],
                    course=course,
                    time_slot=time_slot,
                    color_hex=COLORS[color_index]
                ))

                # Update counters
                hours_remaining -= 2
                current_time = slot_end

                if current_time >= END_TIME:  # If we hit the end of the day, move to the next day
                    current_day = (current_day + 1) % len(DAYS)
                    current_time = START_TIME
                    
            color_index = (color_index + 1) % len(COLORS)
        
        schedule.year_schedules.append(year_schedule)

    return schedule