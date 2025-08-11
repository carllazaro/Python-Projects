import tkinter as tk
from tkinter import *
from tkinter import messagebox
import re
import random
import datetime
import os
import platform
import time

# -- Constants and Data --

MOVIES = ["Fight Club", "Finding Nemo", "Oppenheimer"]
CITIES = ["Los Angeles", "Visakhapatnam", "New York City", "Mumbai", "Toronto", "Atlanta", "Berlin", "Las Vegas", "Manila"]
THEATERS = ["IMDb", "IMAX", "4DX"]

START_DATE = datetime.date(2025, 8, 1)
END_DATE = datetime.date(2025, 12, 1)
DAYS_BETWEEN = (END_DATE - START_DATE).days
RANDOM_DATE = START_DATE + datetime.timedelta(days=random.randrange(DAYS_BETWEEN))

# -- Helper Functions --

def get_environment_info():
    return {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Python Version": platform.python_version(),
        "Architecture": platform.machine(),
        "Current Working Directory": os.getcwd(),
        "Platform": os.name,
    }

def check_credentials(username, password):
    if not os.path.exists("database.txt"):
        return False
    with open("database.txt", "r") as file:
        lines = file.readlines()[2:]  # skip header lines
    for line in lines:
        if "|" not in line:
            continue
        stored_user, stored_pass = re.split(r'\s*\|\s*', line.strip())
        if username == stored_user and password == stored_pass:
            return True
    return False

def register_account(username, password):
    special_chars = r"!@#$%^&*()-_+=\{\}[\]|\\:;\"'<>,.?/`~"
    numbers = r"0123456789"

    # Validate username and password
    if not re.search(f"[{re.escape(special_chars)}]", username):
        return False, "Username must contain at least one special character."
    if not re.search(f"[{re.escape(numbers)}]", username):
        return False, "Username must contain at least one number."
    if not re.search(f"[{re.escape(special_chars)}]", password):
        return False, "Password must contain at least one special character."
    if not re.search(f"[{re.escape(numbers)}]", password):
        return False, "Password must contain at least one number."

    file_exists = os.path.exists("database.txt")
    is_empty = os.path.getsize("database.txt") == 0 if file_exists else True
    with open("database.txt", "a") as file:
        if is_empty:
            file.write("REGISTERED ACCOUNTS\n")
            file.write("----------------------------------------\n")
        file.write(f"{username}   |   {password}\n")
    return True, "Account registered successfully!"

# -- Tkinter Application --
class CinemaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cinema Reservation System")
        self.geometry("400x600")
        icon = tk.PhotoImage(file = "C:\Python\Cinema Reservation with GUI\Popcorn.png")
        self.iconphoto(True, icon)
        self.configure(bg="#121212")
        self.resizable(False, False)

        # Container to hold frames
        container = tk.Frame(self, bg="#121212")
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (LoginPage, RegisterPage, DashboardPage, TicketReservationPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# --- Login Page ---

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        tk.Label(self, text=" Cinema Reservation Login", font=("Arial", 24), fg="white", bg="#121212").pack(pady=20)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(self, text="Username:", fg="white", bg="#121212").pack(pady=(10,0))
        self.username_entry = tk.Entry(self, textvariable=self.username_var, font=("Arial", 14))
        self.username_entry.pack()

        tk.Label(self, text="Password:", fg="white", bg="#121212").pack(pady=(10,0))
        self.password_entry = tk.Entry(self, textvariable=self.password_var, font=("Arial", 14), show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", font=("Arial", 14), bg="#2196f3", fg="white", command=self.login).pack(pady=20)
        tk.Button(self, text="Register", font=("Arial", 12), bg="#424242", fg="white", command=lambda: controller.show_frame(RegisterPage)).pack()

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        if check_credentials(username, password):
            messagebox.showinfo("Success", f"Welcome, @{username}!")
            self.controller.frames[DashboardPage].set_user(username)
            self.controller.show_frame(DashboardPage)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

# --- Register Page ---

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        tk.Label(self, text="Register Account", font=("Arial", 24), fg="white", bg="#121212").pack(pady=20)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(self, text="Username:", fg="white", bg="#121212").pack(pady=(10,0))
        self.username_entry = tk.Entry(self, textvariable=self.username_var, font=("Arial", 14))
        self.username_entry.pack()

        tk.Label(self, text="Password:", fg="white", bg="#121212").pack(pady=(10,0))
        self.password_entry = tk.Entry(self, textvariable=self.password_var, font=("Arial", 14), show="*")
        self.password_entry.pack()

        tk.Button(self, text="Register", font=("Arial", 14), bg="#4caf50", fg="white", command=self.register).pack(pady=20)
        tk.Button(self, text="Back to Login", font=("Arial", 12), bg="#424242", fg="white", command=lambda: controller.show_frame(LoginPage)).pack()

    def register(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        success, msg = register_account(username, password)
        if success:
            messagebox.showinfo("Success", msg)
            self.controller.show_frame(LoginPage)
        else:
            messagebox.showerror("Error", msg)

# --- Dashboard Page ---

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller
        self.username = ""

        self.info_label = tk.Label(self, text="", font=("Arial", 16), fg="white", bg="#121212")
        self.info_label.pack(pady=10)

        self.details_label = tk.Label(self, text="", font=("Arial", 14), fg="white", bg="#121212")
        self.details_label.pack(pady=10)

        btn_frame = tk.Frame(self, bg="#121212")
        btn_frame.pack(pady=20)

        btn_specs = [
            ("Reserve a Ticket", lambda: controller.show_frame(TicketReservationPage)),
            ("Movies", self.show_movies),
            ("Theaters", self.show_theaters),
            ("Trailers", self.show_trailers),
            ("Events & Promos", self.show_events),
            ("Logout", self.logout)
        ]

        for (text, cmd) in btn_specs:
            b = tk.Button(btn_frame, text=text, font=("Arial", 14), width=18, bg="#333", fg="white",
                          activebackground="#555", activeforeground="white", command=cmd)
            b.pack(pady=5)

    def set_user(self, username):
        self.username = username
        self.update_info()

    def update_info(self):
        random_showcase = random.randint(0, 2)
        random_city = random.choice(CITIES)
        random_theater = random.choice(THEATERS)
        date_str = RANDOM_DATE.strftime("%B %d, %Y")

        movie = MOVIES[random_showcase]
        self.info_label.config(text=f"Welcome @{self.username}\nMovie: {movie}")
        self.details_label.config(text=f"Theater: {random_theater}\nCity: {random_city}\nDate: {date_str}")

    def show_movies(self):
        messagebox.showinfo("Movies", "\n".join(MOVIES))

    def show_theaters(self):
        messagebox.showinfo("Theaters", "\n".join(THEATERS))

    def show_trailers(self):
        messagebox.showinfo("Trailers", "Trailers section coming soon!")

    def show_events(self):
        messagebox.showinfo("Events & Promos", "Events & Promos coming soon!")

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.controller.show_frame(LoginPage)

# --- Ticket Reservation Page ---
class TicketReservationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        tk.Label(self, text="Ticket Reservation", font=("Arial", 24), fg="white", bg="#121212").pack(pady=10)

        self.seat_frame = tk.Frame(self, bg="#121212")
        self.seat_frame.pack(pady=10)

        self.theater_var = tk.StringVar()
        self.theater_frame = tk.Frame(self, bg="#121212")
        self.theater_frame.pack(pady=10)

        self.back_button = tk.Button(self, text="Back to Dashboard", font=("Arial", 12), bg="#333", fg="white",
                                     command=lambda: controller.show_frame(DashboardPage))
        self.back_button.pack(pady=10)

        self.rows = 5
        self.cols = 6

        # 0 = available, 1 = reserved, 2 = selected by user
        self.seat_states = [[0]*self.cols for _ in range(self.rows)]

        # Randomly reserve 6-10 seats
        reserved_count = random.randint(6, 10)
        reserved_positions = set()
        while len(reserved_positions) < reserved_count:
            r = random.randint(0, self.rows-1)
            c = random.randint(0, self.cols-1)
            reserved_positions.add((r, c))
        for (r,c) in reserved_positions:
            self.seat_states[r][c] = 1

        self.selected_seat = None

        self.setup_seats()
        self.setup_theaters()

    def setup_seats(self):
        for widget in self.seat_frame.winfo_children():
            widget.destroy()

        # Header
        tk.Label(self.seat_frame, text="Seats Layout", font=("Arial", 16), fg="white", bg="#121212").grid(row=0, column=0, columnspan=self.cols+1)

        for c in range(self.cols):
            tk.Label(self.seat_frame, text=f"C{c+1}", fg="white", bg="#121212", font=("Arial", 12)).grid(row=1, column=c+1, padx=5, pady=5)

        for r in range(self.rows):
            tk.Label(self.seat_frame, text=f"R{r+1}", fg="white", bg="#121212", font=("Arial", 12)).grid(row=r+2, column=0, padx=5, pady=5)
            for c in range(self.cols):
                color = "#4caf50"  # green = available
                if self.seat_states[r][c] == 1:
                    color = "#555454"  # grey = reserved
                elif self.seat_states[r][c] == 2:
                    color = "#ffeb3b"  # yellow = selected

                btn = tk.Button(self.seat_frame, text=f"{r+1}-{c+1}", width=4, bg=color, fg="black",
                                command=lambda rr=r, cc=c: self.select_seat(rr, cc))
                btn.grid(row=r+2, column=c+1, padx=2, pady=2)

    def setup_theaters(self):
        for widget in self.theater_frame.winfo_children():
            widget.destroy()

        tk.Label(self.theater_frame, text="Select Theater", font=("Arial", 16), fg="white", bg="#121212").pack(pady=5)

        self.available_theaters = {}
        for t in THEATERS:
            self.available_theaters[t] = random.choice([True, False])

        for theater in THEATERS:
            state = tk.NORMAL if self.available_theaters[theater] else tk.DISABLED
            rb = tk.Radiobutton(self.theater_frame, text=f"{theater} - {'Available' if self.available_theaters[theater] else 'Not Available'}",
                                variable=self.theater_var, value=theater, font=("Arial", 14),
                                fg="white", bg="#121212", selectcolor="#333", state=state)
            rb.pack(anchor='w')

    def select_seat(self, r, c):
        if self.seat_states[r][c] == 1:
            messagebox.showwarning("Seat Reserved", "This seat is already reserved!")
            return
        if self.seat_states[r][c] == 2:
            # Deselect seat
            self.seat_states[r][c] = 0
            self.selected_seat = None
        else:
            # Deselect previous
            if self.selected_seat is not None:
                pr, pc = self.selected_seat
                self.seat_states[pr][pc] = 0
            self.seat_states[r][c] = 2
            self.selected_seat = (r, c)
        self.setup_seats()

    def reserve_seat(self):
        if self.selected_seat is None:
            messagebox.showerror("No Seat Selected", "Please select a seat before reserving.")
            return
        if not self.theater_var.get():
            messagebox.showerror("No Theater Selected", "Please select a theater before reserving.")
            return

        r, c = self.selected_seat
        self.seat_states[r][c] = 1  # mark as reserved
        self.selected_seat = None
        messagebox.showinfo("Reserved", f"Seat {r+1}-{c+1} reserved at {self.theater_var.get()} theater!")
        self.setup_seats()

# -- Run Application --

if __name__ == "__main__":
    app = CinemaApp()
    app.mainloop()
