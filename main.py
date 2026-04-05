from pawpal_system import Task, Pet, Owner, Scheduler

def run_demo():
    print("--- 🐾 PawPal+ CLI Demo 🐾 ---\n")

    # 1. Initialize the Brain (Scheduler) and the Owner
    scheduler = Scheduler()
    owner = Owner(name="Jordan")

    # 2. Create at least two Pets [cite: 14-15]
    luna = Pet(name="Luna", species="Dog", age=3)
    milo = Pet(name="Milo", species="Cat", age=5)

    # 3. Add pets to the Owner and the Scheduler [cite: 20-21]
    owner.add_pet(luna)
    owner.add_pet(milo)
    scheduler.add_pet(luna)
    scheduler.add_pet(milo)

    # 4. Add at least three Tasks with different times [cite: 7-13]
    # Task 1 for Luna
    t1 = Task(id=1, description="Morning Walk", due_time="08:00", duration_mins=30, priority="high")
    luna.add_task(t1)

    # Task 2 for Milo
    t2 = Task(id=2, description="Breakfast Feeding", due_time="07:30", duration_mins=10, priority="high")
    milo.add_task(t2)

    # Task 3 for Luna
    t3 = Task(id=3, description="Afternoon Play", due_time="14:00", duration_mins=20, priority="medium")
    luna.add_task(t3)

    # 5. Generate and print "Today's Schedule" [cite: 22-24]
    print(f"Generating schedule for {owner.name}...")
    upcoming_tasks = scheduler.get_upcoming_tasks() # This calls our sorting logic 

    if not upcoming_tasks:
        print("No tasks scheduled for today.")
    else:
        print(f"{'TIME':<10} | {'PET':<10} | {'TASK':<20} | {'PRIORITY':<10}")
        print("-" * 55)
        for pet_name, task in upcoming_tasks:
            print(f"{task.due_time:<10} | {pet_name:<10} | {task.description:<20} | {task.priority:<10}")

    print("\n--- Demo Complete ---")

if __name__ == "__main__":
    run_demo()