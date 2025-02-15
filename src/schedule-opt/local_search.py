import random
from copy import deepcopy

from input_builder import extract_teachers, extract_courses, build_first_schedule
from model import Teacher, Course, Schedule, AssignedTimeSlot, TimeSlot
from constants import MAX_ITER, ALPHA, BETA, MAX_MOVES, DAYS, MAX_DAILY_HOURS, START_TIME, END_TIME
from ansi_colors import *

def find_schedule() -> Schedule:
    teachers: list[Teacher] = extract_teachers('./data/teachers_easy.json')
    for teacher in teachers:
        print(teacher)
        print("\n\n")
        
    courses: list[Course] = extract_courses("./data/courses.json", teachers)
    for course in courses:
        print(course)
        print("\n\n")
        
    # we divide in years since the moves of the local search can only influence courses from the same year
    year1_courses: list[Course] = [course for course in courses if course.year == 1]
    year2_courses: list[Course] = [course for course in courses if course.year == 2]
    year3_courses: list[Course] = [course for course in courses if course.year == 3]

    # we get the first solution by just placing all the courses of one year contiguously
    schedule: Schedule = build_first_schedule(year1_courses, year2_courses, year3_courses, use_heuristic=True)

    print(f"{RED}FIRST SOLUTION BY YEAR{RESET}")
    print(schedule.year_schedules[0])
    print("\n\n")
    print(schedule.year_schedules[1])
    print("\n\n")
    print(schedule.year_schedules[2])
    
    best_schedule: Schedule = local_search(schedule, teachers, year1_courses, year2_courses, year3_courses)
    
    return best_schedule

def evaluate_schedule(schedule: Schedule, teachers: list[Teacher], log: bool):
    empty_slots_by_year: list[list[TimeSlot]] = []
    violations_start_end_by_year: list[list[AssignedTimeSlot]] = []
    violations_middle_by_year: list[list[AssignedTimeSlot]] = []
    
    num_empty_slots = 0
    num_violations = 0

    for year_schedule in schedule.year_schedules:
        year_empty_slots: list[TimeSlot] = []
        year_start_end_violations: list[AssignedTimeSlot] = []
        year_middle_violations: list[AssignedTimeSlot] = []

        for day in DAYS:
            daily_slots = sorted(
                [slot for slot in year_schedule if slot.time_slot.day == day],
                key=lambda slot: slot.time_slot.start
            )
            
            # check how many holes there are
            year_empty_slots.extend(find_empty_slots_between_lessons(daily_slots, day))

            # Check underised slots violation while also dividing them in two lists
            # start_end takes the first and last lesson of the day, while middle takes the other ones
            for i, slot in enumerate(daily_slots):
                # Determine if this is the first or last lesson of the day
                is_start_or_end = (i == 0 or i == len(daily_slots) - 1)
                
                for undesired in slot.course.teacher.undesired_slots:
                    if (undesired.day == slot.time_slot.day and
                        slot.time_slot.start < undesired.end and
                        slot.time_slot.end > undesired.start):
                        if is_start_or_end:
                            year_start_end_violations.append(slot)
                        else:
                            year_middle_violations.append(slot)
                        num_violations += 1
                        
                        if log:
                            print(f"{YELLOW}Violation of preference: Teacher {slot.course.teacher.name}\n" +
                               f"has a slot [{slot.time_slot.start}-{slot.time_slot.end}-{slot.time_slot.day if slot.time_slot.day else 'all'}]" +
                               f" - but dont want to work on [{undesired.start}-{undesired.end}-{undesired.day if undesired.day else 'all'}].\n\n{RESET}")

        num_empty_slots += len(year_empty_slots)

        empty_slots_by_year.append(year_empty_slots)
        violations_start_end_by_year.append(year_start_end_violations)
        violations_middle_by_year.append(year_middle_violations)
        
    fitness = ALPHA * num_empty_slots + BETA * num_violations

    return fitness, violations_start_end_by_year, violations_middle_by_year, empty_slots_by_year


def local_search(initial_schedule: Schedule, teachers: list[Teacher],
                 year1_courses: list[Course], year2_courses: list[Course],
                 year3_courses: list[Course]) -> Schedule:
    
    courses_by_year = [year1_courses, year2_courses, year3_courses]
    current_schedule = initial_schedule
    best_fitness, violations_start_end_by_year, violations_middle_by_year, empty_slots_by_year = evaluate_schedule(current_schedule, teachers, log=True)
    
    print(f"{GREEN}FIRST SCHEDULE FITNESS VALUE: {best_fitness}{RESET}\n")
    #print(f"{CYAN} violations middle: {violations_middle_by_year} \n \
    #      violations start-end: {violations_start_end_by_year} \n \
    #      empty_slots: {empty_slots_by_year}{RESET}")

    for num_moves in range(1, MAX_MOVES + 1):
        print(f"\033[91mTrying to improve using {num_moves}.\n\n\033[0m")
        improved: bool = False
        
        for iteration in range(1):
            # we pick a random slot and then try to make one or more moves to enhance the fitness
            year_index = random.randint(0, len(courses_by_year) - 1)
            slot = random.choice(current_schedule.year_schedules[year_index])
            for _ in range(num_moves):
                move = random.choice(["swap", "move"])

                if move == "swap":
                    neighbor = swap_time_slots(current_schedule, year_index, slot)
                else:
                    neighbor = move_to_empty_slot(current_schedule, year_index, slot)

            if is_schedule_valid(neighbor, True):
                fitness, violations_start_end_by_year, violations_middle_by_year, empty_slots_by_year = evaluate_schedule(neighbor, teachers, True)

                if fitness < best_fitness:
                    print(f"\033[92mFitness improved from {best_fitness} to {fitness}.\n\n\033[0m")
                    current_schedule = neighbor
                    best_fitness = fitness
                    improved = True
            
            if best_fitness == 0:
                break
        
        # we try adding more moves if the solution is not improving
        # TODO: this can become a treshold in the future
        if improved and best_fitness >= 4:
            break

    return current_schedule


def find_empty_slots_between_lessons(daily_slots: list[AssignedTimeSlot], day: str) -> list[TimeSlot]:
    empty_slots = []
    for i in range(len(daily_slots) - 1):
        current_end = daily_slots[i].time_slot.end
        next_start = daily_slots[i + 1].time_slot.start
        while current_end + 2 <= next_start:
            empty_slots.append(TimeSlot(start=current_end, end=current_end + 2, day=day))
            current_end += 2
    return empty_slots


def swap_time_slots(schedule: Schedule, year_index: int, slot: AssignedTimeSlot) -> Schedule:
    neighbor = deepcopy(schedule)
    year_schedule = neighbor.year_schedules[year_index]

    year_schedule.remove(slot)
    
    other_slot: AssignedTimeSlot = random.choice(year_schedule)
    year_schedule.remove(other_slot)

    year_schedule.append(AssignedTimeSlot(
        classroom=slot.classroom,
        teacher=slot.course.teacher,
        course=slot.course,
        time_slot=other_slot.time_slot,
        color_hex=slot.color_hex
    ))

    year_schedule.append(AssignedTimeSlot(
        classroom=slot.classroom,
        teacher=other_slot.course.teacher,
        course=other_slot.course,
        time_slot=slot.time_slot,
        color_hex=other_slot.color_hex
    ))

    return neighbor


def move_to_empty_slot(schedule: Schedule, year_index: int, slot: AssignedTimeSlot) -> Schedule:
    neighbor = deepcopy(schedule)
    year_schedule = neighbor.year_schedules[year_index]

    empty_slots = []

    if not empty_slots:
        return schedule

    print(f"empty slots for year {year_index}: {empty_slots}")
    
    new_slot = random.choice(empty_slots)
    year_schedule.remove(slot)
    year_schedule.append(AssignedTimeSlot(
        classroom=slot.classroom,
        teacher=slot.course.teacher,
        course=slot.course,
        time_slot=new_slot,
        color_hex=slot.color_hex
    ))
    
    return neighbor

# Checks for unavailable teachers slots or overlapping teachers lessons between years
def is_schedule_valid(schedule: Schedule, log: bool) -> bool:
    hours_per_day: dict[str, int] = {}
    for year_schedule in schedule.year_schedules:
        for day in DAYS:
            hours_per_day[day] = 0
            
        for slot in year_schedule:
            # check if the day still has space
            hours_per_day[slot.time_slot.day] += 2
            if hours_per_day[slot.time_slot.day] > MAX_DAILY_HOURS:
                if log:
                    print(f"{RED}Violation of strong constraint: TOO MANY HOURS ON {slot.time_slot.day}\n{RESET}")
                return False
            
            # check if there are overlapping lessons of same teachers between years 
            for other_year_schedule in schedule.year_schedules:
                if year_schedule == other_year_schedule:
                    continue
                if any(other_slot.course.teacher == slot.course.teacher and
                       other_slot.time_slot.day == slot.time_slot.day and
                       (other_slot.time_slot.start < slot.time_slot.end and
                        other_slot.time_slot.end > slot.time_slot.start)
                       for other_slot in other_year_schedule):
                    if log:
                        print(f"{RED}Violation of strong constraint: Teacher {slot.course.teacher.name}\n" +
                               f"has two overlapping lessons [{slot.time_slot.start}-{slot.time_slot.end}-{slot.time_slot.day if slot.time_slot.day else 'all'}]" +
                               f" - [{unavailable.start}-{unavailable.end}-{unavailable.day if unavailable.day else 'all'}].\n\n{RESET}")
                    return False

            # check if there are teachers teaching in their unavailable slots
            for unavailable in slot.course.teacher.unavailable_slots:
                if (slot.time_slot.day == unavailable.day and
                        slot.time_slot.start < unavailable.end and
                        slot.time_slot.end > unavailable.start):
                    if log:
                        print(f"{RED}Violation of strong constraint: Teacher {slot.course.teacher.name}\n" +
                               f"has a slot [{slot.time_slot.start}-{slot.time_slot.end}-{slot.time_slot.day if slot.time_slot.day else 'all'}]" +
                               f" - but can't work on [{unavailable.start}-{unavailable.end}-{unavailable.day if unavailable.day else 'all'}].\n\n{RESET}")
                    return False

    return True