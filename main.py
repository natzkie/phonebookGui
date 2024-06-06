# Importing required modules
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import os
import sys

class PhoneBookApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Phone Book")
        
        # Calculate the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the x and y coordinates to display the window at the center
        x_coordinate = (screen_width - 1800) // 2
        y_coordinate = (screen_height - 800) // 2

        # Set the window geometry
        self.root.geometry(f"1800x800+{x_coordinate}+{y_coordinate}")

        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack(pady=20)

        self.input_frame = tk.Frame(self.frame, borderwidth=5, relief=tk.GROOVE)
        self.input_frame.grid(row=0, column=0, padx=(120, 120), pady=5, sticky="nw")

        self.first_name_label = tk.Label(self.input_frame, text="first_name", font=("Helvetica", 14))
        self.first_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.first_name_entry = tk.Entry(self.input_frame, font=("Helvetica", 14), width=30, borderwidth=2)
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.last_name_label = tk.Label(self.input_frame, text="last_name", font=("Helvetica", 14))
        self.last_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.last_name_entry = tk.Entry(self.input_frame, font=("Helvetica", 14), width=30, borderwidth=2)
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.phone_label = tk.Label(self.input_frame, text="Phone", font=("Helvetica", 14))
        self.phone_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.phone_entry = tk.Entry(self.input_frame, font=("Helvetica", 14), width=30, borderwidth=2)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.backup_number_label = tk.Label(self.input_frame, text="Backup Number", font=("Helvetica", 14))
        self.backup_number_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.backup_number_entry = tk.Entry(self.input_frame, font=("Helvetica", 14), width=30, borderwidth=2)
        self.backup_number_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        self.ilabel = tk.Label(self.input_frame, text="Label", font=("Helvetica", 14))
        self.ilabel.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.ilabel_entry = tk.Entry(self.input_frame, font=("Helvetica", 14), width=30, borderwidth=2)
        self.ilabel_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.address_label = tk.Label(self.input_frame, text="Address", font=("Helvetica", 14))
        self.address_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.address_var = tk.StringVar()  # Variable to hold selected address
        self.address_dropdown = ttk.Combobox(self.input_frame, textvariable=self.address_var, font=("Helvetica", 14), width=27)
        self.address_dropdown.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        self.relationship_label = tk.Label(self.input_frame, text="Relationship Status", font=("Helvetica", 14))
        self.relationship_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.relationship_var = tk.StringVar()  # Variable to hold selected relationship status
        self.relationship_dropdown = ttk.Combobox(self.input_frame, textvariable=self.relationship_var, font=("Helvetica", 14), width=27)
        self.relationship_dropdown.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        self.search_var = tk.StringVar()
        self.search_frame = tk.Frame(self.frame, relief=tk.GROOVE)
        self.search_frame.grid(row=1, column=1, padx=(49, 0), pady=5, sticky="nw")
        self.search_bar = tk.Entry(self.search_frame, textvariable=self.search_var, font=("Helvetica", 14), width=30, borderwidth=2)
        self.search_bar.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.search_button = tk.Button(self.search_frame, text="Search", font=("Helvetica", 14), command=self.search_contacts, bg="#007bff", fg="white")
        self.search_button.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        self.button_frame = tk.Frame(self.frame, relief=tk.GROOVE)
        self.button_frame.grid(row=0, column=1, padx=(0, 120), pady=5, sticky="nw")

        self.add_button = tk.Button(self.button_frame, text="Add", font=("Helvetica", 14), command=self.add_contact, bg="#007bff", fg="white", width=20)
        self.add_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.update_button = tk.Button(self.button_frame, text="Update", font=("Helvetica", 14), command=self.update_contact, bg="#007bff", fg="white", width=20)
        self.update_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.delete_button = tk.Button(self.button_frame, text="Delete", font=("Helvetica", 14), command=self.delete_contact, bg="#007bff", fg="white", width=20)
        self.delete_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.clear_button = tk.Button(self.button_frame, text="Clear", font=("Helvetica", 14), command=self.clear_entries, bg="#007bff", fg="white", width=20)
        self.clear_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.pagination_frame = tk.Frame(self.frame)
        self.pagination_frame.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        self.contacts_per_page_var = tk.IntVar(value=10)
        self.contacts_per_page_label = tk.Label(self.pagination_frame, text="Contacts per page:", font=("Helvetica", 14))
        self.contacts_per_page_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.contacts_per_page_entry = tk.Entry(self.pagination_frame, textvariable=self.contacts_per_page_var, font=("Helvetica", 14), width=5, borderwidth=2)
        self.contacts_per_page_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.prev_button = tk.Button(self.pagination_frame, text="Previous", font=("Helvetica", 14), command=self.prev_page, bg="#007bff", fg="white")
        self.prev_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.next_button = tk.Button(self.pagination_frame, text="Next", font=("Helvetica", 14), command=self.next_page, bg="#007bff", fg="white")
        self.next_button.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        self.current_page_label = tk.Label(self.pagination_frame, text="Page 1", font=("Helvetica", 14))
        self.current_page_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")

        self.contact_listbox = tk.Listbox(self.frame, height=15, width=110, font=("Courier New", 14), borderwidth=2)
        self.contact_listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.contact_listbox.bind('<<ListboxSelect>>', self.load_contact)

        self.selected_contact_details = None
        self.current_page = 1
        
        self.load_contacts()
        self.load_addresses()
        self.load_relationship_statuses()

    def get_db_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Update with your database password
            database="phonebook"
        )

    def add_contact(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        backup_number = self.backup_number_entry.get()
        address_id = self.get_address_id(self.address_var.get())
        relationship_status_id = self.get_relationship_status_id(self.relationship_var.get())

        if first_name and phone:  # Ensure required fields are filled
            if len(phone) <= 15 and phone.isdigit():  # Validate phone number
                if not self.check_duplicate_phone(self,phone):  # Check for duplicate phone number
                    if address_id and relationship_status_id:
                        conn = self.get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute('INSERT INTO contacts (first_name, last_name, phone, backup_number, address_id, relationship_status_id, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (first_name, last_name, phone, backup_number, address_id, relationship_status_id, self.user_id))
                        conn.commit()
                        contact_id = cursor.lastrowid
                        conn.close()
                        self.load_contacts()
                        self.clear_entries()
                    else:
                        messagebox.showwarning("Input Error", "Please select both address and relationship status.")
                else:
                    messagebox.showwarning("Duplicate Error", "Phone number already exists.")
            else:
                messagebox.showwarning("Input Error", "Please enter a valid phone number (maximum 15 digits).")
        else:
            messagebox.showwarning("Input Error", "Please enter at least First Name and Phone.")

    def update_contact(self):
        if self.selected_contact_details:
            contact_id = self.selected_contact_details['id']
            first_name = self.first_name_entry.get()
            last_name = self.last_name_entry.get()
            phone = self.phone_entry.get()
            backup_number = self.backup_number_entry.get()
            label = self.label_entry.get()
            address_id = self.get_address_id(self.address_var.get())
            relationship_status_id = self.get_relationship_status_id(self.relationship_var.get())

            if first_name and phone:
                if len(phone) <= 15 and phone.isdigit():
                    if address_id and relationship_status_id:
                        conn = self.get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute('UPDATE contacts SET first_name=%s, last_name=%s, phone=%s, backup_number=%s,label=%s,  address_id=%s, relationship_status_id=%s WHERE id=%s', (first_name, last_name, phone, backup_number,label, address_id, relationship_status_id, contact_id))
                        conn.commit()
                        conn.close()
                        self.load_contacts()
                        self.clear_entries()
                    else:
                        messagebox.showwarning("Input Error", "Please select both address and relationship status.")
                else:
                    messagebox.showwarning("Input Error", "Please enter a valid phone number (maximum 15 digits).")
            else:
                messagebox.showwarning("Input Error", "Please enter at least First Name and Phone.")
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to update.")

    def delete_contact(self):
        if self.selected_contact_details:
            contact_id = self.selected_contact_details['id']
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contacts WHERE id=%s', (contact_id,))
            conn.commit()
            conn.close()
            self.load_contacts()
            self.clear_entries()
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")

    def clear_entries(self):
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.backup_number_entry.delete(0, tk.END)
        self.address_var.set('')
        self.relationship_var.set('')
        self.selected_contact_details = None

    def load_contact(self, event):
        selection = self.contact_listbox.curselection()
        if selection:
            index = selection[0]
            contact_details = self.contact_data[index]
            self.selected_contact_details = contact_details
            self.first_name_entry.delete(0, tk.END)
            self.first_name_entry.insert(0, contact_details['first_name'])
            self.last_name_entry.delete(0, tk.END)
            self.last_name_entry.insert(0, contact_details['last_name'])
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, contact_details['phone'])
            self.backup_number_entry.delete(0, tk.END)
            self.backup_number_entry.insert(0, contact_details['backup_number'])
            self.address_var.set(contact_details['address'])
            self.relationship_var.set(contact_details['relationship_status'])

    def load_contacts(self):
        self.contact_listbox.delete(0, tk.END)
        self.contact_data = []

        conn = self.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM contacts WHERE user_id=%s', (self.user_id,))
        contacts = cursor.fetchall()
        for contact in contacts:
            full_name = f"{contact['first_name']} {contact['last_name']}"
            self.contact_data.append(contact)
            self.contact_listbox.insert(tk.END, full_name)
        conn.close()

    def search_contacts(self):
        search_term = self.search_var.get()
        if search_term:
            self.contact_listbox.delete(0, tk.END)
            self.contact_data = []

            conn = self.get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM contacts WHERE (first_name LIKE %s OR last_name LIKE %s OR phone LIKE %s) AND user_id=%s', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', self.user_id))
            contacts = cursor.fetchall()
            for contact in contacts:
                full_name = f"{contact['first_name']} {contact['last_name']}"
                self.contact_data.append(contact)
                self.contact_listbox.insert(tk.END, full_name)
            conn.close()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.current_page_label.config(text=f"Page {self.current_page}")

    def next_page(self):
        total_pages = len(self.contact_data) // self.contacts_per_page_var.get() + 1
        if self.current_page < total_pages:
            self.current_page += 1
            self.current_page_label.config(text=f"Page {self.current_page}")

    def load_addresses(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM addresses')
        addresses = cursor.fetchall()
        address_options = [address[1] for address in addresses]
        self.address_dropdown['values'] = address_options
        conn.close()

    def load_relationship_statuses(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM relationship_statuses')
        relationship_statuses = cursor.fetchall()
        relationship_options = [status[1] for status in relationship_statuses]
        self.relationship_dropdown['values'] = relationship_options
        conn.close()

    def get_address_id(self, address):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM addresses WHERE address=%s', (address,))
        address_id = cursor.fetchone()
        conn.close()
        return address_id[0] if address_id else None

    def get_relationship_status_id(self, status_name):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM relationship_statuses WHERE status=%s', (status_name,))
        status_id = cursor.fetchone()
        conn.close()
        return status_id[0] if status_id else None


if __name__ == "__main__":
    root = tk.Tk()
    app = PhoneBookApp(root, int(sys.argv[1])) # Assuming user_id=1 for testing
    root.mainloop()