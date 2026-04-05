from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import datetime, timedelta # [cite: 31]


@dataclass
class Task:
    """Sets the task status to completed."""
    id: int
    description: str
    due_time: str 
    duration_mins: int
    priority: str 
    frequency: str = "Once"
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Sets task to complete and triggers recurrence if applicable."""
        self.is_completed = True # [cite: 7]
        # Logic for Phase 4: Step 3 [cite: 58-59]
        if self.frequency == "Daily":
            # AI Suggestion: Use timedelta(days=1) to calculate tomorrow [cite: 31]
            pass
@dataclass
class Pet:
    """Appends a new task to the pet's task list."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a care task to the pet's internal task list."""
        self.tasks.append(task)

@dataclass
class Owner:
    """Registers a new pet profile under the owner's management."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Gathers every task from every registered pet into a unified list."""
        self.pets.append(pet)

class Scheduler:
    def __init__(self):
        """"Initializes the scheduler with an empty list of pets."""
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the scheduler's tracking system."""
        self.pets.append(pet)

    def _time_to_minutes(self, time_str: str) -> int:
        """Converts HH:MM format to minutes since midnight for comparison."""
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    def get_all_tasks(self) -> List[Tuple[str, Task]]:
        """Aggregates all tasks from every registered pet into a single list of tuples"""
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet.name, task))
        return all_tasks

    def get_upcoming_tasks(self) -> List[Tuple[str, Task]]:
        """Returns a chronologically sorted list of all scheduled tasks using a lambda key."""
        tasks = self.get_all_tasks() # [cite: 22-24]
        # The lambda x: x[1].due_time tells Python to sort by the Task's time string [cite: 23, 53]
        return sorted(tasks, key=lambda x: x[1].due_time)

    def check_conflicts(self, new_task: Task) -> bool:
        """Returns True if the new task overlaps with any existing incomplete tasks."""
        new_start = self._time_to_minutes(new_task.due_time)
        new_end = new_start + new_task.duration_mins
        
        for pet in self.pets: # [cite: 20]
            for task in pet.tasks: # [cite: 12]
                if task.is_completed: continue
                
                ex_start = self._time_to_minutes(task.due_time)
                ex_end = ex_start + task.duration_mins
                
                # Conflict math: If they don't start after or end before, they overlap 
                if not (new_end <= ex_start or new_start >= ex_end):
                    return True
        return False