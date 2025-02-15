import json, random
from model import Teacher, Course, TimeSlot, AssignedTimeSlot, Schedule
from constants import DAYS, START_TIME, END_TIME, CLASSROOMS, COLORS, MAX_DAILY_HOURS
from ansi_colors import *

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
                end=slot.split("-")[1],
                day=slot.split("-")[2] if slot.split("-")[2] else None
            )
            for slot in undesired_slots
        ],[
            TimeSlot(
                start=slot.split("-")[0],
                end=slot.split("-")[1],
                day=slot.split("-")[2] if slot.split("-")[2] else None
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

# hell function to build first schedule without using unavailable slots
def build_first_schedule(year1_courses: list[Course],
                         year2_courses: list[Course],
                         year3_courses: list[Course],
                         use_heuristic: bool = False) -> Schedule:
    courses_by_year = [year1_courses, year2_courses, year3_courses]

    for attempt in range(3): # Retry logic for randomized course orders
        schedule = Schedule(
            year_schedules=[]
        )
        
        # we order the courses of each year in non increasing order of number
        # of unavailable slots expressed by the teacher's course
        if use_heuristic:
            for year_courses in courses_by_year:
                year_courses.sort(key=lambda course: course.teacher.get_total_unavailable_hours(), reverse=True)
        
            print(f"{RED}ORDERED COURSES BASED ON HEURISTIC{RESET}")
            print(courses_by_year)
        
        try:
            # For each year
            for i in range(0, 3):
                year_schedule: list[AssignedTimeSlot] = []
                color_index: int = -1 # it will be zero the first time

                # we need to keep track of how many hours a day we have left for each year schedule
                # For the third year we allow two more hours per day since not all courses are mandatory
                hours_left_per_day: dict[str, int] = {}
                for day in DAYS:
                    hours_left_per_day[day] = MAX_DAILY_HOURS if i != 2 else MAX_DAILY_HOURS + 2

                for course in courses_by_year[i]:
                    hours_remaining = course.weekly_hours
                    color_index = (color_index + 1) % len(COLORS)
            
                    valid_slot_found = False

                    for day in DAYS:
                        if hours_remaining <= 0:
                            break
                        for current_time in range(START_TIME, END_TIME, 2):
                            slot_end = current_time + 2
                            
                            if slot_end > END_TIME or (hours_left_per_day[day] == 0):
                                continue

                            time_slot = TimeSlot(
                                start=current_time,
                                end=slot_end,
                                day=day
                            )

                            # Check if the slot is valid
                            if not is_slot_valid(time_slot, course, year_schedule, schedule):
                                continue

                            # Assign the time slot
                            year_schedule.append(AssignedTimeSlot(
                                classroom=CLASSROOMS[i],
                                course=course,
                                time_slot=time_slot,
                                color_hex=COLORS[color_index]
                            ))

                            # we scan for all slots possible contigously and if we find one
                            # we just descrease the hours to schedule for that course and
                            # break time slots cycle to return to the day cycle loop and we 
                            # continue to assign on unassigned days yet.
                            # For every slot assigned, we then check if we need to assign more
                            # hours or not and if we successfully assigned a slot or not.
                            # We also need to descrease the hours still available for that day
                            hours_remaining -= 2
                            hours_left_per_day[day] -= 2
                            valid_slot_found = True
                            break

                    if not valid_slot_found:
                        print(f"\033[91mCannot find a slot for {course}, hours remaining: {hours_remaining}.\n\n\033[0m")
                        print(year_schedule)
                        raise ValueError("Unable to find valid slot for course")

                schedule.year_schedules.append(year_schedule)

            return schedule
        except ValueError:
            if use_heuristic:
                raise RuntimeError(f"{RED}Unable to build a valid schedule using heuristic, too many constraints{RESET}")
            else:
                # Shuffle the courses and retry
                for year_courses in courses_by_year:
                    random.shuffle(year_courses)

    raise RuntimeError(f"Unable to build a valid schedule after {attempt + 1} attempts")


def is_slot_valid(time_slot: TimeSlot, course: Course, year_schedule: list[AssignedTimeSlot], schedule: Schedule) -> bool:
    # Check if the slot is already occupied in the current year
    for assigned_slot in year_schedule:
        if (assigned_slot.time_slot.day == time_slot.day and
                assigned_slot.time_slot.start == time_slot.start):
            return False
        
    # Check if the teacher is unavailable
    for unavailable in course.teacher.unavailable_slots:
        if ((unavailable.day == None or time_slot.day == unavailable.day) and
                time_slot.start < unavailable.end and
                time_slot.end > unavailable.start):
            return False

    # Check for teacher conflicts across years
    for other_year_schedule in schedule.year_schedules:
        for assigned_slot in other_year_schedule:
            if (assigned_slot.course.teacher == course.teacher and
                    assigned_slot.time_slot.day == time_slot.day and
                    assigned_slot.time_slot.start == time_slot.start):
                return False

    return True