import tkinter as tk
from tkinter import ttk
import mysql.connector
import sys

class PhoneLogsApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Phone Logs")

        # Create a Treeview widget to display the phone logs
        self.tree = ttk.Treeview(root, columns=("User ID", "Contact ID", "Action", "Timestamp"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("User ID", text="User ID")
        self.tree.heading("Contact ID", text="Contact ID")
        self.tree.heading("Action", text="Action")
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.pack(fill="both", expand=True)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Load phone logs for the current user from the database
        self.load_phone_logs()

    def get_db_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="phonebook"
        )

    def load_phone_logs(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        # Fetch phone logs for the current user
        cursor.execute("SELECT * FROM contact_logs WHERE user_id = %s", (self.user_id,))
        logs = cursor.fetchall()
        conn.close()

        for log in logs:
            self.tree.insert("", "end", text=log[0], values=log[1:])

    def on_closing(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhoneLogsApp(root, int(sys.argv[1]))  # Assuming user_id is passed as an argument
    root.mainloop()
