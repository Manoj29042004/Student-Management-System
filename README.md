# Student Management

A Tkinter-based Student Management application that allows users to add, update, delete, and search student records. The records are stored in a MySQL database, and the GUI provides an intuitive interface for managing student information efficiently.

## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Database Setup](#database-setup)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **Add Students**: Input and save new student records with validation.
- **Update Students**: Modify existing student details with selective field updates.
- **Delete Students**: Remove student records from the database.
- **Search Students**: Find students using various filters like name, roll number, branch, etc.
- **Display Records**: View all student records in a sortable and searchable Treeview.
- **Clear Form**: Reset all input fields with a single click.
- **Responsive UI**: User-friendly interface with proper focus management and styling.
- **Validation**: Ensures that all necessary fields are filled and correctly formatted.

## Screenshots
![image](https://github.com/user-attachments/assets/082b152d-0eab-4820-a77f-95e63bf3890c)


## Installation

### Prerequisites
- **Python 3.x**: Ensure that Python is installed on your system. You can download it from [here](https://www.python.org/downloads/).
- **MySQL Server**: Install MySQL Server to manage your database. Download it from [here](https://dev.mysql.com/downloads/mysql/).

### Steps

1. **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/student-management.git
    ```
2. **Navigate to the Project Directory**
    ```bash
    cd student-management
    ```
3. **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    python -m venv venv
    ```
    - **Activate the Virtual Environment:**
        - **Windows:**
            ```bash
            venv\Scripts\activate
            ```
        - **macOS/Linux:**
            ```bash
            source venv/bin/activate
            ```
4. **Install Required Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Set Up the Database**
    - Ensure that MySQL Server is running.
    - Use the provided SQL script in the [Database Setup](#database-setup) section to create the necessary database and table.

2. **Configure Database Connection**
    - Open the Python script (e.g., `student_management.py`) and locate the database connection section.
    - Update the `host`, `user`, `password`, and `database` parameters as per your MySQL configuration.
    ```python
    import pymysql

    conn = pymysql.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='student_management'
    )
    cursor = conn.cursor()
    ```

3. **Run the Application**
    ```bash
    python student_management.py
    ```
    - The GUI window will appear, allowing you to manage student records.

## Dependencies

The project relies on the following Python packages:

- [`tkinter`](https://docs.python.org/3/library/tkinter.html): For creating the GUI.
- [`tkcalendar`](https://github.com/j4321/tkcalendar): For date entry widgets.
- [`pymysql`](https://pymysql.readthedocs.io/en/latest/): For MySQL database connections.
- [`ttkbootstrap`](https://ttkbootstrap.readthedocs.io/en/latest/): (Optional) For enhanced styling of widgets.

### Installing Dependencies

All dependencies can be installed using the provided `requirements.txt` file:
```bash
pip install -r requirements.txt
