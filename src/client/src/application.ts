import axios from "axios";
import { ScheduleDto, TimeSlotDto } from "./model_dto";

console.log(
    '🚀 Developed by Prox',
    'color: purple; font-weight: bold;'
);

let searchInput = document.getElementById("search") as HTMLInputElement;

searchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        get_schedule();
    }
});

function viewSchedule(schedule: ScheduleDto) {
    if (!schedule) return;
    
    console.log(schedule);

    const queryTimeElement = document.getElementById('query-time');
    if (queryTimeElement) {
        queryTimeElement.textContent = `Schedule calculated in ${schedule.query_time_ms * 1000} seconds`;
    }

    const scheduleContainer = document.getElementById('schedule');
    if (scheduleContainer) {
        scheduleContainer.innerHTML = '';

        schedule.year_schedules.forEach(year_schedule => {
            const yearDiv = document.createElement('div');
            yearDiv.classList.add('result-item');

            yearDiv.innerHTML = ''; // TODO: html
            
            scheduleContainer.appendChild(yearDiv);
        });
    }
}

function get_schedule() {
    document.getElementById('search-result').style.display = 'block';

    axios.get(`http://localhost:13000/api/schedule`).then((response) => {
        console.log(response.data);

    }).catch((error) => {
        console.error('Error fetching schedule:', error);

        /* const scheduleContainer = document.getElementById('schedule-container');
        if (scheduleContainer) {
            scheduleContainer.innerHTML = '<p>Error fetching schedule.</p>';
        } */
    });
}