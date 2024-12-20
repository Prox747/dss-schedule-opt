export interface TimeSlotDto {
    classroom_name: string
    course_name: string
    teacher_name: string
    start: number
    end: number
}
    
// we have a list for each year, and we have 3 years
export interface ScheduleDto {
    year_schedules: [
        TimeSlotDto[]
    ]
    query_time_ms: number
}