import tkinter as tk
from tkinter import messagebox
import mysql.connector
import sys

class UpdateStatementsApp:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Update Statements GUI")

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Click the button to execute UPDATE statements:", font=("Helvetica", 12))
        self.label.grid(row=0, columnspan=2, padx=10, pady=10)

        self.update_button = tk.Button(self.frame, text="Execute UPDATE Statements", command=lambda: self.execute_update_statements(user_id))
        self.update_button.grid(row=1, columnspan=2, padx=10, pady=10)

        self.output_text = tk.Text(self.frame, width=50, height=10)
        self.output_text.grid(row=2, columnspan=2, padx=10, pady=10)

    def execute_update_statements(self, user_id):
        try:
            # Establish connection to the database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="phonebook"
            )

            # Create cursor object to execute SQL queries
            cursor = connection.cursor()

            # List of remaining 10 UPDATE statements based on user_id
            update_statements = [
                f"UPDATE contacts SET relationship_status = 'Married' WHERE user_id = {user_id}",
                f"UPDATE contacts SET relationship_status = 'Single' WHERE user_id = {user_id}",
                f"UPDATE contacts SET relationship_status = 'Divorced' WHERE user_id = {user_id}",
                f"UPDATE contacts SET relationship_status = 'Engaged' WHERE user_id = {user_id}",
                f"UPDATE contacts SET relationship_status = 'Married' WHERE user_id = {user_id}",
                f"UPDATE contacts SET relationship_status = 'Single' WHERE user_id = {user_id}",
                f"UPDATE contacts SET relationship_status = 'Divorced' WHERE user_id = {user_id}",
                f"UPDATE contacts SET relationship_status = 'Married' WHERE user_id = {user_id}",
                f"UPDATE contacts SET relationship_status = 'Single' WHERE user_id = {user_id}",
                f"UPDATE contacts SET relationship_status = 'Divorced' WHERE user_id = {user_id}"
            ]

            # Execute each UPDATE statement
            output = ""
            for statement in update_statements:
                cursor.execute(statement)
                connection.commit()
                output += f"{statement}\n"

            messagebox.showinfo("Success", "UPDATE statements executed successfully.")
            self.output_text.insert(tk.END, output)

            # Close cursor and connection
            cursor.close()
            connection.close()

        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error executing SQL statement: {error}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UpdateStatementsApp(root, int(sys.argv[1])) 
    root.mainloop()
