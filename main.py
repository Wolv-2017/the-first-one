import json
import tkinter as tk
from tkinter import messagebox, simpledialog

# Creates the class which displays the tasks decriptions 
class Task:
    def __init__(self, title, description, category):
        self.title = title
        self.description = description
        self.category = category
        self.completed = False

    def mark_completed(self):
        self.completed = True

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump([task.__dict__ for task in tasks], f)

def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return [Task(**data) for data in json.load(f)]
    except FileNotFoundError:
        return []

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal To-Do List Application")
        self.tasks = load_tasks()

        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=50, height=15)
        self.task_listbox.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.complete_button = tk.Button(root, text="Mark Completed", command=self.mark_completed)
        self.complete_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.view_button = tk.Button(root, text="View Tasks", command=self.view_tasks)
        self.view_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.pack(pady=5)

        self.view_tasks()  # Initial load of tasks

    def add_task(self):
        title = simpledialog.askstring("Input", "Enter task title:")
        description = simpledialog.askstring("Input", "Enter task description:")
        category = simpledialog.askstring("Input", "Enter task category (e.g., Work, Personal, Urgent):")
        
        if title and description and category:
            self.tasks.append(Task(title, description, category))
            self.view_tasks()
            messagebox.showinfo("Success", "Task added successfully!")
        else:
            messagebox.showwarning("Warning", "All fields are required!")

    def mark_completed(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks[selected_index[0]].mark_completed()
            self.view_tasks()
            messagebox.showinfo("Success", "Task marked as completed.")
        else:
            messagebox.showwarning("Warning", "Select a task to mark as completed.")

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks.pop(selected_index[0])
            self.view_tasks()
            messagebox.showinfo("Success", "Task deleted.")
        else:
            messagebox.showwarning("Warning", "Select a task to delete.")

    def view_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✔️" if task.completed else "❌"
            self.task_listbox.insert(tk.END, f"{status} {task.title} - {task.description} ({task.category})")

    def exit_app(self):
        save_tasks(self.tasks)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
