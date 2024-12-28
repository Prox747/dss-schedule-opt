import random
from input_builder import extract_teachers, extract_courses, build_first_schedule
from model import Teacher, Course, Schedule, AssignedTimeSlot
from constants import MAX_ITER, ALPHA, BETA, MAX_MOVES

def find_schedule() -> Schedule:
    teachers: list[Teacher] = extract_teachers('./data/teachers.json')
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
    schedule: Schedule = build_first_schedule(year1_courses, year2_courses, year3_courses)

    print(schedule.year_schedules[0])
    print("\n\n")
    print(schedule.year_schedules[1])
    print("\n\n")
    print(schedule.year_schedules[2])
    
    best_schedule: Schedule = local_search(schedule, teachers, year1_courses, year2_courses, year3_courses)
    
    return best_schedule

def evaluate_schedule(schedule: Schedule, teachers: list[Teacher]) -> float:
    empty_time_slot_penalty = 0
    teacher_violation_penalty = 0

    for year_schedule in schedule.year_schedules:
        for day in ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi"]:
            daily_slots = [slot for slot in year_schedule if slot.time_slot.day == day]
            if not daily_slots:
                continue

            # Sort daily slots by start time
            daily_slots.sort(key=lambda slot: slot.time_slot.start)
            
            # Identify the range of scheduled hours
            first_slot = daily_slots[0].time_slot.start
            last_slot = daily_slots[-1].time_slot.end

            # Calculate empty slots between the first and last scheduled hours
            occupied_hours = {hour for slot in daily_slots 
                              for hour in range(slot.time_slot.start, slot.time_slot.end)} # this just takes all daily slots' hours and puts them in a set 
            all_hours = set(range(first_slot, last_slot)) # this is a set with all day's hours (from first to last slot)
            empty_slots = len(all_hours - occupied_hours) # we subtract the sets to obtain the empty slots
            empty_time_slot_penalty += empty_slots

    for year_schedule in schedule.year_schedules:
        for slot in year_schedule:
            for undesired in slot.course.teacher.undesired_slots:
                if ((undesired.day == None or slot.time_slot.day == undesired.day) and
                        slot.time_slot.start < undesired.end and
                        slot.time_slot.end > undesired.start):
                    teacher_violation_penalty += 1  # Violation of preference

    return ALPHA * empty_time_slot_penalty + BETA * teacher_violation_penalty

def local_search(initial_schedule: Schedule, teachers: list[Teacher], courses_by_year: list[list[Course]]) -> Schedule:
    current_schedule = initial_schedule
    best_fitness = evaluate_schedule(current_schedule, teachers)

    for num_moves in range(1, MAX_MOVES + 1):
        for iteration in range(MAX_ITER):
            neighbor = current_schedule.copy()

            # we pick a random slot and then try to make one or more moves to enhance the fitness
            year_index = random.randint(0, len(courses_by_year) - 1)
            slot = random.choice(neighbor.year_schedules[year_index])
            for _ in range(num_moves):
                move = random.choice(["swap", "move"])

                if move == "swap":
                    neighbor = swap_time_slots(neighbor, year_index, slot)
                else:
                    neighbor = move_to_empty_slot(neighbor, year_index, slot)

            if is_schedule_valid(neighbor):
                fitness = evaluate_schedule(neighbor, teachers)

                if fitness < best_fitness:
                    current_schedule = neighbor
                    best_fitness = fitness

    return current_schedule

def swap_time_slots(schedule: Schedule, year_index: int, slot: AssignedTimeSlot) -> Schedule:
    neighbor = schedule.copy()
    other_slot = random.choice(neighbor.year_schedules[year_index])

    neighbor.year_schedules[year_index].remove(slot)
    neighbor.year_schedules[year_index].remove(other_slot)

    neighbor.year_schedules[year_index].append(AssignedTimeSlot(
        classroom=other_slot.classroom,
        teacher=slot.course.teacher,
        course=slot.course,
        time_slot=other_slot.time_slot
    ))

    neighbor.year_schedules[year_index].append(AssignedTimeSlot(
        classroom=slot.classroom,
        teacher=other_slot.course.teacher,
        course=other_slot.course,
        time_slot=slot.time_slot
    ))

    return neighbor

def move_to_empty_slot(schedule: Schedule, year_index: int, slot: AssignedTimeSlot) -> Schedule:
    neighbor = schedule.copy()
    empty_slots = [ts for ts in schedule.year_schedules[year_index]
                   if not any(slot.time_slot.start == ts.time_slot.start and
                              slot.time_slot.day == ts.time_slot.day for slot in neighbor.year_schedules[year_index])]

    if not empty_slots:
        return schedule

    new_slot = random.choice(empty_slots)
    neighbor.year_schedules[year_index].remove(slot)
    neighbor.year_schedules[year_index].append(AssignedTimeSlot(
        classroom=new_slot.classroom,
        teacher=slot.course.teacher,
        course=slot.course,
        time_slot=new_slot.time_slot
    ))

    return neighbor

# Checks for unavailable teachers slots or overlapping teachers lessons between years
def is_schedule_valid(schedule: Schedule) -> bool:
    for year_schedule in schedule.year_schedules:
        for slot in year_schedule:
            for other_year_schedule in schedule.year_schedules:
                if year_schedule == other_year_schedule:
                    continue
                if any(other_slot.course.teacher == slot.course.teacher and
                       other_slot.time_slot.day == slot.time_slot.day and
                       (other_slot.time_slot.start < slot.time_slot.end and
                        other_slot.time_slot.end > slot.time_slot.start)
                       for other_slot in other_year_schedule):
                    return False

            for unavailable in slot.course.teacher.unavailable_slots:
                if (slot.time_slot.day == unavailable.day and
                        slot.time_slot.start < unavailable.end and
                        slot.time_slot.end > unavailable.start):
                    return False

    return True