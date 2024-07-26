import tkinter as tk
from tkinter import ttk
import asyncio
from task import Task
from styles import setup_styles
from config import CONFIG
from aiodatabase import Database as AioDatabase
from typing import List

class TodoApp:
    def __init__(self, master: tk.Tk) -> None:
        """
        Initialize the TodoApp with the given Tkinter master widget.
        """
        self.master = master
        self.master.title(CONFIG['app_title'])
        self.master.geometry(CONFIG['window_size'])
        self.master.configure(bg=CONFIG['bg_color'])

        self.db = AioDatabase()
        
        setup_styles()
        self.create_widgets()
        self.tasks: List[Task] = []

    async def initialize_db(self) -> None:
        """
        Initialize the database connection and load existing tasks.
        """
        await self.db.connect("data/config.yml", "data/queries.sql")
        await self.load_tasks()

    async def load_tasks(self) -> None:
        """
        Load tasks from the database and update the task list.
        """
        results = await self.db.fetchall("get_all_tasks")
        self.tasks = [
            Task(result[1], result[2], result[3] == 1, result[4], result[0])
            for result in results
        ]
        self.update_list()

    def create_widgets(self) -> None:
        """
        Create the main application widgets.
        """
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.create_input_area()
        self.create_task_list()

    def create_input_area(self) -> None:
        """
        Create the input area for adding new tasks.
        """
        input_frame = ttk.Frame(self.frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.task_input = ttk.Entry(input_frame, font=CONFIG['input_font'])
        self.task_input.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.task_input.insert(0, CONFIG['input_placeholder'])
        self.task_input.bind("<FocusIn>", self.clear_placeholder)
        self.task_input.bind("<FocusOut>", self.restore_placeholder)
        self.task_input.bind("<Return>", self.add_task_event)

        self.add_button = ttk.Button(input_frame, text="Add", command=self.add_task_event, width=8)
        self.add_button.pack(side=tk.RIGHT, padx=(5, 0))

    def create_task_list(self) -> None:
        """
        Create the task list area with a scrollable canvas.
        """
        self.task_frame = ttk.Frame(self.frame)
        self.task_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.task_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.task_frame, bg=CONFIG['bg_color'], highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def on_frame_configure(self, event: tk.Event) -> None:
        """
        Update the scroll region of the canvas when the inner frame is resized.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event: tk.Event) -> None:
        """
        Adjust the width of the canvas frame to match the canvas width.
        """
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def clear_placeholder(self, event: tk.Event) -> None:
        """
        Clear the placeholder text when the input field gains focus.
        """
        if self.task_input.get() == CONFIG['input_placeholder']:
            self.task_input.delete(0, tk.END)

    def restore_placeholder(self, event: tk.Event) -> None:
        """
        Restore the placeholder text if the input field is empty when it loses focus.
        """
        if not self.task_input.get():
            self.task_input.insert(0, CONFIG['input_placeholder'])

    def add_task_event(self, event: tk.Event = None) -> None:
        """
        Trigger the addition of a new task asynchronously.
        """
        asyncio.create_task(self.add_task_async())

    async def add_task_async(self) -> None:
        """
        Add a new task to the database and update the task list.
        """
        task_text = self.task_input.get()
        if task_text and task_text != CONFIG['input_placeholder']:
            new_task = Task(task_text)
            result = await self.db.execute("add_task", (new_task.text, new_task.status, new_task.done, new_task.date))
            new_task.id = result
            self.tasks.append(new_task)
            self.update_list()
            self.task_input.delete(0, tk.END)
            self.restore_placeholder(None)

    def toggle_done_event(self, task: Task) -> None:
        """
        Trigger the toggling of a task's done status asynchronously.
        """
        asyncio.create_task(self.toggle_done_async(task))

    async def toggle_done_async(self, task: Task) -> None:
        """
        Toggle a task's done status and update the database.
        """
        task.toggle_done()
        await self.db.execute("update_task", (task.status, task.done, task.id))
        self.update_list()

    def remove_task_event(self, task: Task) -> None:
        """
        Trigger the removal of a task asynchronously.
        """
        asyncio.create_task(self.remove_task_async(task))

    async def remove_task_async(self, task: Task) -> None:
        """
        Remove a task from the database and update the task list.
        """
        await self.db.execute("remove_task", (task.id,))
        self.tasks.remove(task)
        self.update_list()

    def update_list(self) -> None:
        """
        Update the task list UI with the current tasks.
        """
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        for task in self.tasks:
            task_frame = ttk.Frame(self.inner_frame, style="TFrame")
            task_frame.pack(fill=tk.X, pady=(0, 5))

            check_var = tk.BooleanVar(value=task.done)
            check = ttk.Checkbutton(
                task_frame,
                variable=check_var,
                command=lambda t=task: self.toggle_done_event(t),
                style="Done.TCheckbutton"
            )
            check.pack(side=tk.LEFT)

            status_style = "Done.TLabel" if task.done else "New.TLabel"
            status_label = ttk.Label(task_frame, text=task.status, style=status_style)
            status_label.pack(side=tk.LEFT, padx=(0, 5))

            task_text = task.text if not task.done else f"\u0336{task.text}\u0336"  # Strikethrough if done
            text_label = ttk.Label(task_frame, text=task_text, foreground="white" if not task.done else "gray")
            text_label.pack(side=tk.LEFT, expand=True, anchor="w")

            date_label = ttk.Label(task_frame, text=task.date, foreground="gray")
            date_label.pack(side=tk.LEFT, padx=(0, 5))

            remove_button = ttk.Button(
                task_frame,
                text="×",
                command=lambda t=task: self.remove_task_event(t),
                style="Remove.TButton",
                width=3
            )
            remove_button.pack(side=tk.RIGHT)

        self.master.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    async def close_db(self) -> None:
        """
        Close the database connection.
        """
        await self.db.close()
