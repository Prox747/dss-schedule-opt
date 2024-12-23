import json
from model import Teacher, Course, TimeSlot

# Load JSON data and convert to Teacher objects
def extract_teachers(json_file_path):
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


