import tkinter as tk
from tkinter import messagebox, ttk
import pymysql
from tkcalendar import DateEntry
import datetime

def clear_entries():
    for entry in entries:
        if isinstance(entry, tk.StringVar):
            entry.set("")
        else:
            entry.delete(0, tk.END)
    gender_var.set("")
    branch_var.set("")
    course_var.set("")
    tree.selection_remove(tree.selection()) 
    dob_entry.set_date(datetime.date.today())
    show_all_records()

def validate_entry(entry):
    if isinstance(entry, ttk.Entry):
        if not entry.get().strip():  # Check if the Entry field is empty
            messagebox.showerror("Input Error", f"{entry.label_text} is required.")
            entry.focus()
            return False
        elif branch_var.get() == "":
            messagebox.showerror("Input Error", "Please select a valid Branch.")
            return False
        elif course_var.get() == "":
            messagebox.showerror("Input Error", "Please select a valid Course.")
            return False
        elif gender_var.get() == "":
            messagebox.showerror("Input Error", "Please select a valid Gender.")
            return False
    return True


def move_focus(event):
    widget = event.widget
    current_index = entries.index(widget)
    if validate_entry(widget):
        next_index = (current_index + 1) % len(entries)
        next_entry = entries[next_index]
        if isinstance(next_entry, tk.StringVar):
            next_entry.set('')
            next_index = (current_index + 2) % len(entries)
            entries[next_index].focus()
        else:
            entries[next_index].focus()

def display_selected_record(event):
    selected_item = tree.focus()
    if selected_item:
        record = tree.item(selected_item)['values']
        for i, value in enumerate(record):
            if i < len(entries):
                if isinstance(entries[i], ttk.Entry):
                    entries[i].delete(0, tk.END)
                    entries[i].insert(0, value)
                elif isinstance(entries[i], tk.StringVar):
                    entries[i].set(value)
        branch_var.set(record[6])
        course_var.set(record[7])
        gender_var.set(record[8])  # Assuming Gender is at index 8
        dob_entry.set_date(record[9])  # Assuming DOB is at index 9


def save_details():
    if all(validate_entry(entry) for entry in entries):
        roll_number = entries[2].get()
        try:
            query = "SELECT * FROM students WHERE roll_number=%s"
            cursor.execute(query, (roll_number,))
            result = cursor.fetchone()

            if result:
                messagebox.showerror("Duplicate Entry", "A record with this Roll Number already exists.")
                return

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

            query = """INSERT INTO students (first_name, last_name, roll_number, email, mobile, alt_mobile, branch, 
                                              course, gender, dob, address)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = tuple(data.values())

            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Success", "Record Saved")
            clear_entries()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
    show_all_records()  # Refresh the data in the Treeview
def show_all_records():
    for row in tree.get_children():
        tree.delete(row)

    try:
        query = "SELECT first_name, last_name, roll_number, email, mobile, alt_mobile, branch, course, gender, dob, address FROM students"
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def update_record():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a record to update.")
        return

    record = tree.item(selected_item)['values']
    roll_number = record[2]  # Assuming Roll Number is at index 2

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

    # Check for changes
    changes_made = False
    for i, key in enumerate(updated_data.keys()):
        if updated_data[key] != record[i]:
            changes_made = True
            break

    if not changes_made:
        messagebox.showerror("Update Error", "You must change at least one field to update.")
        return

    # Only update the fields that have changed
    update_query = "UPDATE students SET "
    update_fields = []
    update_values = []

    for i, (key, value) in enumerate(updated_data.items()):
        if value != record[i]:
            update_fields.append(f"{key.lower().replace(' ', '_')}=%s")
            update_values.append(value)

    update_query += ", ".join(update_fields) + " WHERE roll_number=%s"
    update_values.append(roll_number)

    try:
        cursor.execute(update_query, tuple(update_values))
        conn.commit()
        messagebox.showinfo("Success", "Record Updated")
        clear_entries()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

    show_all_records()


def delete_record():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a record to delete.")
        return

    record = tree.item(selected_item)['values']
    roll_number = record[2]

    try:
        query = "DELETE FROM students WHERE roll_number=%s"
        cursor.execute(query, (roll_number,))
        conn.commit()
        messagebox.showinfo("Success", "Record Deleted")
        clear_entries()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    show_all_records()  # Refresh the data in the Treeview

def search_records():
    filters = {
        "first_name": entries[0].get(),
        "last_name": entries[1].get(),
        "roll_number": entries[2].get(),
        "email": entries[3].get(),
        "mobile": entries[4].get(),
        "alt_mobile": entries[5].get(),
        "branch": branch_var.get(),
        "course": course_var.get(),
        "gender": gender_var.get(),
        "address": entries[6].get()
    }

    query = "SELECT first_name, last_name, roll_number, email, mobile, alt_mobile, branch, course, gender, dob, address FROM students WHERE 1=1"
    values = []

    for key, value in filters.items():
        if value:
            query += f" AND {key} LIKE %s"
            values.append(f"%{value}%")

    for row in tree.get_children():
        tree.delete(row)

    try:
        cursor.execute(query, values)
        results = cursor.fetchall()
        for row in results:
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if conn:
            conn.close()
        root.destroy()

try:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="diet"
    )
    cursor = conn.cursor()
    print("DB Connected")
except Exception as e:
    messagebox.showerror("DB Error", str(e))
    raise

# Tkinter GUI Setup
root = tk.Tk()
root.title("Student Management System")
root.state("zoomed")

fs = ("Times New Roman", 17)

title = tk.Label(root, text="Student Management System", fg="black", bg="yellow", pady=20, font=("Comic Sans MS", 25, "bold"))
title.grid(row=0, column=0, columnspan=4)

# Arranging the labels and entries
labels_texts = [
    ("Enter First Name", "Enter Last Name"),
    ("Enter Roll Number", "Enter Email"),
    ("Enter Mobile", "Enter Alternate Phone"),
    ("Enter Address",)
]

entries = []
for i, labels in enumerate(labels_texts):
    for j, label_text in enumerate(labels):
        label = tk.Label(root, text=label_text, font=fs, width=15, bg="yellow", fg="blue")
        label.grid(row=i+1, column=j*2, pady=10, sticky="e")

        entry = ttk.Entry(root, font=fs)
        entry.label_text = label_text
        entry.grid(row=i+1, column=j*2+1, pady=10, padx=10, sticky="w")
        entries.append(entry)

# Date of Birth
dob_label = tk.Label(root, text="Select DOB", font=fs, width=15, bg="yellow", fg="blue")
dob_label.grid(row=len(labels_texts)+1, column=0, pady=10, sticky="e")

dob_entry = DateEntry(root, font=fs, width=17, background='darkblue', foreground='white', date_pattern="yyyy-mm-dd")
dob_entry.grid(row=len(labels_texts)+1, column=1, pady=10, padx=10, sticky="w")

# Gender Label and Radio Buttons
gender_var = tk.StringVar()
gender_label = tk.Label(root, text="Select Gender", font=fs, width=15, bg="yellow", fg="blue")
gender_label.grid(row=len(labels_texts)+1, column=2, pady=10, sticky="e")

gender_frame = tk.Frame(root)
gender_frame.grid(row=len(labels_texts)+1, column=3, pady=10, padx=10, sticky="w")
ttk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male").pack(side="left")
ttk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female").pack(side="left")
ttk.Radiobutton(gender_frame, text="Other", variable=gender_var, value="Other").pack(side="left")
gender_var.label_text = "Gender"

# Branch and Course Dropdowns
branches = ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil"]
branch_var = tk.StringVar()
branch_label = tk.Label(root, text="Choose Branch", font=fs, width=15, bg="yellow", fg="blue")
branch_label.grid(row=len(labels_texts)+2, column=0, pady=10, sticky="e")

branch_dropdown = ttk.Combobox(root, font=fs, values=branches, state="readonly", textvariable=branch_var)
branch_dropdown.grid(row=len(labels_texts)+2, column=1, pady=10, padx=10, sticky="w")

courses = ["B.Tech", "M.Tech", "PhD"]
course_var = tk.StringVar()
course_label = tk.Label(root, text="Choose Course", font=fs, width=15, bg="yellow", fg="blue")
course_label.grid(row=len(labels_texts)+2, column=2, pady=10, sticky="e")

course_dropdown = ttk.Combobox(root, font=fs, values=courses, state="readonly", textvariable=course_var)
course_dropdown.grid(row=len(labels_texts)+2, column=3, pady=10, padx=10, sticky="w")

# Create a Style object
style = ttk.Style()

# Configure the custom style for the buttons
style.configure('Custom.TButton',
                font=('Helvetica', 14, 'bold'),
                foreground='blue',
                background='yellow',
                padding=10)

# Configure the style for different states (active, disabled)
style.map('Custom.TButton',
          foreground=[('active', 'green'), ('disabled', 'gray')],
          background=[('active', 'black'), ('disabled', 'lightgrey')])

btn_search = ttk.Button(root, text="Search",style='Custom.TButton',  command=search_records)
btn_search.place(x=300,y=670)

btn_save = ttk.Button(root, text="Save", style='Custom.TButton',  command=save_details)
btn_save.place(x=700,y=670)

btn_update = ttk.Button(root, text="Update", style='Custom.TButton',  command=update_record)
btn_update.place(x=1100,y=670)

btn_delete = ttk.Button(root, text="Delete", style='Custom.TButton',  command=delete_record)
btn_delete.place(x=500,y=720)

# Clear Button
btn_clear = ttk.Button(root, text="Clear", style='Custom.TButton',  command=clear_entries)
btn_clear.place(x=900,y=720)

# Treeview for displaying records
tree_frame = tk.Frame(root)
tree_frame.grid(row=len(labels_texts)+5, column=0, columnspan=4, pady=20, padx=20)

columns = ("first_name", "last_name", "roll_number", "email", "mobile", "alt_mobile", "branch", "course", "gender", "dob", "address")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

verscrlbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
verscrlbar.pack(side='right', fill='y')  # Correct fill direction to 'y' for vertical scrollbar
tree.configure(yscrollcommand=verscrlbar.set) 

for col in columns:
    tree.heading(col, text=col.replace("_", " ").title())
    tree.column(col, width=136)

tree.pack(fill="both", expand=True)
tree.bind("<ButtonRelease-1>", display_selected_record)  # Bind row selection

for entry in entries:
    entry.bind("<Return>", move_focus)

show_all_records()  # Load the initial data into the Treeview

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
