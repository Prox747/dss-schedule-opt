export type Day = "Lunedi" | "Martedi" | "Mercoledi" | "Giovedi" | "Venerdi"

export interface TimeSlotDto {
    classroom_name: string
    course_name: string
    teacher_name: string
    start: number
    end: number
    day: Day
    color_hex: string
}
    
// we have a list for each year, and we have 3 years
export interface ScheduleDto {
    year_schedules: [
        TimeSlotDto[],
        TimeSlotDto[],
        TimeSlotDto[]
    ]
    init_fitness: number
    best_fitness: number
    query_time_ms: number
}