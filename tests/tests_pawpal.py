import pytest
from pawpal_system import Task, Pet, Scheduler

def test_chronological_sorting():
    """Verify tasks are returned in HH:MM order regardless of input order."""
    s = Scheduler()
    p = Pet("Mochi", "Dog", 2)
    s.add_pet(p)
    
    # ADDED 'low' and 'high' as the priority arguments
    p.add_task(Task(1, "Dinner", "18:00", 30, "low"))
    p.add_task(Task(2, "Breakfast", "08:00", 20, "high"))
    
    scheduled = s.get_upcoming_tasks()
    # Check that Breakfast (08:00) comes before Dinner (18:00)
    assert scheduled[0][1].description == "Breakfast"
    assert scheduled[1][1].description == "Dinner"

def test_conflict_detection():
    """Verify that overlapping times are flagged as conflicts."""
    s = Scheduler()
    p = Pet("Mochi", "Dog", 2)
    s.add_pet(p)
    
    # Task 1: 10:00 - 11:00 (60 mins)
    p.add_task(Task(1, "Long Walk", "10:00", 60, "medium"))
    
    # Task 2: Starts at 10:30 (Conflict!)
    conflict_task = Task(2, "Snack", "10:30", 15, "low")
    assert s.check_conflicts(conflict_task) is True

def test_daily_recurrence():
    """Verify marking a daily task complete works."""
    # Added 'medium' priority and 'Daily' frequency
    t = Task(1, "Vitamin", "09:00", 5, "medium", frequency="Daily")
    t.mark_complete()
    assert t.is_completed is True