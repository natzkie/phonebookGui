import tkinter as tk
from tkinter import messagebox
import mysql.connector
import sys

class RelationshipStatusApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Relationship Status Management")

        # Create labels and entry fields
        tk.Label(root, text="Relationship Status:").grid(row=0, column=0, padx=5, pady=5)
        self.status_entry = tk.Entry(root)
        self.status_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create buttons
        self.add_button = tk.Button(root, text="Add", command=self.add_status)
        self.add_button.grid(row=1, column=0, padx=5, pady=5)
        self.update_button = tk.Button(root, text="Update", command=self.update_status)
        self.update_button.grid(row=1, column=1, padx=5, pady=5)
        self.delete_button = tk.Button(root, text="Delete", command=self.delete_status)
        self.delete_button.grid(row=1, column=2, padx=5, pady=5)

        # Create listbox to display relationship statuses
        self.status_listbox = tk.Listbox(root)
        self.status_listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # Populate listbox with existing relationship statuses
        self.populate_status_listbox()

    def populate_status_listbox(self):
        self.status_listbox.delete(0, tk.END)
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="phonebook"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM relationship_statuses WHERE user_id = %s", (self.user_id,))
            statuses = cursor.fetchall()
            for status in statuses:
                self.status_listbox.insert(tk.END, status[1])
            connection.close()
        except mysql.connector.Error as error:
            print("Error fetching relationship statuses:", error)

    def add_status(self):
        status = self.status_entry.get()
        if status:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="phonebook"
                )
                cursor = connection.cursor()
                cursor.execute("INSERT INTO relationship_statuses (status, user_id) VALUES (%s, %s)", (status, self.user_id))
                connection.commit()
                connection.close()
                self.status_entry.delete(0, tk.END)
                self.populate_status_listbox()
            except mysql.connector.Error as error:
                print("Error adding relationship status:", error)
        else:
            messagebox.showerror("Error", "Please enter a relationship status.")

    def update_status(self):
        selected_index = self.status_listbox.curselection()
        if selected_index:
            new_status = self.status_entry.get()
            if new_status:
                try:
                    connection = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="phonebook"
                    )
                    cursor = connection.cursor()
                    cursor.execute("UPDATE relationship_statuses SET status = %s WHERE id = %s AND user_id = %s",
                                   (new_status, selected_index[0] + 1, self.user_id))  # Index in list starts from 0, id starts from 1
                    connection.commit()
                    connection.close()
                    self.populate_status_listbox()
                except mysql.connector.Error as error:
                    print("Error updating relationship status:", error)
            else:
                messagebox.showerror("Error", "Please enter a new relationship status.")
        else:
            messagebox.showerror("Error", "Please select a relationship status to update.")

    def delete_status(self):
        selected_index = self.status_listbox.curselection()
        if selected_index:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="phonebook"
                )
                cursor = connection.cursor()
                cursor.execute("DELETE FROM relationship_statuses WHERE id = %s AND user_id = %s", (selected_index[0] + 1, self.user_id))
                connection.commit()
                connection.close()
                self.populate_status_listbox()
            except mysql.connector.Error as error:
                print("Error deleting relationship status:", error)
        else:
            messagebox.showerror("Error", "Please select a relationship status to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RelationshipStatusApp(root, int(sys.argv[1]))
    root.mainloop()
