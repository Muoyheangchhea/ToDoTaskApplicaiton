import streamlit as st
from datetime import datetime

class Node:
    def __init__(self, data, due_date=None, priority=0, start_time=None, end_time=None):
        self.data = data
        self.due_date = due_date
        self.priority = priority
        self.start_time = start_time
        self.end_time = end_time
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_task(self, task, due_date=None, priority=0, start_time=None, end_time=None):
        new_node = Node(task, due_date, priority, start_time, end_time)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def remove_task(self, task_number):
        current = self.head
        previous = None
        task_counter = 1
        while current is not None:
            if task_counter == task_number:
                if previous is not None:
                    previous.next = current.next
                else:
                    self.head = current.next
                return True
            previous = current
            current = current.next
            task_counter += 1
        return False

    def edit_task(self, task_number, field_to_edit, new_value):
        current = self.head
        task_counter = 1
        while current is not None:
            if task_counter == task_number:
                if field_to_edit == "Task":
                    current.data = new_value
                elif field_to_edit == "Due Date":
                    current.due_date = new_value
                elif field_to_edit == "Priority":
                    current.priority = {"Low": 0, "Medium": 1, "High": 2}[new_value]
                elif field_to_edit == "Start Time":
                    current.start_time = new_value
                elif field_to_edit == "End Time":
                    current.end_time = new_value
                return True
            current = current.next
            task_counter += 1
        return False

    def clear_tasks(self):
        self.head = None

    def display_tasks(self):
        tasks = []
        current = self.head
        while current is not None:
            task_info = {
                "data": current.data,
                "due_date": current.due_date,
                "priority": current.priority,
                "start_time": current.start_time,
                "end_time": current.end_time
            }
            tasks.append(task_info)
            current = current.next
        return tasks

def main():
    st.title("To-Do List App with Linked List")
    
    today = datetime.now().date()
    st.write(f"**Today's Date:** {today.strftime('%B %d, %Y')}")

    if "tasks_list" not in st.session_state:
        st.session_state.tasks_list = LinkedList()
    tasks_list = st.session_state.tasks_list

    st.sidebar.write("**Adding Task Section**")
    task_input = st.sidebar.text_input("Add Task:")
    due_date_input = st.sidebar.date_input("Due Date (optional):", value=None)
    priority_input = st.sidebar.selectbox("Priority:", ["Low", "Medium", "High"], index=0)
    start_time_input = st.sidebar.time_input("Start Time (optional):", value=None)
    end_time_input = st.sidebar.time_input("Finish Time (optional):", value=None)

    if st.sidebar.button("Add") and task_input:
        priority_level = {"Low": 0, "Medium": 1, "High": 2}[priority_input]
        tasks_list.add_task(task_input, due_date_input, priority_level, start_time_input, end_time_input)
        st.sidebar.success(f"Task '{task_input}' has been added successfully.", icon='✅')


    st.sidebar.write("**Removing Task Section**")
    task_to_remove_number = st.sidebar.number_input("Remove Task Number:", min_value=1, value=1)
    if st.sidebar.button("Remove"):
        if tasks_list.remove_task(task_to_remove_number):
            st.sidebar.success(f"Task number {task_to_remove_number} has been removed successfully.", icon='✅')
        else:
            st.sidebar.error(f"Task number {task_to_remove_number} is not found.", icon='❌')

    st.sidebar.write("**Editing Task Section**")
    task_to_edit_number = st.sidebar.number_input("Edit Task Number:", min_value=1, value=1)
    field_to_edit = st.sidebar.selectbox("Select Field to Edit:", ["Task", "Due Date", "Priority", "Start Time", "End Time"])

    if field_to_edit == "Task":
        edit_value = st.sidebar.text_input("Enter New Task:")
    elif field_to_edit == "Due Date":
        edit_value = st.sidebar.date_input("Enter New Due Date:", value=None)
    elif field_to_edit == "Priority":
        edit_value = st.sidebar.selectbox("Enter New Priority:", ["Low", "Medium", "High"], index=0)
    elif field_to_edit == "Start Time":
        edit_value = st.sidebar.time_input("Enter New Start Time:", value=None)
    elif field_to_edit == "Finish Time":
        edit_value = st.sidebar.time_input("Enter New Finish Time:", value=None)

    if st.sidebar.button("Edit"):
        if tasks_list.edit_task(task_to_edit_number, field_to_edit, edit_value):
            st.sidebar.success(f"Task number {task_to_edit_number} has been edited successfully.", icon='✅')
        else:
            st.sidebar.error(f"Task number {task_to_edit_number} is not found.", icon='❌')

    st.sidebar.write("**Clear All Task Section**")
    if st.sidebar.button("Clear All"):
        tasks_list.clear_tasks()
        st.sidebar.success("All tasks have been cleared.", icon='✅')

    st.write("## My To-Do List:")
    tasks = tasks_list.display_tasks()
    st.markdown("*Stay Focused & Be Productive* - :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")
    if not tasks:
        st.write("No tasks yet. Add some tasks using the sidebar!")
    else:
        tasks.sort(key=lambda x: (x["priority"], x["due_date"]), reverse=True)
        for i, task in enumerate(tasks, start=1):
            due_date_str = task["due_date"].strftime("%Y-%m-%d") if task["due_date"] else "No due date"
            priority_str = ["Low", "Medium", "High"][task["priority"]]
            start_time_str = task["start_time"].strftime("%H:%M") if task["start_time"] else "No start time"
            end_time_str = task["end_time"].strftime("%H:%M") if task["end_time"] else "No finish time"
            st.write(f"{i}. **{task['data'].capitalize()}** \n\n -Due: {due_date_str}\n\n -Priority: {priority_str}\n\n -Start: {start_time_str} ~ End: {end_time_str}")

if __name__ == "__main__":
    main()