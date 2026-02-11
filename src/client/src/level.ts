type Level = 1 | 2 | 3 | 4 | 5 | 6 | 7;

export function isLevel(value: number): value is Level {
    return value >= 1 && value <= 7;
  }

export const levelDescriptions: Record<Level, string> = {
    1: "Ogni docente ha due slot indesiderati e due non disponibili. Gli slot sono semplici blocchi di 2 ore, distribuiti leggermente durante la settimana.",
    2: "Gli slot sono distribuiti in modo leggermente diverso nei vari giorni. Alcuni blocchi per i docenti del primo anno cadono al mattino presto, mentre i corsi degli anni successivi sono riservati alle fasce orarie più tarde.",
    3: "Ogni docente indica tre slot indesiderati e tre non disponibili. Le fasce mattutine e di inizio giornata sono favorite per i docenti del primo anno, mentre le ore più tarde sono assegnate ai corsi avanzati.",
    4: "Ogni docente ha tre slot per lista e alcuni sono blocchi di quattro ore. Le assegnazioni mostrano maggiore varietà di giorni e orari, richiedendo la gestione di blocchi più lunghi e sovrapposti.",
    5: "Ogni docente indica quattro slot indesiderati e quattro non disponibili. Diversi blocchi durano quattro ore e la distribuzione è volutamente pesante e sovrapposta per stressare l’algoritmo.",
    6: "Ogni docente ha cinque slot indesiderati e cinque non disponibili, con alcuni blocchi di quattro ore e altri sovrapposti o estesi su gran parte della giornata.",
    7: "Ogni docente ha sei slot indesiderati e sei non disponibili, molti dei quali durano quattro ore e si sovrappongono. La configurazione è volutamente iper-vincolata, costringendo l’algoritmo a scegliere tra molteplici conflitti."
};