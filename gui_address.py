import tkinter as tk
from tkinter import messagebox
import mysql.connector
import sys

class AddressApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Address Book")

        # Create labels and entry fields
        tk.Label(root, text="Address:").grid(row=0, column=0, padx=5, pady=5)
        self.address_entry = tk.Entry(root)
        self.address_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create buttons
        self.add_button = tk.Button(root, text="Add", command=self.add_address)
        self.add_button.grid(row=1, column=0, padx=5, pady=5)
        self.update_button = tk.Button(root, text="Update", command=self.update_address)
        self.update_button.grid(row=1, column=1, padx=5, pady=5)
        self.delete_button = tk.Button(root, text="Delete", command=self.delete_address)
        self.delete_button.grid(row=1, column=2, padx=5, pady=5)

        # Create listbox to display addresses
        self.address_listbox = tk.Listbox(root)
        self.address_listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # Populate listbox with existing addresses
        self.populate_address_listbox()

    def populate_address_listbox(self):
        self.address_listbox.delete(0, tk.END)
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="phonebook"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM addresses WHERE user_id = %s", (self.user_id,))
            addresses = cursor.fetchall()
            for address in addresses:
                self.address_listbox.insert(tk.END, address[1])
            connection.close()
        except mysql.connector.Error as error:
            print("Error fetching addresses:", error)

    def add_address(self):
        address = self.address_entry.get()
        if address:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="phonebook"
                )
                cursor = connection.cursor()
                cursor.execute("INSERT INTO addresses (address, user_id) VALUES (%s, %s)", (address, self.user_id))
                connection.commit()
                connection.close()
                self.address_entry.delete(0, tk.END)
                self.populate_address_listbox()
            except mysql.connector.Error as error:
                print("Error adding address:", error)
        else:
            messagebox.showerror("Error", "Please enter an address.")

    def update_address(self):
        selected_index = self.address_listbox.curselection()
        if selected_index:
            new_address = self.address_entry.get()
            if new_address:
                try:
                    connection = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="phonebook"
                    )
                    cursor = connection.cursor()
                    cursor.execute("UPDATE addresses SET address = %s WHERE id = %s AND user_id = %s",
                                   (new_address, selected_index[0] + 1, self.user_id))  # Index in list starts from 0, id starts from 1
                    connection.commit()
                    connection.close()
                    self.populate_address_listbox()
                except mysql.connector.Error as error:
                    print("Error updating address:", error)
            else:
                messagebox.showerror("Error", "Please enter a new address.")
        else:
            messagebox.showerror("Error", "Please select an address to update.")

    def delete_address(self):
        selected_index = self.address_listbox.curselection()
        if selected_index:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="phonebook"
                )
                cursor = connection.cursor()
                cursor.execute("DELETE FROM addresses WHERE id = %s AND user_id = %s", (selected_index[0] + 1, self.user_id))
                connection.commit()
                connection.close()
                self.populate_address_listbox()
            except mysql.connector.Error as error:
                print("Error deleting address:", error)
        else:
            messagebox.showerror("Error", "Please select an address to delete.")

if __name__ == "__main__":
    
    root = tk.Tk()
    app = AddressApp(root, int(sys.argv[1]))
    root.mainloop()
