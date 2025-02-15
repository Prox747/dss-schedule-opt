import random
from copy import deepcopy
from collections import defaultdict

from input_builder import extract_teachers, extract_courses, build_first_schedule
from model import Teacher, Course, Schedule, AssignedTimeSlot, TimeSlot
from constants import MAX_ITER, MAX_ITER_SLOT, ALPHA, BETA, DAYS, MAX_DAILY_HOURS, START_TIME, END_TIME, MOVE_TYPE
from ansi_colors import *

debug_cont = {
    "unavailable": 0,
    "same day": 0,
    "toomanyhours": 0,
    "overlap": 0
}

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
    
    best_schedule, init_fitness, best_fitness = local_search(schedule, teachers, year1_courses, year2_courses, year3_courses)
    
    return best_schedule, init_fitness, best_fitness

def evaluate_schedule(schedule: Schedule, log: bool):
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


def choose_slot_and_move(violations_middle, violations_start_end, empty_slots) -> tuple[str, AssignedTimeSlot]:
    slot = None
    
    # if there are a lot of violations of preference we try to address them
    if len(violations_middle) + len(violations_start_end) > len(empty_slots):
        # we try switching the middle ones, as we cannot move them (we create holes)
        if violations_middle == []:
            slot = random.choice(violations_start_end)
        if violations_start_end == []:
            slot = random.choice(violations_middle)
        if violations_start_end != [] and violations_middle != []:
            slot = random.choice(violations_middle if (random.random() < 0.7) else violations_start_end)
        move = MOVE_TYPE.SWAP.value
    # else we choose to fill the holes
    elif len(empty_slots) >= len(violations_middle) + len(violations_start_end):
        if violations_start_end != []:
            slot = random.choice(violations_start_end)
        move = MOVE_TYPE.MOVE.value
            
    return move, slot
        

def local_search(initial_schedule: Schedule, teachers: list[Teacher],
                 year1_courses: list[Course], year2_courses: list[Course],
                 year3_courses: list[Course]) -> Schedule:
    
    courses_by_year = [year1_courses, year2_courses, year3_courses]
    current_schedule = initial_schedule
    init_fitness, violations_start_end_by_year, violations_middle_by_year, empty_slots_by_year = evaluate_schedule(current_schedule, log=True)
    
    best_fitness = init_fitness
    
    print(f"{GREEN}FIRST SCHEDULE FITNESS VALUE: {best_fitness}{RESET}\n")
    #print(f"{CYAN} violations middle: {violations_middle_by_year} \n \
    #      violations start-end: {violations_start_end_by_year} \n \
    #      empty_slots: {empty_slots_by_year}{RESET}")

    for iteration in range(MAX_ITER):
        improved = False
        # we pick an optimal slot and then try to make a move to make it better
        year_index = random.randint(0, len(courses_by_year) - 1)
        year_scedule = current_schedule.year_schedules[year_index]
        move, slot = choose_slot_and_move(violations_middle_by_year[year_index],
                                    violations_start_end_by_year[year_index],
                                    empty_slots_by_year[year_index])
        # if no optimal slot is found, just select one randomly
        # To diversify research, 10% probability to select a random slot
        if slot == None or random.random() < 0.1:
            slot = random.choice(year_scedule)
        
        if move == "swap":
            # try swapping in the same day
            # if it does not improve, switch between days
            day = slot.time_slot.day
            day_slots = [s for s in year_scedule if s.time_slot.day == day and s.time_slot.start != slot.time_slot.start]
            slots_to_choose_from = day_slots
            for iter in range(MAX_ITER_SLOT):
                neighbor, swapped_slot = swap_time_slots(current_schedule, year_index, slot, slots_to_choose_from=slots_to_choose_from)
                
                # Update Fitness
                if is_schedule_valid(neighbor, True):
                    fitness, new_violations_start_end_by_year, new_violations_middle_by_year, new_empty_slots_by_year = evaluate_schedule(neighbor, True)

                    if fitness < best_fitness:
                        print(f"{GREEN}Fitness improved from {best_fitness} to {fitness}.\n\n{RESET}")
                        violations_start_end_by_year = new_violations_start_end_by_year
                        violations_middle_by_year = new_violations_middle_by_year
                        empty_slots_by_year = new_empty_slots_by_year
                        current_schedule = neighbor
                        best_fitness = fitness
                        improved = True
                    
                # remove the last swapped slot to not select it again
                slots_to_choose_from.remove(swapped_slot)
                
                # we break if we improve or have none slots to choose
                if improved or len(slots_to_choose_from) == 0:
                    break
            
            if not improved:
                # Then try to swap between days (without trying the same day slots again or the chosen slot itself)
                day_slots.append(slot)
                slots_to_choose_from = [s for s in year_scedule if s not in day_slots]
                
                print(f"Didn't improve on day slots, trying swapping between days\n")
                for iter in range(MAX_ITER_SLOT):
                    neighbor, swapped_slot = swap_time_slots(current_schedule, year_index, slot, slots_to_choose_from=slots_to_choose_from)
                    
                    # Update Fitness
                    if is_schedule_valid(neighbor, True):
                        fitness, new_violations_start_end_by_year, new_violations_middle_by_year, new_empty_slots_by_year = evaluate_schedule(neighbor, True)

                        if fitness < best_fitness:
                            print(f"{GREEN}Fitness improved from {best_fitness} to {fitness}.\n\n{RESET}")
                            violations_start_end_by_year = new_violations_start_end_by_year
                            violations_middle_by_year = new_violations_middle_by_year
                            empty_slots_by_year = new_empty_slots_by_year
                            current_schedule = neighbor
                            best_fitness = fitness
                            improved = True
                    
                    # remove the last swapped slot to not select it again
                    slots_to_choose_from.remove(swapped_slot)
                    
                    # we break if we improve or have none slots to choose
                    if improved or len(slots_to_choose_from) == 0:
                        break
        else:
            neighbor = move_to_empty_slot(current_schedule, year_index, slot)

        if best_fitness == 0:
            break

    print(f"EVAL OF FINAL SCHEDULE:\n")
    evaluate_schedule(current_schedule, True)
    
    print(f"{CYAN}Finished after {MAX_ITER} iterations ({MAX_ITER_SLOT} iterations per slot).\
                  \nInitial Fitness: {init_fitness} --- Best Fitness: {best_fitness}\n\
                  {RED}DEBUG: {debug_cont.items()}\n")
    return current_schedule, init_fitness, best_fitness


def find_empty_slots_between_lessons(daily_slots: list[AssignedTimeSlot], day: str) -> list[TimeSlot]:
    empty_slots = []
    for i in range(len(daily_slots) - 1):
        current_end = daily_slots[i].time_slot.end
        next_start = daily_slots[i + 1].time_slot.start
        while current_end + 2 <= next_start:
            empty_slots.append(TimeSlot(start=current_end, end=current_end + 2, day=day))
            current_end += 2
    return empty_slots


def swap_time_slots(schedule: Schedule, year_index: int, slot: AssignedTimeSlot, slots_to_choose_from: list[AssignedTimeSlot] = None) -> tuple[Schedule, AssignedTimeSlot]:
    neighbor = deepcopy(schedule)
    year_schedule = neighbor.year_schedules[year_index]

    year_schedule.remove(slot)
    
    if slots_to_choose_from == None or slots_to_choose_from == []:
        slots_to_choose_from = year_schedule
    
    other_slot: AssignedTimeSlot = random.choice(slots_to_choose_from)
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

    return neighbor, other_slot


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
    
    for i, year_schedule in enumerate(schedule.year_schedules):
        for day in DAYS:
            hours_per_day[day] = MAX_DAILY_HOURS
            # on third year we have 2 more hours per day
            if i == 2:
                hours_per_day[day] += 2
            # we need this map to know if a course is already in a day
            day2courses: dict[str, list[str]] = defaultdict(list)
            
        for slot in year_schedule:
            # check if the course is alredy taught that day
            if slot.course.name in day2courses[slot.time_slot.day]:
                if log:
                    print(f"{RED}Violation of strong constraint: Course {slot.course.name} already taught on {slot.time_slot.day}\n{RESET}")
                debug_cont["same day"] += 1
                return False
            else:
                day2courses[slot.time_slot.day].append(slot.course.name)
            
            # check if the day still has space
            hours_per_day[slot.time_slot.day] -= 2
            if hours_per_day[slot.time_slot.day] < 0:
                if log:
                    print(f"{RED}Violation of strong constraint: TOO MANY HOURS ON {slot.time_slot.day} on year {i + 1}\n{RESET}")
                debug_cont["toomanyhours"] += 1
                return False
            
            # check if there are overlapping lessons of same teachers between years 
            for j, other_year_schedule in enumerate(schedule.year_schedules):
                if not( (i,j) in {(1,2), (1,3), (2,3)} ):
                    continue
                if any(other_slot.course.teacher.name == slot.course.teacher.name and
                       other_slot.time_slot.day == slot.time_slot.day and
                       (other_slot.time_slot.start < slot.time_slot.end and
                        other_slot.time_slot.end > slot.time_slot.start)
                       for other_slot in other_year_schedule):
                    if log:
                        print(f"{RED}Violation of strong constraint: Teacher {slot.course.teacher.name}\n" +
                               f"has two overlapping lessons [{slot.time_slot.start}-{slot.time_slot.end}-{slot.time_slot.day if slot.time_slot.day else 'all'}]" +
                               f" - on years {i+1} and {j+1}.\n\n{RESET}")
                    debug_cont["overlap"] += 1
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
                    debug_cont["unavailable"] += 1
                    return False

    return True