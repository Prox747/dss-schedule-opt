from enum import Enum

DAYS = ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi"]
START_TIME = 8  # Start of the day
END_TIME = 18  # End of the day
CLASSROOMS: list[str] = ["N18", "N11", "N13"]

MAX_ITER = 1500 # number of slots iterated
MAX_ITER_NO_IMPROVEMENT = 300 # maximum number of iterations to do where no improvement is found
ALPHA = 1 # weight for the empty slots
BETA = 1 # weight for the teacher slot preference
MAX_DAILY_HOURS = 6

class MOVE_TYPE(Enum):
    SWAP = "swap"
    MOVE = "move"

COLORS: list[str] = [
    "#556B2F", # Dark Olive Green
    "#8B4513", # Saddle Brown
    "#4682B4", # Steel Blue
    "#5F9EA0", # Cadet Blue
    "#7B68EE", # Medium Slate Blue
    "#708090", # Slate Gray
    "#9ACD32", # Yellow-Green
    "#D2691E", # Chocolate
]