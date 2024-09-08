import tkinter as tk  # Importing the Tkinter library for GUI components
from tkinter import messagebox, ttk  # Importing messagebox for error/info popups and ttk for styled widgets
import pymysql  # Importing pymysql for database connection and operations
from tkcalendar import DateEntry  # Importing DateEntry from tkcalendar to handle date input
import datetime  # Importing datetime to work with date objects

# Function to clear all input fields, reset the date picker, and refresh the records in the Treeview
def clear_entries():
    for entry in entries:  # Loop through all entries (input fields)
        if isinstance(entry, tk.StringVar):  # If the entry is a StringVar (e.g., from dropdowns)
            entry.set("")  # Reset it
        else:
            entry.delete(0, tk.END)  # If it's a text input, clear it
    gender_var.set("")  # Reset gender selection
    branch_var.set("")  # Reset branch selection
    course_var.set("")  # Reset course selection
    tree.selection_remove(tree.selection())  # Deselect any row in the Treeview
    dob_entry.set_date(datetime.date.today())  # Reset the DOB field to the current date
    show_all_records()  # Refresh the records in the Treeview

# Function to validate if an entry (input field) is filled and appropriate selections are made
def validate_entry(entry):
    if isinstance(entry, ttk.Entry):  # Check if the widget is an Entry
        if not entry.get().strip():  # If the Entry field is empty
            messagebox.showerror("Input Error", f"{entry.label_text} is required.")  # Show an error
            entry.focus()  # Set focus on the missing field
            return False  # Return validation failure
        elif branch_var.get() == "":  # Check if the branch is selected
            messagebox.showerror("Input Error", "Please select a valid Branch.")  # Error for branch
            return False
        elif course_var.get() == "":  # Check if the course is selected
            messagebox.showerror("Input Error", "Please select a valid Course.")  # Error for course
            return False
        elif gender_var.get() == "":  # Check if gender is selected
            messagebox.showerror("Input Error", "Please select a valid Gender.")  # Error for gender
            return False
    return True  # Validation success

# Function to move focus to the next entry when pressing Enter key
def move_focus(event):
    widget = event.widget  # Get the widget where the event occurred
    current_index = entries.index(widget)  # Get the current widget's index in the entries list
    if validate_entry(widget):  # If the current field passes validation
        next_index = (current_index + 1) % len(entries)  # Calculate the next widget's index
        next_entry = entries[next_index]  # Get the next entry field
        if isinstance(next_entry, tk.StringVar):  # If it's a dropdown or StringVar type field
            next_entry.set('')  # Reset it
            next_index = (current_index + 2) % len(entries)  # Skip ahead to the next input field
            entries[next_index].focus()  # Focus on the next widget
        else:
            entries[next_index].focus()  # Focus on the next entry field

# Function to display selected record in input fields when a Treeview row is clicked
def display_selected_record(event):
    selected_item = tree.focus()  # Get the currently selected item in the Treeview
    if selected_item:  # If an item is selected
        record = tree.item(selected_item)['values']  # Retrieve the values of the selected row
        for i, value in enumerate(record):  # Loop over the record's values
            if i < len(entries):  # If the value corresponds to an entry
                if isinstance(entries[i], ttk.Entry):  # If it's a text entry
                    entries[i].delete(0, tk.END)  # Clear the entry
                    entries[i].insert(0, value)  # Insert the value into the entry
                elif isinstance(entries[i], tk.StringVar):  # If it's a StringVar (dropdown)
                    entries[i].set(value)  # Set the dropdown value
        branch_var.set(record[6])  # Set the branch value
        course_var.set(record[7])  # Set the course value
        gender_var.set(record[8])  # Set the gender value (assumed index 8)
        dob_entry.set_date(record[9])  # Set the DOB value (assumed index 9)

# Function to save details entered in the form into the database
def save_details():
    if all(validate_entry(entry) for entry in entries):  # Check if all entries pass validation
        roll_number = entries[2].get()  # Get the roll number (assumed index 2)
        try:
            # Check if the roll number already exists in the database
            query = "SELECT * FROM students WHERE roll_number=%s"
            cursor.execute(query, (roll_number,))
            result = cursor.fetchone()

            if result:  # If roll number exists, show error
                messagebox.showerror("Duplicate Entry", "A record with this Roll Number already exists.")
                return

            # Create a data dictionary to hold input field values
            data = {
                "First Name": entries[0].get(),
                "Last Name": entries[1].get(),
                "Roll Number": roll_number,
                "Email": entries[3].get(),
                "Mobile": entries[4].get(),
                "Alternate Phone": entries[5].get(),
                "Branch": branch_var.get(),
                "Course": course_var.get(),
                "Gender": gender_var.get(),
                "DOB": dob_entry.get_date().strftime("%Y-%m-%d"),
                "Address": entries[6].get()
            }

            # Insert query for saving the student data
            query = """INSERT INTO students (first_name, last_name, roll_number, email, mobile, alt_mobile, branch, 
                                              course, gender, dob, address)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = tuple(data.values())  # Convert data values to tuple for query execution

            cursor.execute(query, values)  # Execute the insert query
            conn.commit()  # Commit the changes to the database
            messagebox.showinfo("Success", "Record Saved")  # Show success message
            clear_entries()  # Clear the input fields
        except Exception as e:
            messagebox.showerror("Database Error", str(e))  # Show error if query execution fails
    show_all_records()  # Refresh the Treeview to show updated records

# Function to load and display all records in the Treeview
def show_all_records():
    for row in tree.get_children():  # Clear the Treeview
        tree.delete(row)

    try:
        # Fetch all records from the students table
        query = "SELECT first_name, last_name, roll_number, email, mobile, alt_mobile, branch, course, gender, dob, address FROM students"
        cursor.execute(query)
        results = cursor.fetchall()  # Get all fetched records

        for row in results:  # Insert each record into the Treeview
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))  # Show error if fetching records fails

# Function to update a selected record in the database
def update_record():
    selected_item = tree.focus()  # Get the selected item in the Treeview
    if not selected_item:  # If no item is selected, show a warning
        messagebox.showwarning("Selection Error", "Please select a record to update.")
        return

    record = tree.item(selected_item)['values']  # Get the selected record's values
    roll_number = record[2]  # Get the roll number (assumed index 2)

    # Prepare a dictionary of updated data from the input fields
    updated_data = {
        "First Name": entries[0].get(),
        "Last Name": entries[1].get(),
        "Email": entries[3].get(),
        "Mobile": entries[4].get(),
        "alt_mobile": entries[5].get(),
        "Branch": branch_var.get(),
        "Course": course_var.get(),
        "Gender": gender_var.get(),
        "DOB": dob_entry.get_date().strftime("%Y-%m-%d"),
        "Address": entries[6].get()
    }

    # Check if any changes were made to the record
    changes_made = False
    for i, key in enumerate(updated_data.keys()):
        if updated_data[key] != record[i]:
            changes_made = True  # Mark that changes were made
            break

    if not changes_made:  # If no changes were made, show an error
        messagebox.showerror("Update Error", "You must change at least one field to update.")
        return

    # Prepare an update query with only the changed fields
    update_query = "UPDATE students SET "
    update_fields = []
    update_values = []

    for i, (key, value) in enumerate(updated_data.items()):
        if value != record[i]:  # Only update changed fields
            update_fields.append(f"{key.lower().replace(' ', '_')}=%s")
            update_values.append(value)

    update_query += ", ".join(update_fields) + " WHERE roll_number=%s"
    update_values.append(roll_number)

    try:
        cursor.execute(update_query, tuple(update_values))  # Execute the update query
        conn.commit()  # Commit the changes to the database
        messagebox.showinfo("Success", "Record updated successfully.")  # Show success message
        clear_entries()  # Clear the input fields
    except Exception as e:
        messagebox.showerror("Database Error", str(e))  # Show error if query execution fails

    show_all_records()  # Refresh the Treeview with updated records

# Function to delete a selected record from the database
def delete_record():
    selected_item = tree.focus()  # Get the selected item in the Treeview
    if not selected_item:  # If no item is selected, show a warning
        messagebox.showwarning("Selection Error", "Please select a record to delete.")
        return

    record = tree.item(selected_item)['values']  # Get the selected record's values
    roll_number = record[2]  # Get the roll number (assumed index 2)

    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete record {roll_number}?")
    if confirm:  # If user confirms deletion
        try:
            query = "DELETE FROM students WHERE roll_number=%s"
            cursor.execute(query, (roll_number,))  # Execute the delete query
            conn.commit()  # Commit the changes to the database
            messagebox.showinfo("Success", "Record deleted successfully.")  # Show success message
            clear_entries()  # Clear the input fields
        except Exception as e:
            messagebox.showerror("Database Error", str(e))  # Show error if query execution fails

    show_all_records()  # Refresh the Treeview with updated records

# Initialize database connection
def init_db():
    global conn, cursor
    try:
        conn = pymysql.connect(
            host='localhost', user='root', password='password', database='student_registration')
        cursor = conn.cursor()
    except Exception as e:
        messagebox.showerror("Connection Error", f"Unable to connect to the database. Error: {str(e)}")

# Close the database connection upon closing the app
def close_db():
    if conn:
        conn.close()

# Define the main app window
app = tk.Tk()
app.title("Student Registration System")  # Set the window title
app.geometry("800x600")  # Set the window size
app.configure(bg="lightblue")  # Set background color

# Define label and entry fields for the registration form
labels_texts = ["First Name", "Last Name", "Roll Number", "Email", "Mobile", "Alt Mobile", "Address"]
entries = []

for i, label_text in enumerate(labels_texts):
    label = ttk.Label(app, text=label_text)  # Create label
    label.grid(row=i, column=0, padx=10, pady=5)  # Place label on the grid
    entry = ttk.Entry(app)  # Create entry (text field)
    entry.grid(row=i, column=1, padx=10, pady=5)  # Place entry on the grid
    entry.label_text = label_text  # Store label text in entry for validation messages
    entries.append(entry)  # Add entry to the list of entries

# Define other input fields such as Gender (Radio buttons), Branch (Dropdown), Course (Dropdown), and DOB (DateEntry)
gender_var = tk.StringVar()  # Variable to store gender selection
branch_var = tk.StringVar()  # Variable to store branch selection
course_var = tk.StringVar()  # Variable to store course selection

# Gender selection with radio buttons
gender_label = ttk.Label(app, text="Gender")
gender_label.grid(row=len(entries), column=0, padx=10, pady=5)
gender_frame = ttk.Frame(app)  # Create a frame to hold radio buttons
gender_frame.grid(row=len(entries), column=1, padx=10, pady=5)
male_radio = ttk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male")
male_radio.grid(row=0, column=0)
female_radio = ttk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female")
female_radio.grid(row=0, column=1)
entries.append(gender_var)  # Add gender_var to the list of entries for validation

# Branch selection with dropdown
branch_label = ttk.Label(app, text="Branch")
branch_label.grid(row=len(entries), column=0, padx=10, pady=5)
branch_dropdown = ttk.Combobox(app, textvariable=branch_var, values=["CSE", "ECE", "EEE", "IT", "MECH"], state="readonly")
branch_dropdown.grid(row=len(entries), column=1, padx=10, pady=5)
entries.append(branch_var)  # Add branch_var to the list of entries for validation

# Course selection with dropdown
course_label = ttk.Label(app, text="Course")
course_label.grid(row=len(entries), column=0, padx=10, pady=5)
course_dropdown = ttk.Combobox(app, textvariable=course_var, values=["B.Tech", "M.Tech", "MBA"], state="readonly")
course_dropdown.grid(row=len(entries), column=1, padx=10, pady=5)
entries.append(course_var)  # Add course_var to the list of entries for validation

# Date of Birth selection with DateEntry widget
dob_label = ttk.Label(app, text="Date of Birth")
dob_label.grid(row=len(entries), column=0, padx=10, pady=5)
dob_entry = DateEntry(app, date_pattern='yyyy-mm-dd')  # Create DateEntry widget for DOB selection
dob_entry.grid(row=len(entries), column=1, padx=10, pady=5)
entries.append(dob_entry)  # Add dob_entry to the list of entries

# Define buttons for form actions: Save, Update, Delete, Clear
save_button = ttk.Button(app, text="Save", command=save_details)  # Create Save button
save_button.grid(row=len(entries)+1, column=0, padx=10, pady=10)

update_button = ttk.Button(app, text="Update", command=update_record)  # Create Update button
update_button.grid(row=len(entries)+1, column=1, padx=10, pady=10)

delete_button = ttk.Button(app, text="Delete", command=delete_record)  # Create Delete button
delete_button.grid(row=len(entries)+1, column=2, padx=10, pady=10)

clear_button = ttk.Button(app, text="Clear", command=clear_entries)  # Create Clear button
clear_button.grid(row=len(entries)+1, column=3, padx=10, pady=10)

# Define a Treeview widget to display the records in a table format
tree = ttk.Treeview(app, columns=("First Name", "Last Name", "Roll Number", "Email", "Mobile", "Alt Mobile", "Branch", "Course", "Gender", "DOB", "Address"),
                    show="headings", selectmode="browse")
tree.grid(row=len(entries)+2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
tree.bind("<ButtonRelease-1>", display_selected_record)  # Bind row click to show the record in input fields

# Define column headings for the Treeview
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Create vertical and horizontal scrollbars for the Treeview
vsb = ttk.Scrollbar(app, orient="vertical", command=tree.yview)
vsb.grid(row=len(entries)+2, column=4, sticky="ns")
tree.configure(yscrollcommand=vsb.set)

hsb = ttk.Scrollbar(app, orient="horizontal", command=tree.xview)
hsb.grid(row=len(entries)+3, column=0, columnspan=4, sticky="ew")
tree.configure(xscrollcommand=hsb.set)

# Initialize the database connection and fetch the records when the app starts
init_db()
show_all_records()

# Bind the Enter key to move focus to the next entry field
for entry in entries:
    if isinstance(entry, ttk.Entry):  # Bind only for Entry fields
        entry.bind("<Return>", move_focus)

# Run the Tkinter main event loop
app.mainloop()

# Close the database connection when the app closes
close_db()
