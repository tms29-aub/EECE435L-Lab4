import tkinter as tk
import json

from tkinter import ttk
from tkinter import messagebox

from classes import Student, Instructor, Course

# Part 2

# Step 1
root = tk.Tk()
root.title('School Management System')
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

main_tab = tk.Frame(notebook)
records_tab = tk.Frame(notebook)

notebook.add(main_tab, text="Main")
notebook.add(records_tab, text="Records")

# Step 2
students = []
instructors = []
courses = []

# sample_student = Student("John", 25, "p3J8Z@example.com", 1)
# sample_instructor = Instructor("Jane", 30, "p3J8Z@example.com", 1)
# sample_course = Course(1, "Math", sample_instructor)
# students.append(sample_student)
# instructors.append(sample_instructor)
# courses.append(sample_course) 

DATA_FILE = "data.json"

def update_course_combobox():
    """
    Updates the combobox elements in the UI with the latest list of available courses from the courses list.
    
    :return: None
    :rtype: None
    """
    course_combobox['values'] = [course.course_name for course in courses]
    if courses:
        course_combobox.set(courses[0].course_name)  # Set default value to first course
        course_combobox_for_instructor.set(courses[0].course_name)
    else:
        course_combobox.set("No Courses Available")


def save_data():
    """
    Saves the students, instructors, and courses data to a JSON file. This includes information about enrolled students 
    and assigned instructors for courses.
    
    :raises IOError: If there is an issue writing to the file.
    :return: None
    :rtype: None
    """
    data = {
        "students": [json.loads(student.to_json()) for student in students],
        "instructors": [json.loads(instructor.to_json()) for instructor in instructors],
        "courses": [
            {
                "course_id": course.course_id,
                "course_name": course.course_name,
                "instructor": json.loads(course.instructor.to_json()) if course.instructor else None,  
                "enrolled_students": [json.loads(student.to_json()) for student in course.enrolled_students] 
            } for course in courses
        ]
    }

    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Success", "Data saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving: {e}")

# Function to load data from JSON file and populate the lists
def load_data():
    """
    Loads students, instructors, and courses data from a JSON file and populates the application with the loaded data. 
    Also reassigns enrolled students to their respective courses.
    
    :raises FileNotFoundError: If the data file does not exist.
    :raises IOError: If there is an issue reading from the file.
    :return: None
    :rtype: None
    """
    global students, instructors, courses

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        # Load students
        students = [
            Student(student['name'], student['age'], student['email'], student['student_id'])
            for student in data.get("students", [])
        ]

        # Load instructors
        instructors = [
            Instructor(instructor['name'], instructor['age'], instructor['email'], instructor['instructor_id'])
            for instructor in data.get("instructors", [])
        ]

        # Load courses 
        courses = [
            Course(
                course['course_id'],
                course['course_name'],
                Instructor(course['instructor']['name'], course['instructor']['age'], course['instructor']['email'], course['instructor']['instructor_id'])
            ) for course in data.get("courses", [])
        ]

        # Re-link enrolled students to courses
        for course_data, course in zip(data.get("courses", []), courses):
            for student_data in course_data['enrolled_students']:
                student = next((s for s in students if s.student_id == student_data['student_id']), None)
                if student:
                    course.add_student(student)  # Re-enroll the student

        refresh_treeview()  
        update_course_combobox()

        messagebox.showinfo("Success", "Data loaded successfully!")
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No saved data found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading: {e}")


def student_window():
    """
    Opens a new window in the UI to allow adding a new student to the application, including their name, age, email, 
    and student ID.
    
    :return: None
    :rtype: None
    """
    def add_student():
        name = student_name_entry.get()
        age = int(age_entry.get())  
        email = student_email_entry.get()
        student_id = int(id_entry.get())

        students.append(Student(name, age, email, student_id))  
        student_window.destroy()
    
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
    Opens a new window in the UI to allow adding a new instructor to the application, including their name, age, email, 
    and instructor ID.
    
    :return: None
    :rtype: None
    """
    def add_instructor():
        name = instructor_name_entry.get()
        age = int(age_entry.get())
        email = instructor_email_entry.get()
        instructor_id = int(id_entry.get())

        instructors.append(Instructor(name, age, email, instructor_id))  
        instructor_window.destroy()

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
    Opens a new window in the UI to allow adding a new course to the application, including its course ID and course name. 
    Assigns the first available instructor by default.
    
    :return: None
    :rtype: None
    """
    def add_course():
        course_id = int(id_entry.get())
        course_name = course_name_entry.get()

        instructor = instructors[0] if instructors else None  
        courses.append(Course(course_id, course_name, instructor))
        course_window.destroy()

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

save_button = tk.Button(option_button_frame, text="Save Data", command=save_data)
save_button.pack(side="right", padx=10)

load_button = tk.Button(option_button_frame, text="Load Data", command=load_data)
load_button.pack(side="right", padx=10)

add_button_frame = tk.Frame(main_tab)
add_button_frame.pack(pady=10, anchor="center")

student_button = tk.Button(add_button_frame, text="Add Student", command=student_window)
student_button.pack(side="left", padx=10)

instructor_button = tk.Button(add_button_frame, text="Add Instructor", command=instructor_window)
instructor_button.pack(side="left", padx=10)

course_button = tk.Button(add_button_frame, text="Add Course", command=course_window)
course_button.pack(side="left", padx=10)

# Step 3
def register_course():
    """
    Registers a student for a course by adding the student to the course's enrolled students list. Ensures the student and 
    course exist before enrollment.
    
    :raises ValueError: If the student or course is not found.
    :return: None
    :rtype: None
    """
    student_name = student_name_for_course_entry.get()
    course_name = selected_course.get()

    student = None
    course = None

    # Find the student and course objects by name
    for s in students:
        if s.name == student_name:
            student = s
            break

    for c in courses:
        if c.course_name == course_name:
            course = c
            break

    if student and course:
        course.add_student(student)


course_registration_label = tk.Label(main_tab, text="Student Registration for Course", font=('Helvetica', 16, 'bold'), justify='left')
course_registration_label.pack(pady=10, anchor="w")

student_name_for_course_label = tk.Label(main_tab, text="Student Name", anchor="w")
student_name_for_course_label.pack(fill="x")

student_name_for_course_entry = tk.Entry(main_tab)
student_name_for_course_entry.pack(fill="x", pady=5)

# Dropdown for selecting a course
selected_course = tk.StringVar(main_tab)
course_combobox = ttk.Combobox(main_tab, textvariable=selected_course)

if courses:
    course_combobox['values'] = [course.course_name for course in courses]
    selected_course.set(courses[0].course_name)  # Set default value to first course
else:
    course_combobox['values'] = ["No Courses Available"]
    selected_course.set("No Courses Available")

course_dropdown_label = tk.Label(main_tab, text="Select Course", anchor="w")
course_dropdown_label.pack(fill="x")

course_combobox.pack(fill="x", pady=5)

register_button = tk.Button(main_tab, text="Register", command=register_course)
register_button.pack(pady=10, anchor="w")

# Step 4
def assign_instructor_to_course():
    """
    Assigns an instructor to a course by setting the course's instructor field. Ensures both the instructor and course exist 
    before assignment.
    
    :raises ValueError: If the instructor or course is not found.
    :return: None
    :rtype: None
    """
    instructor_name = instructor_name_for_course_entry.get()
    selected_course_name = selected_course_for_instructor.get()

    instructor = None
    course = None

    # Find the instructor and course objects by name
    for i in instructors:
        if i.name == instructor_name:
            instructor = i
            break

    for c in courses:
        if c.course_name == selected_course_name:
            course = c
            break  

    if instructor and course:
        course.instructor = instructor

instructor_assignment_label = tk.Label(main_tab, text="Instructor Assignment to Course", font=('Helvetica', 16, 'bold'), anchor="w")
instructor_assignment_label.pack(pady=(20, 10), anchor="w")

instructor_name_for_course_label = tk.Label(main_tab, text="Instructor Name", anchor="w")
instructor_name_for_course_label.pack(fill="x")

instructor_name_for_course_entry = tk.Entry(main_tab)
instructor_name_for_course_entry.pack(fill="x", pady=5)

# Dropdown for selecting a course for the instructor
selected_course_for_instructor = tk.StringVar(main_tab)
course_combobox_for_instructor = ttk.Combobox(main_tab, textvariable=selected_course_for_instructor)

if courses:
    course_combobox_for_instructor['values'] = [course.course_name for course in courses]
    selected_course_for_instructor.set(courses[0].course_name)  # Set default value to first course
else:
    course_combobox_for_instructor['values'] = ["No Courses Available"]
    selected_course_for_instructor.set("No Courses Available")

course_dropdown_for_instructor_label = tk.Label(main_tab, text="Select Course", anchor="w")
course_dropdown_for_instructor_label.pack(fill="x")

course_combobox_for_instructor.pack(fill="x", pady=5)

assign_instructor_button = tk.Button(main_tab, text="Assign", command=assign_instructor_to_course)
assign_instructor_button.pack(pady=10, anchor="w")

def refresh_treeview():
    """
    Refreshes the Treeview UI element to display the most up-to-date information about students, instructors, and courses.
    
    :return: None
    :rtype: None
    """
    display_records()

# Step 5
def delete_record():
    """
    Deletes the selected record (student, instructor, or course) from the respective list and refreshes the UI. Ensures the 
    record exists before deletion.
    
    :raises ValueError: If no record is selected or if the record is not found.
    :return: None
    :rtype: None
    """
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a record to delete.")
        return
    
    item = tree.item(selected_item)
    values = item['values']
    record_type = values[0]

    if record_type == "Student":
        for student in students:
            if student.student_id == values[3]:
                students.remove(student)
                break
    elif record_type == "Instructor":
        for instructor in instructors:
            if instructor.instructor_id == values[3]:
                instructors.remove(instructor)
                break
    elif record_type == "Course":
        for course in courses:
            if course.course_id == values[2]:
                courses.remove(course)
                break
    
    refresh_treeview()

def edit_record_popup():
    """
    Opens a popup window to edit the selected student, instructor, or course. Updates the selected record with the new values 
    and refreshes the UI after saving.
    
    :raises ValueError: If no record is selected.
    :return: None
    :rtype: None
    """
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a record to edit.")
        return
    
    item = tree.item(selected_item)
    values = item['values']
    record_type = values[0]

    # Find the selected instance
    instance = None
    if record_type == "Student":
        for student in students:
            if student.student_id == values[3]:
                instance = student
                break
    elif record_type == "Instructor":
        for instructor in instructors:
            if instructor.instructor_id == values[3]:
                instance = instructor
                break
    elif record_type == "Course":
        for course in courses:
            if course.course_id == values[2]:
                instance = course
                break

    if not instance:
        return

    # Create a popup window for editing the selected record
    popup = tk.Toplevel(root)
    popup.title(f"Edit {record_type}")
    popup.geometry("300x400")

    # Labels and Entry fields for editing
    name_label = tk.Label(popup, text="Name:")
    name_label.pack(pady=5)
    name_entry = tk.Entry(popup)
    name_entry.pack(pady=5)
    name_entry.insert(0, instance.name)  # Prepopulate with the current name

    if record_type == "Student" or record_type == "Instructor":
        age_label = tk.Label(popup, text="Age:")
        age_label.pack(pady=5)
        age_entry = tk.Entry(popup)
        age_entry.pack(pady=5)
        age_entry.insert(0, instance.age)

    if record_type == "Student":
        id_label = tk.Label(popup, text="Student ID:")
        id_label.pack(pady=5)
        id_entry = tk.Entry(popup)
        id_entry.pack(pady=5)
        id_entry.insert(0, instance.student_id)

    elif record_type == "Instructor":
        id_label = tk.Label(popup, text="Instructor ID:")
        id_label.pack(pady=5)
        id_entry = tk.Entry(popup)
        id_entry.pack(pady=5)
        id_entry.insert(0, instance.instructor_id)

    elif record_type == "Course":
        id_label = tk.Label(popup, text="Course ID:")
        id_label.pack(pady=5)
        id_entry = tk.Entry(popup)
        id_entry.pack(pady=5)
        id_entry.insert(0, instance.course_id)

    def save_changes():
        # Update instance with new values
        instance.name = name_entry.get()

        if record_type == "Student" or record_type == "Instructor":
            instance.age = int(age_entry.get())

        if record_type == "Student":
            instance.student_id = int(id_entry.get())
        elif record_type == "Instructor":
            instance.instructor_id = int(id_entry.get())
        elif record_type == "Course":
            instance.course_id = int(id_entry.get())

        refresh_treeview()
        popup.destroy()

    save_button = tk.Button(popup, text="Save Changes", command=save_changes)
    save_button.pack(pady=20)

def display_records(search_term=""):
    """
    Displays the records (students, instructors, courses) in the Treeview UI element, filtered by the provided search term. 
    Searches by name or ID.
    
    :param search_term: The term used to filter the records by name or ID, defaults to an empty string for no filter.
    :type search_term: str, optional
    :return: None
    :rtype: None
    """
    # Clear the tree
    for i in tree.get_children():
        tree.delete(i)

    search_term = search_term.lower()  # Case-insensitive search

    # Display Students
    for student in students:
        if search_term in student.name.lower() or search_term in str(student.student_id).lower():
            tree.insert("", "end", values=("Student", student.name, student.age, student.student_id))

    # Display Instructors
    for instructor in instructors:
        if search_term in instructor.name.lower() or search_term in str(instructor.instructor_id).lower():
            tree.insert("", "end", values=("Instructor", instructor.name, instructor.age, instructor.instructor_id))

    # Display Courses
    for course in courses:
        if search_term in course.course_name.lower() or search_term in str(course.course_id).lower():
            tree.insert("", "end", values=("Course", course.course_name, "", course.course_id))

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

display_records()

root.mainloop()
