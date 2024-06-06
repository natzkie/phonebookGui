import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import os

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Phone Book Login")

        # Calculate the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the x and y coordinates to display the window at the center
        x_coordinate = (screen_width - 800) // 2
        y_coordinate = (screen_height - 600) // 2

        # Set the window geometry
        self.root.geometry(f"800x600+{x_coordinate}+{y_coordinate}")

        # Frame
        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.pack(pady=100, padx=100)

        # Header
        self.header_label = tk.Label(self.frame, text="Login", bg="#f0f0f0", font=("Helvetica", 24))
        self.header_label.grid(row=0, columnspan=2, padx=10, pady=10)

        # Username label and entry
        self.username_label = tk.Label(self.frame, text="Username", bg="#f0f0f0", font=("Helvetica", 12))
        self.username_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = tk.Entry(self.frame, width=30, font=("Helvetica", 12))
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        # Password label and entry
        self.password_label = tk.Label(self.frame, text="Password", bg="#f0f0f0", font=("Helvetica", 12))
        self.password_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = tk.Entry(self.frame, width=30, show="*", font=("Helvetica", 12))
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Save Password checkbox
        self.save_password_var = tk.BooleanVar()
        self.save_password_var.trace_add('write', self.toggle_save_password)
        self.save_password_check = tk.Checkbutton(self.frame, text="Save Password", variable=self.save_password_var, bg="#f0f0f0", font=("Helvetica", 12))
        self.save_password_check.grid(row=3, columnspan=2, padx=10, pady=5)

        # Login button
        self.login_button = tk.Button(self.frame, text="Login", width=20, bg="#007bff", fg="#ffffff", font=("Helvetica", 12), command=self.login)
        self.login_button.grid(row=4, columnspan=2, pady=10)

        # Register button
        self.register_button = tk.Button(self.frame, text="Register", width=20, bg="#007bff", fg="#ffffff", font=("Helvetica", 12), command=self.open_register)
        self.register_button.grid(row=5, columnspan=2)

        # Bind <Return> key to the login function
        self.root.bind("<Return>", lambda event: self.login())

        # Override the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Load saved password
        self.load_saved_password()
        

    def get_db_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="phonebook"
        )

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Input Error", "Please enter both username and password.")
            return

        if self.save_password_var.get():
            self.save_password(username, password)
        else:
            self.remove_saved_password()

        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.root.withdraw()  # Hide the login window
            self.open_home_window(user[0])  # Open the phone book window with user ID
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def open_register(self):
        self.root.withdraw()  # Hide the login window
        subprocess.Popen(['python', 'register.py'])  # Open the register window

    def open_home_window(self, user_id):
        home_process = subprocess.Popen(['python', 'home.py', str(user_id)])
        home_process.wait()  # Wait for the home window to close
        self.root.deiconify()  # Bring the login window back to front

    def save_password(self, username, password):
        with open("saved_password.txt", "w") as f:
            f.write(f"{username}:{password}")

    def load_saved_password(self):
        try:
            with open("saved_password.txt", "r") as f:
                saved_data = f.read().strip().split(":")
                if len(saved_data) == 2:
                    username, password = saved_data
                    self.username_entry.insert(0, username)
                    self.password_entry.insert(0, password)
                    self.save_password_var.set(True)
        except FileNotFoundError:
            pass

    def remove_saved_password(self):
        try:
            os.remove("saved_password.txt")
        except FileNotFoundError:
            pass

    def toggle_save_password(self, *args):
        if not self.save_password_var.get():
            self.remove_saved_password()

    def on_closing(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginSystem(root)
    root.mainloop()
