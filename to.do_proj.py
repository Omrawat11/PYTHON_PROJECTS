import streamlit as st

st.title("📝 Task Management App")

# Initialize task list in session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ---- ADD TASK ----
st.subheader("Add a Task")
new_task = st.text_input("Enter a new task")

if st.button("Add Task"):
    if new_task:
        st.session_state.tasks.append(new_task)
        st.success(f"Task '{new_task}' added successfully!")
    else:
        st.warning("Please enter a task")

# ---- UPDATE TASK ----
st.subheader("Update a Task")
task_to_update = st.selectbox("Select task to update", st.session_state.tasks)

updated_task = st.text_input("Enter updated task")

if st.button("Update Task"):
    if updated_task:
        index = st.session_state.tasks.index(task_to_update)
        st.session_state.tasks[index] = updated_task
        st.success("Task updated successfully!")
    else:
        st.warning("Please enter updated task")

# ---- DELETE TASK ----
st.subheader("Delete a Task")
task_to_delete = st.selectbox("Select task to delete", st.session_state.tasks)

if st.button("Delete Task"):
    st.session_state.tasks.remove(task_to_delete)
    st.success(f"Task '{task_to_delete}' deleted successfully!")

# ---- VIEW TASKS ----
st.subheader("Your Tasks")
if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks, start=1):
        st.write(f"{i}. {task}")
else:
    st.info("No tasks added yet")