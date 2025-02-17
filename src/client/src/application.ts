import axios from "axios";
import { ScheduleDto, TimeSlotDto } from "./model_dto";
import { example_output } from "./examples";

console.log(
    '🚀 Developed by Prox'
);

// Simple delay function
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

initializeSchedule();

let getScheduleBtn = document.getElementById("get-schedule-btn") as HTMLButtonElement;
let spinner = document.getElementById("spinner") as HTMLElement;

console.log(spinner, getScheduleBtn);

getScheduleBtn.addEventListener("click", async () => {
        spinner.classList.remove("d-none");
        getScheduleBtn.disabled = true;

        await get_schedule();
    
        spinner.classList.add("d-none");
        getScheduleBtn.disabled = false;
});

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
    // we loop for each of the three years and init the grids
    for (let i = 1; i <= 3; i++) {
        const scheduleBody = document.getElementById(`${i}-schedule-body`) as HTMLElement;

        // Clear any previously generated schedule rows
        scheduleBody.innerHTML = "";
        
        const hours = Array.from({ length: 10 }, (_, i) => 8 + i); // [8, 9, ..., 17]

        hours.forEach(hour => {
            const row = document.createElement("tr");

            // Time column
            const timeCell = document.createElement("td");
            timeCell.textContent = `${hour}:00 - ${hour + 1}:00`;
            // we add a bottom left border if we are on 17-18 time slot
            if (hour == 17) {
                timeCell.classList.add("last-left-cell");
            }

            row.appendChild(timeCell);

            // Empty cells for each day
            ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi"].forEach(dayId => {
                const cell = document.createElement("td");
                // each cell has an id in this format: "year-day-start_hour"
                cell.id = `${i}-${dayId}-${hour}`;

                //to add bottom right rounded border
                if (cell.id.includes("venerdi-17")) {
                    cell.classList.add("last-right-cell");
                }
                cell.classList.add("p-0");
                
                row.appendChild(cell);
            });

            scheduleBody.appendChild(row);
        });
    }
}

// Function to populate the schedule table
function populateSchedule(data: ScheduleDto) {
    // empty the previous schedule
    initializeSchedule()

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

    // write query time taken
    const info = document.getElementById('query-info') as HTMLElement;
    info.textContent = `🕒Tempo di calcolo: ${data.query_time_ms} ms    👋Fitness Iniziale: ${data.init_fitness}    💪Fitness Migliore: ${data.best_fitness}`;
}

async function get_schedule() {
    await axios.get(`http://localhost:13000/api/schedule`).then((response) => {
        console.log(response.data);
        populateSchedule(response.data);

    }).catch((error) => {
        console.error('Error fetching schedule:', error);
    });
}

function example() {
    // Initialize and populate the schedule
    initializeSchedule();
    populateSchedule(example_output);
}