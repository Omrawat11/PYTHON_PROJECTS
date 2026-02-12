

import streamlit as st

st.title("📝 Task Management App")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ---------------- ADD TASKS ----------------
st.subheader("Add Tasks")

num_tasks = st.number_input("How many tasks do you want to add?", min_value=0, step=1)

new_tasks = []

for i in range(int(num_tasks)):
    task = st.text_input(f"Enter Task {i+1}", key=f"add_{i}")
    new_tasks.append(task)

if st.button("Add Tasks"):
    for task in new_tasks:
        if task:
            st.session_state.tasks.append(task)
    st.success("Tasks added successfully!")

# ---------------- UPDATE TASKS ----------------
st.subheader("Update Tasks")

if st.session_state.tasks:

    num_update = st.number_input("How many tasks do you want to update?", min_value=0, step=1)

    for i in range(int(num_update)):
        task_to_update = st.selectbox(
            f"Select task to update {i+1}",
            st.session_state.tasks,
            key=f"update_select_{i}"
        )

        updated_task = st.text_input(
            f"Enter updated value for task {i+1}",
            key=f"update_text_{i}"
        )

        if st.button(f"Update Task {i+1}", key=f"update_btn_{i}"):
            index = st.session_state.tasks.index(task_to_update)
            st.session_state.tasks[index] = updated_task
            st.success("Task updated!")

# ---------------- VIEW TASKS ----------------
st.subheader("View Tasks")

if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks, start=1):
        st.write(f"{i}. {task}")
else:
    st.info("No tasks added yet")

# ---------------- DELETE TASK ----------------
st.subheader("Delete Task")

if st.session_state.tasks:
    task_to_delete = st.selectbox("Select task to delete", st.session_state.tasks)

    if st.button("Delete Selected Task"):
        st.session_state.tasks.remove(task_to_delete)
        st.success("Task deleted successfully!")
