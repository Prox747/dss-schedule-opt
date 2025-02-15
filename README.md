# DSS-schedule-opt 🗓️
A university project focused on finding the optimal schedule for a university bachelor program given a set of constraints.

## Teachers input examples
To test the system 5 examples have been created in incresing difficulty (each slot is min 2 hours long). Each example contains underised and unavailable time slots expressed by each fictional teacher.
### Easy
Each teacher has two undesired and two unavailable slots. The slots are simple 2‑hour blocks with a light spread across the week.
### Medium
The slots are spread a bit differently by day and some blocks for first‑year teachers fall in the early morning while later courses are reserved for the upper years.
### Difficult
Each teacher lists three undesired and three unavailable slots. Now morning/early‐day slots are favored for first‑year instructors and later hours for those teaching advanced courses.
### Very Difficult
In this scenario each teacher has three slots per list and some of the entries are four‑hour blocks. The assignments now show more variety in day and time so that the algorithm must handle longer, overlapping blocks.
### Impossible
In this final example every teacher lists four undesired and four unavailable slots. Several of these blocks span four hours, and the distribution is intentionally heavy and overlapping to stress-test the scheduling algorithm.

