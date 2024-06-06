import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import mysql.connector
import os

class Home:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Home")

        # Calculate the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the x and y coordinates to display the window at the center
        x_coordinate = (screen_width - 700) // 2
        y_coordinate = (screen_height - 800) // 2

        # Set the window geometry
        self.root.geometry(f"700x800+{x_coordinate}+{y_coordinate}")

        # Frame
        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.pack(pady=100, padx=100)

        # Get the username from the database
        self.username = self.get_username()

        # Welcome message
        self.welcome_label = tk.Label(self.frame, text=f"Welcome, {self.username}!", bg="#f0f0f0", font=("Helvetica", 24))
        self.welcome_label.grid(row=0, columnspan=2, padx=10, pady=10)

        # Phonebook button
        self.phonebook_button = tk.Button(self.frame, text="Phonebook", width=35, bg="#007bff", fg="#ffffff", font=("Helvetica", 12), command=self.open_phonebook)
        self.phonebook_button.grid(row=1, columnspan=2, pady=10)

        # Phone log button
        self.phone_log_button = tk.Button(self.frame, text="Phone Log", width=35, bg="#007bff", fg="#ffffff", font=("Helvetica", 12), command=self.open_phone_log)
        self.phone_log_button.grid(row=2, columnspan=2, pady=10)
        
        # Address button
        self.address_button = tk.Button(self.frame, text="Gui Address", width=35, bg="#007bff", fg="#ffffff", font=("Helvetica", 12), command=self.open_gui_address)
        self.address_button.grid(row=3, columnspan=2, pady=10)
        
        # Relationship button
        self.relationship_button = tk.Button(self.frame, text="Gui Relationship", width=35, bg="#007bff", fg="#ffffff", font=("Helvetica", 12), command=self.open_gui_relationship)
        self.relationship_button.grid(row=4, columnspan=2, pady=10)

        # Logout button
        self.logout_button = tk.Button(self.frame, text="Logout", width=35, bg="#dc3545", fg="#ffffff", font=("Helvetica", 12), command=self.logout)
        self.logout_button.grid(row=5, columnspan=2, pady=10)

        # Store references to subprocesses
        self.subprocesses = []

    def get_db_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="phonebook"
        )

    def get_username(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id = %s", (self.user_id,))
        username = cursor.fetchone()[0]
        conn.close()
        return username

    def open_phonebook(self):
        process = subprocess.Popen(['python', 'main.py', str(self.user_id)])
        self.subprocesses.append(process)

    def open_phone_log(self):
        process = subprocess.Popen(['python', 'logs.py', str(self.user_id)])
        self.subprocesses.append(process)
        
    def open_gui_address(self):
        process = subprocess.Popen(['python', 'gui_address.py', str(self.user_id)])
        self.subprocesses.append(process)
        
    def open_gui_relationship(self):
        process = subprocess.Popen(['python', 'gui_relationship.py', str(self.user_id)])
        self.subprocesses.append(process)

    def logout(self):
        self.root.destroy()
        for process in self.subprocesses:
            process.terminate()
        subprocess.run(['python', 'login.py'])

    def on_close(self):
        self.logout()

if __name__ == "__main__":
    root = tk.Tk()
    app = Home(root, int(sys.argv[1]))
    root.mainloop()
