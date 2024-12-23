import axios from "axios";
import { ScheduleDto, TimeSlotDto } from "./model_dto";
import { example_output } from "./examples";

console.log(
    '🚀 Developed by Prox'
);

/* let searchInput = document.getElementById("search") as HTMLInputElement;

searchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        get_schedule();
    }
}); */

const colors = [
    "#556B2F", // Dark Olive Green
    "#8B4513", // Saddle Brown
    "#4682B4", // Steel Blue
    "#5F9EA0", // Cadet Blue
    "#7B68EE", // Medium Slate Blue
    "#708090", // Slate Gray
    "#9ACD32", // Yellow-Green
];

// Function to initialize the schedule grids
function initializeSchedule() {
    // we loop for each od the three years and init the grids
    for (let i = 1; i <= 3; i++) {
        const scheduleBody = document.getElementById(`${i}-schedule-body`) as HTMLElement;
        const hours = Array.from({ length: 10 }, (_, i) => 8 + i); // [8, 9, ..., 17]

        hours.forEach(hour => {
            const row = document.createElement("tr");

            // Time column
            const timeCell = document.createElement("td");
            timeCell.textContent = `${hour}:00 - ${hour + 1}:00`;
            row.appendChild(timeCell);

            // Empty cells for each day
            ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi"].forEach(dayId => {
                const cell = document.createElement("td");
                // each cell has an id in this format: "year-day-start_hour"
                cell.id = `${i}-${dayId}-${hour}`;
                cell.classList.add("p-0");
                row.appendChild(cell);
            });

            scheduleBody.appendChild(row);
        });
    }
}

// Function to populate the schedule table
function populateSchedule(data: ScheduleDto) {
    const yearSchedules = data.year_schedules;

    // we have 3 years
    yearSchedules.forEach((yearSchedule, index) => {
        console.log(`Printing YEAR ${index + 1}`)
        yearSchedule.forEach(slot => {
            for (let hour = slot.start; hour < slot.end; hour++) {
                // each cell has an id in this format: "year-day-start_hour"
                const cellId = `${index + 1}-${slot.day.toLowerCase()}-${hour}`;
                const cell = document.getElementById(cellId);
    
                console.log(cellId)
                if (cell) {
                    console.log(`printing cell for ${slot.day.toLowerCase()}-${hour}-${hour + 1}`)
                    cell.innerHTML = `
              <div class="class-cell" style="background-color:${slot.color_hex}">
                <strong>${slot.course_name}</strong><br>
                ${slot.teacher_name}<br>
                ${slot.classroom_name}
              </div>`;
                }
            }
        })
    });
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

function example() {
    // Initialize and populate the schedule
    initializeSchedule();
    populateSchedule(example_output);
}

example()