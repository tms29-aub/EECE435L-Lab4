import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from classes import Student, Instructor, Course

# Connect to SQLite database
conn = sqlite3.connect('school_management.db')
cursor = conn.cursor()

def init_db():
    """
    Initializes the database by checking if the necessary tables ('students', 'instructors', 'courses', 'enrollments') 
    exist, and creates them if they do not.
    
    :raises sqlite3.Error: If there is an issue creating or interacting with the database.
    :return: None
    :rtype: None
    """
    # Check if the 'students' table exists
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='students';
    ''')
    student_table_exists = cursor.fetchone()

    # Check if the 'instructors' table exists
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='instructors';
    ''')
    instructor_table_exists = cursor.fetchone()

    # Check if the 'courses' table exists
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='courses';
    ''')
    course_table_exists = cursor.fetchone()

    # Check if the 'enrollments' table exists
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='enrollments';
    ''')
    enrollment_table_exists = cursor.fetchone()

    # If any table does not exist, create the necessary tables
    if not student_table_exists:
        cursor.execute('''
            CREATE TABLE students (
                student_id INTEGER PRIMARY KEY, 
                name TEXT, 
                age INTEGER, 
                email TEXT
            )
        ''')

    if not instructor_table_exists:
        cursor.execute('''
            CREATE TABLE instructors (
                instructor_id INTEGER PRIMARY KEY, 
                name TEXT, 
                age INTEGER, 
                email TEXT
            )
        ''')

    if not course_table_exists:
        cursor.execute('''
            CREATE TABLE courses (
                course_id INTEGER PRIMARY KEY, 
                course_name TEXT, 
                instructor_id INTEGER,
                FOREIGN KEY (instructor_id) REFERENCES instructors (instructor_id)
            )
        ''')

    if not enrollment_table_exists:
        cursor.execute('''
            CREATE TABLE enrollments (
                course_id INTEGER, 
                student_id INTEGER, 
                FOREIGN KEY (course_id) REFERENCES courses (course_id),
                FOREIGN KEY (student_id) REFERENCES students (student_id)
            )
        ''')

    conn.commit()
    update_course_combobox()
    messagebox.showinfo("Success", "Database connection established, and necessary tables are ready.")


# Function to save data to SQLite database
def backup_data():
    """
    Creates a backup of the current database by copying the data to a separate backup database file.
    
    :raises sqlite3.Error: If there is an issue with the backup process.
    :raises Exception: If any other errors occur during the backup.
    :return: None
    :rtype: None
    """
    try:
        # Open a connection to the backup database
        backup_db = sqlite3.connect('school_management_backup.db')

        # Perform the backup
        with backup_db:
            conn.backup(backup_db)

        backup_db.close()

        # Show success message in a Tkinter messagebox
        messagebox.showinfo('Success', 'Backup created successfully!')

    except Exception as e:
        # Show error message in a Tkinter messagebox
        messagebox.showerror('Error', f'An error occurred during the backup: {e}')

root = tk.Tk()
root.title('School Management System')
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

main_tab = tk.Frame(notebook)
records_tab = tk.Frame(notebook)

notebook.add(main_tab, text="Main")
notebook.add(records_tab, text="Records")

def update_course_combobox():
    """
    Updates the combobox elements in the UI with the latest list of available courses from the database.
    
    :return: None
    :rtype: None
    """
    cursor = conn.cursor()
    cursor.execute("SELECT course_name FROM courses")
    courses = cursor.fetchall()

    course_names = [row[0] for row in courses]
    course_combobox['values'] = course_names
    course_combobox_for_instructor['values'] = course_names

    if course_names:
        course_combobox.set(course_names[0])
        course_combobox_for_instructor.set(course_names[0])
    else:
        course_combobox.set("No Courses Available")
        course_combobox_for_instructor.set("No Courses Available")

# Close the connection when the program exits
root.protocol("WM_DELETE_WINDOW", lambda: (conn.close(), root.destroy()))

def student_window():
    """
    Opens a new window in the UI to allow adding a new student to the database, including details such as 
    name, age, email, and student ID.
    
    :return: None
    :rtype: None
    """
    def add_student():
        name = student_name_entry.get()
        age = int(age_entry.get())
        email = student_email_entry.get()
        student_id = int(id_entry.get())

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (student_id, name, age, email) 
            VALUES (?, ?, ?, ?)
        ''', (student_id, name, age, email))

        conn.commit()
        student_window.destroy()
        refresh_treeview()  # Refresh the tree view to reflect the new data

    
    student_window = tk.Toplevel(main_tab)
    student_window.title("Add Student")
    student_window.geometry("300x500")
    
    student_name_label = tk.Label(student_window, text="Name")
    student_name_label.pack(pady=5)
    student_name_entry = tk.Entry(student_window)
    student_name_entry.pack(pady=5)

    age_label = tk.Label(student_window, text="Age")
    age_label.pack(pady=5)
    age_entry = tk.Entry(student_window)
    age_entry.pack(pady=5)

    id_label = tk.Label(student_window, text="Student ID")
    id_label.pack(pady=5)
    id_entry = tk.Entry(student_window)
    id_entry.pack(pady=5)

    student_email_label = tk.Label(student_window, text="Email")
    student_email_label.pack(pady=5)
    student_email_entry = tk.Entry(student_window)
    student_email_entry.pack(pady=5)

    submit_button = tk.Button(student_window, text="Submit", command=add_student)
    submit_button.pack(pady=10)

def instructor_window():
    """
    Opens a new window in the UI to allow adding a new instructor to the database, including details such as 
    name, age, email, and instructor ID.
    
    :return: None
    :rtype: None
    """
    def add_instructor():
        name = instructor_name_entry.get()
        age = int(age_entry.get())
        email = instructor_email_entry.get()
        instructor_id = int(id_entry.get())

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO instructors (instructor_id, name, age, email)
            VALUES (?, ?, ?, ?)
        ''', (instructor_id, name, age, email))

        conn.commit()
        instructor_window.destroy()
        refresh_treeview()


    instructor_window = tk.Toplevel(main_tab)
    instructor_window.title("Add Instructor")
    instructor_window.geometry("300x500")
    
    instructor_name_label = tk.Label(instructor_window, text="Name")
    instructor_name_label.pack(pady=5)
    instructor_name_entry = tk.Entry(instructor_window)
    instructor_name_entry.pack(pady=5)

    age_label = tk.Label(instructor_window, text="Age")
    age_label.pack(pady=5)
    age_entry = tk.Entry(instructor_window)
    age_entry.pack(pady=5)

    id_label = tk.Label(instructor_window, text="Instructor ID")
    id_label.pack(pady=5)
    id_entry = tk.Entry(instructor_window)
    id_entry.pack(pady=5)

    instructor_email_label = tk.Label(instructor_window, text="Email")
    instructor_email_label.pack(pady=5)
    instructor_email_entry = tk.Entry(instructor_window)
    instructor_email_entry.pack(pady=5)

    submit_button = tk.Button(instructor_window, text="Submit", command=add_instructor)
    submit_button.pack(pady=10)

def course_window():
    """
    Opens a new window in the UI to allow adding a new course to the database, including details such as 
    course ID, course name, and instructor assignment.
    
    :return: None
    :rtype: None
    """
    def add_course():
        course_id = int(id_entry.get())
        course_name = course_name_entry.get()
        instructor_id = None

        cursor = conn.cursor()

        # Query the database for available instructors
        cursor.execute('SELECT instructor_id FROM instructors')
        available_instructors = cursor.fetchall()

        # Check if there are any instructors available and assign the first one if needed
        if available_instructors:
            instructor_id = available_instructors[0][0]  # Get the first instructor's ID

        # Insert the new course into the database
        cursor.execute('''
            INSERT INTO courses (course_id, course_name, instructor_id)
            VALUES (?, ?, ?)
        ''', (course_id, course_name, instructor_id))

        conn.commit()
        course_window.destroy()
        refresh_treeview()


    course_window = tk.Toplevel(main_tab)
    course_window.title("Add Course")
    course_window.geometry("300x200")

    id_label = tk.Label(course_window, text="Course ID:")
    id_label.pack(pady=5)
    id_entry = tk.Entry(course_window)
    id_entry.pack(pady=5)

    course_name_label = tk.Label(course_window, text="Course Name:")
    course_name_label.pack(pady=5)
    course_name_entry = tk.Entry(course_window)
    course_name_entry.pack(pady=5)

    submit_button = tk.Button(course_window, text="Submit", command=add_course)
    submit_button.pack(pady=10)

option_button_frame = tk.Frame(main_tab)
option_button_frame.pack(pady=10, anchor="ne")

save_button = tk.Button(option_button_frame, text="Backup Data", command=backup_data)
save_button.pack(side="right", padx=10)

add_button_frame = tk.Frame(main_tab)
add_button_frame.pack(pady=10, anchor="center")

student_button = tk.Button(add_button_frame, text="Add Student", command=student_window)
student_button.pack(side="left", padx=10)

instructor_button = tk.Button(add_button_frame, text="Add Instructor", command=instructor_window)
instructor_button.pack(side="left", padx=10)

course_button = tk.Button(add_button_frame, text="Add Course", command=course_window)
course_button.pack(side="left", padx=10)

def refresh_treeview():
    """
    Refreshes the Treeview UI element with the latest data from the database for students, instructors, and courses.
    
    :return: None
    :rtype: None
    """
    cursor = conn.cursor()

    # Clear the tree view
    for i in tree.get_children():
        tree.delete(i)

    # Display Students
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        tree.insert("", "end", values=("Student", row[1], row[2], row[0]))

    # Display Instructors
    cursor.execute("SELECT * FROM instructors")
    for row in cursor.fetchall():
        tree.insert("", "end", values=("Instructor", row[1], row[2], row[0]))

    # Display Courses
    cursor.execute("SELECT * FROM courses")
    for row in cursor.fetchall():
        tree.insert("", "end", values=("Course", row[1], "", row[0]))

def register_course():
    """
    Registers a student for a course in the database by adding a record to the 'enrollments' table. 
    Checks if the student and course exist and whether the student is already registered before inserting the data.
    
    :raises ValueError: If the student or course does not exist or if the student is already enrolled.
    :return: None
    :rtype: None
    """
    student_name = student_name_for_course_entry.get()
    course_name = selected_course.get()

    cursor = conn.cursor()

    # Find the student by name
    cursor.execute("SELECT student_id FROM students WHERE name = ?", (student_name,))
    student_row = cursor.fetchone()

    if not student_row:
        messagebox.showerror("Error", "Student not found.")
        return
    student_id = student_row[0]

    # Find the course by name
    cursor.execute("SELECT course_id FROM courses WHERE course_name = ?", (course_name,))
    course_row = cursor.fetchone()

    if not course_row:
        messagebox.showerror("Error", "Course not found.")
        return
    course_id = course_row[0]

    # Check if the student is already enrolled in the course
    cursor.execute("SELECT * FROM enrollments WHERE course_id = ? AND student_id = ?", (course_id, student_id))
    if cursor.fetchone():
        messagebox.showerror("Error", "Student is already enrolled in this course.")
        return

    # Register the student in the course
    cursor.execute("INSERT INTO enrollments (course_id, student_id) VALUES (?, ?)", (course_id, student_id))
    conn.commit()

    messagebox.showinfo("Success", f"Student {student_name} has been registered for the course {course_name}.")


course_registration_label = tk.Label(main_tab, text="Student Registration for Course", font=('Helvetica', 16, 'bold'), justify='left')
course_registration_label.pack(pady=10, anchor="w")

student_name_for_course_label = tk.Label(main_tab, text="Student Name", anchor="w")
student_name_for_course_label.pack(fill="x")

student_name_for_course_entry = tk.Entry(main_tab)
student_name_for_course_entry.pack(fill="x", pady=5)

selected_course = tk.StringVar(main_tab)
course_combobox = ttk.Combobox(main_tab, textvariable=selected_course)

course_dropdown_label = tk.Label(main_tab, text="Select Course", anchor="w")
course_dropdown_label.pack(fill="x")

course_combobox.pack(fill="x", pady=5)

register_button = tk.Button(main_tab, text="Register", command=register_course)
register_button.pack(pady=10, anchor="w")

selected_course_for_instructor = tk.StringVar(main_tab)
course_combobox_for_instructor = ttk.Combobox(main_tab, textvariable=selected_course_for_instructor)

def assign_instructor_to_course():
    """
    Assigns an instructor to a course in the database by updating the 'courses' table with the instructor's ID.
    
    :raises ValueError: If the instructor or course does not exist.
    :return: None
    :rtype: None
    """
    instructor_name = instructor_name_for_course_entry.get()
    selected_course_name = selected_course_for_instructor.get()

    cursor = conn.cursor()

    # Find the instructor by name
    cursor.execute("SELECT instructor_id FROM instructors WHERE name = ?", (instructor_name,))
    instructor_row = cursor.fetchone()

    if not instructor_row:
        messagebox.showerror("Error", "Instructor not found.")
        return
    instructor_id = instructor_row[0]

    # Find the course by name
    cursor.execute("SELECT course_id FROM courses WHERE course_name = ?", (selected_course_name,))
    course_row = cursor.fetchone()

    if not course_row:
        messagebox.showerror("Error", "Course not found.")
        return
    course_id = course_row[0]

    # Assign the instructor to the course
    cursor.execute("UPDATE courses SET instructor_id = ? WHERE course_id = ?", (instructor_id, course_id))
    conn.commit()

    messagebox.showinfo("Success", f"Instructor {instructor_name} has been assigned to the course {selected_course_name}.")

instructor_assignment_label = tk.Label(main_tab, text="Instructor Assignment to Course", font=('Helvetica', 16, 'bold'), anchor="w")
instructor_assignment_label.pack(pady=(20, 10), anchor="w")

instructor_name_for_course_label = tk.Label(main_tab, text="Instructor Name", anchor="w")
instructor_name_for_course_label.pack(fill="x")

instructor_name_for_course_entry = tk.Entry(main_tab)
instructor_name_for_course_entry.pack(fill="x", pady=5)

selected_course_for_instructor = tk.StringVar(main_tab)
course_combobox_for_instructor = ttk.Combobox(main_tab, textvariable=selected_course_for_instructor)

course_dropdown_for_instructor_label = tk.Label(main_tab, text="Select Course", anchor="w")
course_dropdown_for_instructor_label.pack(fill="x")

course_combobox_for_instructor.pack(fill="x", pady=5)

assign_instructor_button = tk.Button(main_tab, text="Assign", command=assign_instructor_to_course)
assign_instructor_button.pack(pady=10, anchor="w")

def refresh_treeview():
    display_records()

def delete_record():
    """
    Deletes a selected record from the database (student, instructor, or course) and refreshes the UI. 
    Ensures associated enrollments or course assignments are properly handled.
    
    :raises sqlite3.Error: If there is an issue deleting the record.
    :return: None
    :rtype: None
    """
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a record to delete.")
        return
    
    # Get the selected item's values
    item = tree.item(selected_item)
    values = item['values']
    record_type = values[0]  # Either "Student", "Instructor", or "Course"
    record_id = values[3]    # ID of the selected record (student_id, instructor_id, or course_id)

    cursor = conn.cursor()

    try:
        if record_type == "Student":
            # Delete student from the students table
            cursor.execute("DELETE FROM students WHERE student_id = ?", (record_id,))
            
            # Delete related enrollments from the enrollments table
            cursor.execute("DELETE FROM enrollments WHERE student_id = ?", (record_id,))

        elif record_type == "Instructor":
            # Delete instructor from the instructors table
            cursor.execute("DELETE FROM instructors WHERE instructor_id = ?", (record_id,))
            
            # Unassign the instructor from any courses they were assigned to
            cursor.execute("UPDATE courses SET instructor_id = NULL WHERE instructor_id = ?", (record_id,))

        elif record_type == "Course":
            # Delete course from the courses table
            cursor.execute("DELETE FROM courses WHERE course_id = ?", (record_id,))
            
            # Delete related enrollments from the enrollments table
            cursor.execute("DELETE FROM enrollments WHERE course_id = ?", (record_id,))

        conn.commit()
        refresh_treeview()
        messagebox.showinfo("Success", f"{record_type} record deleted successfully!")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while deleting: {e}")

def edit_record_popup():
    """
    Opens a popup window to edit the selected record (student, instructor, or course) in the database. 
    Updates the record and refreshes the UI upon saving changes.
    
    :return: None
    :rtype: None
    """
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a record to edit.")
        return
    
    item = tree.item(selected_item)
    values = item['values']
    record_type = values[0]  # Either "Student", "Instructor", or "Course"
    record_id = values[3]    # ID of the selected record (student_id, instructor_id, or course_id)

    cursor = conn.cursor()

    # Fetch the current record from the database
    if record_type == "Student":
        cursor.execute("SELECT * FROM students WHERE student_id = ?", (record_id,))
        record = cursor.fetchone()
        if not record:
            messagebox.showerror("Error", "Student not found.")
            return

        # record contains (student_id, name, age, email)
        name, age, email = record[1], record[2], record[3]

    elif record_type == "Instructor":
        cursor.execute("SELECT * FROM instructors WHERE instructor_id = ?", (record_id,))
        record = cursor.fetchone()
        if not record:
            messagebox.showerror("Error", "Instructor not found.")
            return

        # record contains (instructor_id, name, age, email)
        name, age, email = record[1], record[2], record[3]

    elif record_type == "Course":
        cursor.execute("SELECT * FROM courses WHERE course_id = ?", (record_id,))
        record = cursor.fetchone()
        if not record:
            messagebox.showerror("Error", "Course not found.")
            return

        # record contains (course_id, course_name, instructor_id)
        course_name, instructor_id = record[1], record[2]

    # Create a popup window for editing the selected record
    popup = tk.Toplevel(root)
    popup.title(f"Edit {record_type}")
    popup.geometry("300x400")

    # Labels and Entry fields for editing
    name_label = tk.Label(popup, text="Name:")
    name_label.pack(pady=5)
    name_entry = tk.Entry(popup)
    name_entry.pack(pady=5)
    name_entry.insert(0, name)  # Prepopulate with the current name

    if record_type == "Student" or record_type == "Instructor":
        age_label = tk.Label(popup, text="Age:")
        age_label.pack(pady=5)
        age_entry = tk.Entry(popup)
        age_entry.pack(pady=5)
        age_entry.insert(0, age)

        email_label = tk.Label(popup, text="Email:")
        email_label.pack(pady=5)
        email_entry = tk.Entry(popup)
        email_entry.pack(pady=5)
        email_entry.insert(0, email)

    elif record_type == "Course":
        id_label = tk.Label(popup, text="Course ID:")
        id_label.pack(pady=5)
        id_entry = tk.Entry(popup)
        id_entry.pack(pady=5)
        id_entry.insert(0, record_id)

    def save_changes():
        # Get updated values from the entry fields
        updated_name = name_entry.get()

        if record_type == "Student" or record_type == "Instructor":
            updated_age = int(age_entry.get())
            updated_email = email_entry.get()

        if record_type == "Student":
            # Update the student record in the database
            cursor.execute('''
                UPDATE students 
                SET name = ?, age = ?, email = ?
                WHERE student_id = ?
            ''', (updated_name, updated_age, updated_email, record_id))

        elif record_type == "Instructor":
            # Update the instructor record in the database
            cursor.execute('''
                UPDATE instructors 
                SET name = ?, age = ?, email = ?
                WHERE instructor_id = ?
            ''', (updated_name, updated_age, updated_email, record_id))

        elif record_type == "Course":
            updated_course_name = name_entry.get()
            # Update the course record in the database
            cursor.execute('''
                UPDATE courses 
                SET course_name = ?
                WHERE course_id = ?
            ''', (updated_course_name, record_id))

        conn.commit()  # Commit the changes to the database
        refresh_treeview()  # Refresh the treeview to show the updated record
        popup.destroy()  # Close the popup window

    save_button = tk.Button(popup, text="Save Changes", command=save_changes)
    save_button.pack(pady=20)

def display_records(search_term=""):
    """
    Displays records in the Treeview UI element, filtered by a search term if provided. 
    Fetches students, instructors, and courses from the database.
    
    :param search_term: The term used to filter the records by name or ID, defaults to an empty string for no filter.
    :type search_term: str, optional
    :return: None
    :rtype: None
    """
    cursor = conn.cursor()

    # Clear the tree view
    for i in tree.get_children():
        tree.delete(i)

    search_term = search_term.lower()  # Case-insensitive search

    # Display Students
    cursor.execute("SELECT student_id, name, age FROM students WHERE LOWER(name) LIKE ? OR CAST(student_id AS TEXT) LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    for row in cursor.fetchall():
        tree.insert("", "end", values=("Student", row[1], row[2], row[0]))

    # Display Instructors
    cursor.execute("SELECT instructor_id, name, age FROM instructors WHERE LOWER(name) LIKE ? OR CAST(instructor_id AS TEXT) LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    for row in cursor.fetchall():
        tree.insert("", "end", values=("Instructor", row[1], row[2], row[0]))

    # Display Courses
    cursor.execute("SELECT course_id, course_name FROM courses WHERE LOWER(course_name) LIKE ? OR CAST(course_id AS TEXT) LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    for row in cursor.fetchall():
        tree.insert("", "end", values=("Course", row[1], "", row[0]))



def search_records():
    """
    Searches for records based on the input in the search bar and displays them in the UI.
    
    :return: None
    :rtype: None
    """
    search_term = search_entry.get() 
    display_records(search_term)

# Search and display widgets
search_entry = tk.Entry(records_tab)
search_entry.pack(pady=5, anchor="w", fill="x")

search_button = tk.Button(records_tab, text="Search", command=search_records)
search_button.pack(pady=5, anchor="w")

# Create Treeview widget in the "Records" tab
tree = ttk.Treeview(records_tab, columns=("Type", "Name", "Age", "ID"), show="headings")
tree.heading("Type", text="Type")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("ID", text="ID")
tree.pack(expand=True, fill="both")

# Add scrollbars to the Treeview
scrollbar_y = ttk.Scrollbar(records_tab, orient="vertical", command=tree.yview)
scrollbar_y.pack(side="right", fill="y")
tree.config(yscrollcommand=scrollbar_y.set)

button_frame = tk.Frame(records_tab)
button_frame.pack(pady=10)

edit_button = tk.Button(button_frame, text="Edit Record", command=edit_record_popup)
edit_button.pack(side="left", padx=10)

delete_button = tk.Button(button_frame, text="Delete Record", command=delete_record)
delete_button.pack(side="left", padx=10)

init_db()
update_course_combobox()
display_records()
root.mainloop()