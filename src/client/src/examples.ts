import { ScheduleDto } from "./model_dto";

const colors = [
    "#556B2F", // Dark Olive Green
    "#8B4513", // Saddle Brown
    "#4682B4", // Steel Blue
    "#5F9EA0", // Cadet Blue
    "#7B68EE", // Medium Slate Blue
    "#708090", // Slate Gray
    "#9ACD32", // Yellow-Green
];

export const example_data: ScheduleDto = {
    year_schedules: [
      // Year 1
      [
        { classroom_name: "N18", course_name: "Fisica I", teacher_name: "Matteo Rosati", start: 8, end: 10, day: "Lunedi", color_hex: colors[0] },
        { classroom_name: "N18", course_name: "Fondamenti di Informatica", teacher_name: "Fabrizio Frati", start: 10, end: 12, day: "Lunedi", color_hex: colors[1] },
        { classroom_name: "N18", course_name: "Fisica I", teacher_name: "Matteo Rosati", start: 8, end: 10, day: "Martedi", color_hex: colors[0] },
        { classroom_name: "N18", course_name: "Fondamenti di Informatica", teacher_name: "Fabrizio Frati", start: 10, end: 12, day: "Martedi", color_hex: colors[1] },
        { classroom_name: "N18", course_name: "Fisica I", teacher_name: "Matteo Rosati", start: 8, end: 10, day: "Mercoledi", color_hex: colors[0] },
        { classroom_name: "N18", course_name: "Fondamenti di Informatica", teacher_name: "Fabrizio Frati", start: 10, end: 12, day: "Mercoledi", color_hex: colors[1] },
        { classroom_name: "N18", course_name: "Fisica I", teacher_name: "Matteo Rosati", start: 8, end: 10, day: "Giovedi", color_hex: colors[0] },
        { classroom_name: "N18", course_name: "Fondamenti di Informatica", teacher_name: "Fabrizio Frati", start: 10, end: 12, day: "Giovedi", color_hex: colors[1] },
        { classroom_name: "N18", course_name: "Fisica I", teacher_name: "Matteo Rosati", start: 8, end: 10, day: "Venerdi", color_hex: colors[0] },
        { classroom_name: "N18", course_name: "Fondamenti di Informatica", teacher_name: "Fabrizio Frati", start: 10, end: 12, day: "Venerdi", color_hex: colors[1] },
        { classroom_name: "N18", course_name: "Fisica I", teacher_name: "Riccardo Borghi", start: 14, end: 16, day: "Lunedi", color_hex: colors[2] },
        { classroom_name: "N18", course_name: "Fondamenti di Informatica", teacher_name: "Carla Limongelli", start: 14, end: 16, day: "Martedi", color_hex: colors[3] },
        { classroom_name: "N18", course_name: "Fisica I", teacher_name: "Riccardo Borghi", start: 14, end: 16, day: "Mercoledi", color_hex: colors[2] },
        { classroom_name: "N18", course_name: "Fondamenti di Informatica", teacher_name: "Carla Limongelli", start: 14, end: 16, day: "Giovedi", color_hex: colors[3] },
        { classroom_name: "N18", course_name: "Fisica I", teacher_name: "Riccardo Borghi", start: 14, end: 16, day: "Venerdi", color_hex: colors[2] },
        { classroom_name: "N18", course_name: "Fondamenti di Informatica", teacher_name: "Carla Limongelli", start: 16, end: 18, day: "Lunedi", color_hex: colors[4] },
        { classroom_name: "N18", course_name: "Fisica I", teacher_name: "Riccardo Borghi", start: 16, end: 18, day: "Martedi", color_hex: colors[2] },
        { classroom_name: "N18", course_name: "Fondamenti di Informatica", teacher_name: "Carla Limongelli", start: 16, end: 18, day: "Mercoledi", color_hex: colors[4] },
        { classroom_name: "N18", course_name: "Fisica I", teacher_name: "Riccardo Borghi", start: 16, end: 18, day: "Giovedi", color_hex: colors[2] },
        { classroom_name: "N18", course_name: "Fondamenti di Informatica", teacher_name: "Carla Limongelli", start: 16, end: 18, day: "Venerdi", color_hex: colors[4] }
      ],
      // Year 2
      [
        { classroom_name: "N11", course_name: "Fondamenti di Automatica", teacher_name: "Stefano Panzieri", start: 14, end: 15, day: "Lunedi", color_hex: colors[0] },
        { classroom_name: "N11", course_name: "Calcolatori Elettronici", teacher_name: "Riccardo Torlone", start: 14, end: 15, day: "Martedi", color_hex: colors[1] },
        { classroom_name: "N11", course_name: "Fondamenti di Automatica", teacher_name: "Stefano Panzieri", start: 14, end: 15, day: "Mercoledi", color_hex: colors[0] },
        { classroom_name: "N11", course_name: "Fondamenti di Automatica", teacher_name: "Stefano Panzieri", start: 14, end: 15, day: "Giovedi", color_hex: colors[0] },
        { classroom_name: "N11", course_name: "Calcolatori Elettronici", teacher_name: "Riccardo Torlone", start: 14, end: 15, day: "Venerdi", color_hex: colors[1] },
        { classroom_name: "N11", course_name: "Fondamenti di Automatica", teacher_name: "Stefano Panzieri", start: 15, end: 16, day: "Lunedi", color_hex: colors[0] },
        { classroom_name: "N11", course_name: "Calcolatori Elettronici", teacher_name: "Riccardo Torlone", start: 15, end: 16, day: "Martedi", color_hex: colors[1] },
        { classroom_name: "N11", course_name: "Fondamenti di Automatica", teacher_name: "Stefano Panzieri", start: 15, end: 16, day: "Mercoledi", color_hex: colors[0] },
        { classroom_name: "N11", course_name: "Fondamenti di Automatica", teacher_name: "Stefano Panzieri", start: 15, end: 16, day: "Giovedi", color_hex: colors[0] },
        { classroom_name: "N11", course_name: "Calcolatori Elettronici", teacher_name: "Riccardo Torlone", start: 15, end: 16, day: "Venerdi", color_hex: colors[1] },
        { classroom_name: "N11", course_name: "Programmazione Orientata agli Oggetti", teacher_name: "Valter Crescenzi", start: 16, end: 18, day: "Lunedi", color_hex: colors[2] },
        { classroom_name: "N11", course_name: "Ricerca Operativa", teacher_name: "D'Ariano/Samà", start: 16, end: 18, day: "Martedi", color_hex: colors[3] },
        { classroom_name: "N11", course_name: "Programmazione Orientata agli Oggetti", teacher_name: "Valter Crescenzi", start: 16, end: 18, day: "Mercoledi", color_hex: colors[2] },
        { classroom_name: "N11", course_name: "Ricerca Operativa", teacher_name: "D'Ariano/Samà", start: 16, end: 18, day: "Giovedi", color_hex: colors[3] },
        { classroom_name: "N11", course_name: "Programmazione Orientata agli Oggetti", teacher_name: "Valter Crescenzi", start: 16, end: 18, day: "Venerdi", color_hex: colors[2] }
      ],
      // Year 3
      [
        { classroom_name: "N11", course_name: "Sistemi Informativi su Web", teacher_name: "Paolo Merialdo", start: 8, end: 9, day: "Lunedi", color_hex: colors[0] },
        { classroom_name: "N11", course_name: "Sistemi Informativi su Web", teacher_name: "Paolo Merialdo", start: 8, end: 9, day: "Martedi", color_hex: colors[0] },
        { classroom_name: "N11", course_name: "Sistemi Informativi su Web", teacher_name: "Paolo Merialdo", start: 8, end: 9, day: "Giovedi", color_hex: colors[0] },
        { classroom_name: "N11", course_name: "Sistemi Informativi su Web", teacher_name: "Paolo Merialdo", start: 9, end: 10, day: "Lunedi", color_hex: colors[0] },
        { classroom_name: "N11", course_name: "Sistemi Informativi su Web", teacher_name: "Paolo Merialdo", start: 9, end: 10, day: "Martedi", color_hex: colors[0] },
        { classroom_name: "N11", course_name: "Sistemi Informativi su Web", teacher_name: "Paolo Merialdo", start: 9, end: 10, day: "Giovedi", color_hex: colors[0] },
        { classroom_name: "N11", course_name: "Analisi e Progettazione del Software", teacher_name: "Luca Cabibbo", start: 10, end: 11, day: "Lunedi", color_hex: colors[1] },
        { classroom_name: "N11", course_name: "Analisi e Progettazione del Software", teacher_name: "Luca Cabibbo", start: 10, end: 11, day: "Martedi", color_hex: colors[1] },
        { classroom_name: "N11", course_name: "Analisi e Progettazione del Software", teacher_name: "Luca Cabibbo", start: 10, end: 11, day: "Giovedi", color_hex: colors[1] },
        { classroom_name: "N11", course_name: "Analisi e Progettazione del Software", teacher_name: "Luca Cabibbo", start: 11, end: 12, day: "Lunedi", color_hex: colors[1] },
        { classroom_name: "N11", course_name: "Analisi e Progettazione del Software", teacher_name: "Luca Cabibbo", start: 11, end: 12, day: "Martedi", color_hex: colors[1] },
        { classroom_name: "N11", course_name: "Analisi e Progettazione del Software", teacher_name: "Luca Cabibbo", start: 11, end: 12, day: "Giovedi", color_hex: colors[1] }
      ]
    ],
    query_time_ms: 123,
  };