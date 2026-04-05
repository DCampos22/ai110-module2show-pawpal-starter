import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

# 1. Initialize the "Vault" (Session State)
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
    st.session_state.scheduler = Scheduler()
    
    # Create default pet
    default_pet = Pet(name="Mochi", species="dog", age=2)
    
    # Register pet to both logic classes
    st.session_state.owner.add_pet(default_pet)
    st.session_state.scheduler.add_pet(default_pet)
    st.session_state.current_pet = default_pet

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

with st.sidebar:
    st.header("👤 Profile Settings")
    # Update the Owner object in the 'vault'
    new_owner_name = st.text_input("Owner Name", value=st.session_state.owner.name)
    st.session_state.owner.name = new_owner_name
    
    st.divider()
    
    st.header("🐶 Pet Settings")
    # Update the Pet object in the 'vault'
    pet = st.session_state.scheduler.pets[0]
    pet.name = st.text_input("Pet Name", value=pet.name)
    pet.species = st.selectbox("Species", ["dog", "cat", "other"], 
                               index=["dog", "cat", "other"].index(pet.species))
    
    st.success(f"Profiles updated for {st.session_state.owner.name} & {pet.name}!")

# --- UI Header ---
with st.expander("Scenario & Instructions", expanded=False):
    st.markdown("""
    **PawPal+** is your pet care planning assistant. 
    Add tasks below, and the system will use your backend logic to detect conflicts 
    and generate an optimized daily schedule.
    """)

st.divider()

# --- Input Section ---
st.subheader("Add a Task")
col1, col2, col3, col4 = st.columns(4)

with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_time = st.time_input("Start Time", value=None) 
with col3:
    duration = st.number_input("Duration (mins)", min_value=1, max_value=240, value=20)
with col4:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2) 


if st.button("Add task"):
    # Format time safely for your Scheduler logic
    formatted_time = task_time.strftime("%H:%M") if task_time else "08:00"

    # 1. Create the Task object
    new_task = Task(
        id=len(st.session_state.scheduler.get_all_tasks()) + 1,
        description=task_title,
        due_time=formatted_time,
        duration_mins=int(duration),
        priority=priority
    )

    # 2. Check for conflicts using your Phase 4 algorithm
    if st.session_state.scheduler.check_conflicts(new_task):
        st.warning(f"⚠️ Schedule Conflict: '{task_title}' overlaps with another task!")
    
    # 3. Save to the Brain
    st.session_state.scheduler.pets[0].add_task(new_task)
    st.success(f"Added '{task_title}' at {formatted_time}!")

st.divider()

# --- Results Section ---
st.subheader("Final Schedule")
if st.button("Generate Optimized Plan"):
    scheduler = st.session_state.scheduler
    upcoming_tasks = scheduler.get_upcoming_tasks()
    
    if not upcoming_tasks:
        st.info("No tasks scheduled yet.")
    else:
        st.subheader("🗓️ Today's Optimized Care Plan")
        
        formatted_schedule = []
        for pet_name, task in upcoming_tasks:
            formatted_schedule.append({
                "Time": task.due_time,
                "Pet": pet_name,
                "Task": task.description,
                "Priority": task.priority,
                "Duration": f"{task.duration_mins} mins"
            })
        
        st.table(formatted_schedule)
        st.success("Tasks have been sorted chronologically!")