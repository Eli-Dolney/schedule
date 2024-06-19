import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
import itertools

class PCA_Scheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("PCA Scheduler")
        self.root.geometry("500x400")
        self.month = 1
        self.year = 2024
        self.worker_availability = {}
        self.schedules = []

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Month:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.month_entry = tk.Entry(self.root, width=5, font=("Helvetica", 12))
        self.month_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        tk.Label(self.root, text="Year:", font=("Helvetica", 12)).grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.year_entry = tk.Entry(self.root, width=10, font=("Helvetica", 12))
        self.year_entry.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        tk.Button(self.root, text="Set Month and Year", command=self.set_month_year, font=("Helvetica", 12)).grid(row=0, column=4, padx=10, pady=10)

        self.worker_availability_listbox = tk.Listbox(self.root, font=("Helvetica", 12), width=50, height=10)
        self.worker_availability_listbox.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

        tk.Button(self.root, text="Add Worker Availability", command=self.add_worker_availability, font=("Helvetica", 12)).grid(row=2, column=0, columnspan=5, pady=10)
        tk.Button(self.root, text="Generate Schedules", command=self.generate_schedules, font=("Helvetica", 12)).grid(row=3, column=0, columnspan=5, pady=10)

        self.schedule_buttons_frame = tk.Frame(self.root)
        self.schedule_buttons_frame.grid(row=4, column=0, columnspan=5)

    def set_month_year(self):
        self.month = int(self.month_entry.get())
        self.year = int(self.year_entry.get())

    def add_worker_availability(self):
        worker_name = simpledialog.askstring("Worker Name", "Enter worker name:")
        worker_availability = simpledialog.askstring("Worker Availability", "Enter available days (comma-separated or ranges):")
        self.worker_availability[worker_name] = self.parse_availability(worker_availability)
        self.update_worker_availability_listbox()

    def parse_availability(self, availability):
        days = set()
        for part in availability.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                days.update(range(start, end + 1))
            else:
                days.add(int(part))
        return sorted(days)

    def update_worker_availability_listbox(self):
        self.worker_availability_listbox.delete(0, tk.END)
        for worker, availability in self.worker_availability.items():
            self.worker_availability_listbox.insert(tk.END, f"{worker}: {', '.join(map(str, availability))}")

    def generate_schedules(self):
        num_schedules = simpledialog.askinteger("Number of Schedules", "Enter number of unique schedules to generate:")
        self.schedules = []

        all_days = list(range(1, 32))
        worker_permutations = list(itertools.permutations(self.worker_availability.keys(), len(self.worker_availability)))

        while len(self.schedules) < num_schedules and worker_permutations:
            random_perm = random.choice(worker_permutations)
            worker_permutations.remove(random_perm)

            schedule = {}
            available_workers = {worker: days[:] for worker, days in self.worker_availability.items()}

            for day in all_days:
                assigned_worker = None
                for worker in random_perm:
                    if day in available_workers[worker]:
                        assigned_worker = worker
                        available_workers[worker].remove(day)
                        break
                if assigned_worker:
                    schedule[day] = assigned_worker
                else:
                    schedule[day] = "No one available"

            if schedule not in self.schedules:
                self.schedules.append(schedule)
                self.display_schedule(schedule)

        if not self.schedules:
            messagebox.showerror("Error", "Could not generate unique schedules")

    def display_schedule(self, schedule):
        schedule_number = len(self.schedules)
        button = tk.Button(self.schedule_buttons_frame, text=f"Schedule {schedule_number}", command=lambda s=schedule: self.show_schedule(s), font=("Helvetica", 12))
        button.grid(row=schedule_number, column=0, pady=5)

    def show_schedule(self, schedule):
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title(f"Schedule {self.schedules.index(schedule) + 1}")
        
        canvas = tk.Canvas(schedule_window, width=800, height=600)
        canvas.pack()

        calendar_image = self.create_calendar_image(schedule)
        self.updated_calendar_image = ImageTk.PhotoImage(calendar_image)
        canvas.create_image(400, 300, image=self.updated_calendar_image)

    def create_calendar_image(self, schedule):
        image = Image.new("RGB", (800, 600), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_days = ImageFont.truetype("arial.ttf", 24)

        draw.text((400, 50), f"{self.month}/{self.year}", fill="black", anchor="mm", font=font_title)

        cell_width = 800 // 7
        cell_height = (600 - 100) // 5
        for day in range(1, 31):
            x = ((day - 1) % 7) * cell_width
            y = ((day - 1) // 7) * cell_height + 100
            draw.rectangle([x, y, x + cell_width, y + cell_height], outline="black")
            draw.text((x + 10, y + 10), str(day), fill="black", font=font_days)
            draw.text((x + 10, y + 40), schedule.get(day, ""), fill="black", font=font_days)

        return image

if __name__ == "__main__":
    root = tk.Tk()
    app = PCA_Scheduler(root)
    root.mainloop()
