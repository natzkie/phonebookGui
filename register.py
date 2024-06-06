import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess

class RegisterSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        
        # Calculate the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the x and y coordinates to display the window at the center
        x_coordinate = (screen_width - 800) // 2  # Adjust 400 according to your window width
        y_coordinate = (screen_height - 500) // 2  # Adjust 300 according to your window height

        # Set the window geometry
        self.root.geometry(f"800x500+{x_coordinate}+{y_coordinate}")

        # Frame
        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.pack(pady=100, padx=0)


        # Header
        self.header_label = tk.Label(self.frame, text="Register", bg="#f0f0f0", font=("Helvetica", 24))
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

        # Register button
        self.register_button = tk.Button(self.frame, text="Register", width=20, bg="#007bff", fg="#ffffff", font=("Helvetica", 12), command=self.register)
        self.register_button.grid(row=3, columnspan=2, pady=10)

        # Login button
        self.login_button = tk.Button(self.frame, text="Back to Login", width=20, bg="#007bff", fg="#ffffff", font=("Helvetica", 12), command=self.open_login)
        self.login_button.grid(row=4, columnspan=2)

    def get_db_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="phonebook"
        )

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Input Error", "Please enter both username and password.")
            return

        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            conn.close()
            messagebox.showerror("Registration Error", "Username already exists.")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Registration Success", f"User {username} registered successfully!")
            self.root.destroy()
            subprocess.Popen(['python', 'login.py'])

    def open_login(self):
        self.root.destroy()
        subprocess.Popen(['python', 'login.py'])

if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterSystem(root)
    root.mainloop()