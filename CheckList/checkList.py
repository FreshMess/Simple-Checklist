import tkinter as tk
from tkinter import messagebox
import time
import threading

class ChecklistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Checklist App")
        self.root.geometry("800x600")

        self.tasks = []
        self.repeating_tasks = []
        self.add_repeating_task = False

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.title_label = tk.Label(self.frame, text="Checklist", font=("Helvetica", 16))
        self.title_label.pack()

        self.task_frame = tk.Frame(self.frame)
        self.task_frame.pack()

        self.load_tasks()

        self.task_entry = tk.Entry(self.frame, width=25)
        self.task_entry.pack(pady=5)
        self.task_entry.bind('<Return>', lambda event: self.add_task(event))
        self.task_entry.bind('<Shift-Return>', lambda event: self.add_repeating_task_command(event))

        self.add_task_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.add_repeating_task_button = tk.Button(self.frame, text="Add Repeating Task", command=self.add_repeating_task_command)
        self.add_repeating_task_button.pack(pady=5)

        self.save_button = tk.Button(self.frame, text="Save Tasks", command=self.save_tasks)
        self.save_button.pack(pady=5)

        self.load_button = tk.Button(self.frame, text="Load Tasks", command=self.load_tasks)
        self.load_button.pack(pady=5)

        self.about_label = tk.Label(self.root, text="Simple Checklist App. Made by FreshMess aka DouglasB", font=("Helvetica", 10))
        self.about_label.pack(side='bottom', pady=10)

        self.set_alarms()

    def add_task(self, event=None):
        task_text = self.task_entry.get()
        if task_text != "":
            if self.add_repeating_task:
                self.repeating_tasks.append(task_text)
            else:
                self.tasks.append(task_text)
            self.task_entry.delete(0, tk.END)
            self.update_tasks()
            self.add_repeating_task = False

    def update_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        for task in self.tasks:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.task_frame, text=task, variable=var, command=lambda t=task: self.remove_task(t))
            chk.pack(anchor='w')

        for task in self.repeating_tasks:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.task_frame, text=f"{task} (Repeating)", variable=var, fg='blue', command=lambda t=task: self.remove_task(t))
            chk.pack(anchor='w')

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
        if task in self.repeating_tasks:
            self.repeating_tasks.remove(task)
        self.update_tasks()

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(f"{task}\n")
        with open("repeating_tasks.txt", "w") as file:
            for task in self.repeating_tasks:
                file.write(f"{task}\n")
        messagebox.showinfo("Info", "Tasks saved successfully.")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                self.tasks = file.read().splitlines()
            with open("repeating_tasks.txt", "r") as file:
                self.repeating_tasks = file.read().splitlines()
            self.update_tasks()
        except FileNotFoundError:
            pass

    def set_alarms(self):
        def check_tasks():
            while True:
                current_time = time.localtime()
                if current_time.tm_hour == 0 and current_time.tm_min == 0:  # Midnight check
                    self.repeating_tasks.clear() 
                    self.update_tasks()
                
                incomplete_tasks = [task for task in self.tasks]
                if incomplete_tasks:
                    messagebox.showwarning("Warning", "You have incomplete tasks!")
                
                time.sleep(30 * 60) # Checks for incompletes every thirty minutes

        alarm_thread = threading.Thread(target=check_tasks)
        alarm_thread.daemon = True
        alarm_thread.start()

    def add_repeating_task_command(self, event=None):
        self.add_repeating_task = True
        self.add_task()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChecklistApp(root)
    root.mainloop()
