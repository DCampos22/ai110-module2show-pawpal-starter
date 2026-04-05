# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML included four classes: Task, Pet, Owner, and Scheduler. I designed Task as a dataclass holding the core scheduling fields — due_time, duration_mins, priority, and frequency. Pet owned a list of tasks and handled adding them. Owner grouped pets under a single profile. Scheduler was the central brain: it tracked all pets and was responsible for aggregating tasks, sorting them, and detecting conflicts. From the start, I kept domain logic (what a task is, what a pet owns) separate from scheduling logic (when things happen, what conflicts).

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

The main change I made during implementation was pulling conflict detection into the Scheduler rather than leaving it on Pet or Task. Initially I considered having Task handle some of this, but it quickly became clear that detecting a conflict requires comparing across all pets — not just within one pet's task list. Moving check_conflicts to Scheduler made more sense because the scheduler is the only class with a full view of the schedule.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers two main constraints: time (when a task is due) and duration (how long it takes). Tasks carry a priority field (high, medium, low), but the primary sort key for get_upcoming_tasks is due_time. Conflict detection uses both due_time and duration_mins to determine whether two tasks overlap: a conflict exists if the new task's window intersects any existing incomplete task's window.
I chose time as the primary constraint because a daily schedule has to be chronologically coherent, you can't complete a 14:00 task before an 08:00 one regardless of priority.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler sorts strictly by due_time rather than by a combination of time and priority. This means a low-priority task scheduled for 08:00 appears before a high-priority task scheduled for 09:00. The tradeoff is simplicity and predictability: the owner always sees the day in time order, which is more readable and actionable than a priority-first sort that could scramble the chronology. For a future iteration, priority could serve as a tiebreaker between tasks at the same time slot.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI during the design phase to pressure-test my UML — specifically to check whether my class responsibilities were cleanly separated. I also used it during debugging, especially for the conflict detection math. The most useful prompts were ones where I described the specific behavior I wanted (e.g., "given two tasks with overlapping time windows, return True") and asked the AI to verify whether my logic handled edge cases, like tasks that share an endpoint but don't actually overlap.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment where I didn't take the AI suggestion as-is was around mark_complete and recurrence. The AI suggested using timedelta(days=1) to automatically advance the due_time on a daily task. I left this as a pass placeholder because the current system stores due_time as a plain string ("HH:MM"), not a datetime object, so auto-advancing it would require either converting the field type or parsing and reformatting the string every time. I verified this by tracing through what timedelta would actually need as input, confirmed it wouldn't work cleanly on a raw string, and decided to defer the recurrence logic to a later phase.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I wrote three tests:

Chronological sorting (test_chronological_sorting): Adds tasks out of order and confirms get_upcoming_tasks returns them sorted by due_time. This is the core scheduling behavior, so it had to be correct.
Conflict detection (test_conflict_detection): Adds a 60-minute task starting at 10:00, then checks that a task starting at 10:30 is flagged as a conflict. This validates the overlap math in check_conflicts.
Daily recurrence marking (test_daily_recurrence): Creates a daily task, calls mark_complete, and asserts is_completed is True. This is a basic sanity check that the method works even though full recurrence logic isn't implemented yet.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm confident the sorting and conflict detection work correctly for standard inputs. The edge cases I'd test next are: tasks that share an exact endpoint (e.g., one ends at 10:00, the next starts at 10:00, should not be a conflict), tasks that span midnight, and what happens when a pet has no tasks at all.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with how clean the class separation turned out. Task, Pet, Owner, and Scheduler each have a clear, single responsibility, and none of them bleeds into the others' logic. The conflict detection math in check_conflicts also came out cleaner than I expected — the not-overlap condition (new_end <= ex_start or new_start >= ex_end) is easy to read and reason about.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

In the next iteration, I'd store due_time as a proper datetime or time object instead of a raw string. Right now the scheduler works because HH:MM strings happen to sort correctly lexicographically, but that's fragile. It also blocks the recurrence logic — you can't add a day to a string. Switching to a proper time type early would make the whole system more robust.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important thing I learned is that the design decisions you make about data types early on constrain what you can implement later. Storing due_time as a string felt convenient at first, but it cascaded into limitations around recurrence and made _time_to_minutes a necessary workaround. Designing with the full feature set in mind, even if you're not implementing everything yet — saves a lot of refactoring down the line.

