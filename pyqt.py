import subprocess
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QTableWidgetSelectionRange,
    QMessageBox,
    QFileDialog,
    QInputDialog,
)
import json
import re 
import sqlite3
from sqlalchemy import (
    MetaData,
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session


def connect_to_mysql():
    """
    Connect to a MySQL database and create tables based on models.

    This function establishes a connection to a MySQL database using SQLAlchemy's 
    `create_engine` and creates the tables defined in the models using `Base.metadata.create_all`.

    :return: The SQLAlchemy engine instance connected to the MySQL database.
    :rtype: sqlalchemy.engine.base.Engine

    :raises sqlalchemy.exc.SQLAlchemyError: If there is an issue connecting to the MySQL database.
    """
    engine = create_engine("mysql+pymysql://root:Aub123@localhost/school")
    Base.metadata.create_all(engine)  # This creates the tables based on the models
    return engine


# Base class for all ORM models
Base = declarative_base()
engine = connect_to_mysql()
Session = scoped_session(sessionmaker(bind=engine))


class Person(Base):
    """
    A base class representing a person.

    This class defines common attributes and methods shared by both `Student` and `Instructor`.
    It uses SQLAlchemy to define database table columns and manage relationships.

    :param id: Unique identifier for the person, auto-incremented.
    :type id: int
    :param name: The name of the person.
    :type name: str
    :param age: The age of the person.
    :type age: int
    :param email: The email address of the person.
    :type email: str
    :param type: A string value indicating the type of person ('student' or 'instructor').
    :type type: str
    :return: A string introducing the person with their name and age.
    :rtype: str
    """

    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    email = Column(String(100), nullable=False)
    type = Column(String(50))
    
    __mapper_args__ = {"polymorphic_on": "type"}

    def introduce(self):
        """
        Return a string introducing the person.

        :return: A greeting with the person's name and age.
        :rtype: str
        """
        return f"Hello, my name is {self.name} and I am {self.age} years old."


class Student(Person):
    """
    A class representing a student, inheriting from `Person`.

    This class defines additional attributes for students, such as the courses they are registered in.

    :param student_id: Unique identifier for the student, related to the `persons.id`.
    :type student_id: int
    :param registered_courses: A relationship defining the courses in which the student is registered.
    :type registered_courses: list of `Course` objects
    """

    __tablename__ = "students"

    student_id = Column(Integer, ForeignKey("persons.id"), primary_key=True)
    registered_courses = relationship(
        "Course", secondary="registrations", back_populates="enrolled_students"
    )

    __mapper_args__ = {"polymorphic_identity": "student"}


class Instructor(Person):
    """
    A class representing an instructor, inheriting from `Person`.

    This class defines additional attributes for instructors, such as the courses they are assigned to teach.

    :param instructor_id: Unique identifier for the instructor, related to the `persons.id`.
    :type instructor_id: int
    :param assigned_courses: A relationship defining the courses assigned to the instructor.
    :type assigned_courses: list of `Course` objects
    """

    __tablename__ = "instructors"

    instructor_id = Column(Integer, ForeignKey("persons.id"), primary_key=True)
    assigned_courses = relationship("Course", back_populates="instructor")

    __mapper_args__ = {"polymorphic_identity": "instructor"}


class Course(Base):
    """
    A class representing a course.

    This class defines attributes and relationships associated with a course, including its instructor and enrolled students.

    :param course_id: Unique identifier for the course, auto-incremented.
    :type course_id: int
    :param course_name: The name of the course.
    :type course_name: str
    :param instructor_id: The identifier of the instructor teaching the course.
    :type instructor_id: int
    :param instructor: A relationship to the `Instructor` object teaching the course.
    :type instructor: Instructor
    :param enrolled_students: A relationship defining the students enrolled in the course.
    :type enrolled_students: list of `Student` objects
    """

    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(100), nullable=False)
    instructor_id = Column(Integer, ForeignKey("instructors.instructor_id"))
    instructor = relationship("Instructor", back_populates="assigned_courses")
    enrolled_students = relationship(
        "Student", secondary="registrations", back_populates="registered_courses"
    )


registrations = Table(
    "registrations",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.student_id")),
    Column("course_id", Integer, ForeignKey("courses.course_id")),
)


# Functions for validation

def validate_email(email):
    """
    Validate if the given email is in a valid format.

    This function uses a regular expression to check if the input email follows the standard format (e.g., `example@example.com`).

    :param email: The email address to be validated.
    :type email: str
    :return: True if the email is valid, False otherwise.
    :rtype: bool
    """
    return re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$", email)


def validate_age(age):
    """
    Validate if the given age is a non-negative integer.

    This function checks if the input is a digit and converts it to an integer to ensure it's non-negative.

    :param age: The age to be validated.
    :type age: str
    :return: True if the age is a non-negative integer, False otherwise.
    :rtype: bool
    """
    return age.isdigit() and int(age) >= 0


# Save and load data functions

def save_data(data, filename):
    """
    Save a list of objects to a file in JSON format.

    This function serializes a list of objects (using their `__dict__` attribute) and saves them to a JSON file.

    :param data: A list of objects to be saved.
    :type data: list
    :param filename: The name of the file where the data will be saved.
    :type filename: str
    :return: None
    """
    with open(filename, "w") as f:
        json.dump([obj.__dict__ for obj in data], f)


def load_data(filename):
    """
    Load data from a JSON file.

    This function reads data from a JSON file and returns it as a Python object.

    :param filename: The name of the file to be loaded.
    :type filename: str
    :return: The loaded data.
    :rtype: list
    """
    with open(filename, "r") as f:
        return json.load(f)

# PyQt Application
class SchoolManagementApp(QMainWindow):
    """
    A PyQt application for managing school data including students, instructors, courses, and records.

    This class defines the main window for the application, managing tabs, forms, tables, and backups.

    :param QMainWindow: Inherits from PyQt's QMainWindow.
    """
    def __init__(self):
        """
        Initializes the main window of the School Management System application.

        - Sets the window title and geometry.
        - Initializes the UI components by creating the main tabs and forms.
        - Loads initial data (instructors and table display).
        - Sets the MySQL dump path for backups.
        """
        super().__init__()

        # Main window properties
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)

        # Setup UI Components
        self.init_ui()
        self.load_initial_data()  # Add this line
        self.mysqldump_path = "mysqldump"

    def load_initial_data(self):
        """
        Loads the initial data for the dropdown and display table.
        
        - Updates the instructor dropdown with available instructors.
        - Refreshes the records table with current data from the database.
        """
        self.update_instructor_dropdown()
        self.update_display_table()

    def init_ui(self):
        """
        Initializes the user interface.

        - Sets up the tab widget as the central widget.
        - Creates the forms for students, instructors, and courses.
        - Creates the display table and backup buttons.
        """
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.create_student_form()
        self.create_instructor_form()
        self.create_course_form()
        self.create_display_table()
        self.create_backup_button()

    def create_student_form(self):
        """
        Creates the form for adding a student.

        The form includes input fields for student name, age, email, and ID, and a button to add the student.
        """
        student_tab = QWidget()
        layout = QVBoxLayout()

        self.student_name_input = QLineEdit()
        self.student_age_input = QLineEdit()
        self.student_email_input = QLineEdit()
        self.student_id_input = QLineEdit()

        layout.addWidget(QLabel("Student Name"))
        layout.addWidget(self.student_name_input)
        layout.addWidget(QLabel("Student Age"))
        layout.addWidget(self.student_age_input)
        layout.addWidget(QLabel("Student Email"))
        layout.addWidget(self.student_email_input)
        layout.addWidget(QLabel("Student ID"))
        layout.addWidget(self.student_id_input)

        add_student_btn = QPushButton("Add Student")
        add_student_btn.clicked.connect(self.add_student)
        layout.addWidget(add_student_btn)

        student_tab.setLayout(layout)
        self.tabs.addTab(student_tab, "Students")

    def create_instructor_form(self):
        """
        Creates the form for adding an instructor.

        The form includes input fields for instructor name, age, email, and ID, and a button to add the instructor.
        """
        instructor_tab = QWidget()
        layout = QVBoxLayout()

        self.instructor_name_input = QLineEdit()
        self.instructor_age_input = QLineEdit()
        self.instructor_email_input = QLineEdit()
        self.instructor_id_input = QLineEdit()

        layout.addWidget(QLabel("Instructor Name"))
        layout.addWidget(self.instructor_name_input)
        layout.addWidget(QLabel("Instructor Age"))
        layout.addWidget(self.instructor_age_input)
        layout.addWidget(QLabel("Instructor Email"))
        layout.addWidget(self.instructor_email_input)
        layout.addWidget(QLabel("Instructor ID"))
        layout.addWidget(self.instructor_id_input)

        add_instructor_btn = QPushButton("Add Instructor")
        add_instructor_btn.clicked.connect(self.add_instructor)
        layout.addWidget(add_instructor_btn)

        instructor_tab.setLayout(layout)
        self.tabs.addTab(instructor_tab, "Instructors")

    def create_course_form(self):
        """
        Creates the form for adding a course.

        The form includes input fields for the course name and a dropdown to select the instructor, and a button to add the course.
        """
        course_tab = QWidget()
        layout = QVBoxLayout()

        self.course_name_input = QLineEdit()
        self.instructor_dropdown = QComboBox()

        layout.addWidget(QLabel("Course Name"))
        layout.addWidget(self.course_name_input)
        layout.addWidget(QLabel("Select Instructor"))
        layout.addWidget(self.instructor_dropdown)

        add_course_btn = QPushButton("Add Course")
        add_course_btn.clicked.connect(self.add_course)
        layout.addWidget(add_course_btn)

        course_tab.setLayout(layout)
        self.tabs.addTab(course_tab, "Courses")

    def create_display_table(self):
        """
        Creates the table to display records of students, instructors, and courses.

        The table includes three columns: 'Type', 'Name', and 'ID'. A delete button allows removing selected records.
        """
        records_tab = QWidget()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Type", "Name", "ID"])

        delete_btn = QPushButton("Delete Selected Record")
        delete_btn.clicked.connect(self.delete_record)

        layout.addWidget(self.table)
        layout.addWidget(delete_btn)

        records_tab.setLayout(layout)
        self.tabs.addTab(records_tab, "Records")

    # Methods to add students, instructors, and courses
    def add_student(self):
        """
        Adds a new student to the database.

        - Validates the student's age and email.
        - Adds the student to the database.
        - Refreshes the display table with the new student data.

        Raises a warning if data is invalid.
        """
        name = self.student_name_input.text()
        age = self.student_age_input.text()
        email = self.student_email_input.text()
        student_id = self.student_id_input.text()

        if self.validate_age(age) and self.validate_email(email):
            session = Session()
            student = Student(
                name=name, age=int(age), email=email, student_id=int(student_id)
            )
            session.add(student)
            session.commit()
            session.close()
            self.update_display_table()
        else:
            QMessageBox.warning(self, "Invalid Data", "Please enter valid data")

    def add_instructor(self):
        """
        Adds a new instructor to the database.

        - Validates the instructor's age and email.
        - Adds the instructor to the database.
        - Updates the instructor dropdown and refreshes the display table.

        Raises a warning if data is invalid.
        """
        name = self.instructor_name_input.text()
        age = self.instructor_age_input.text()
        email = self.instructor_email_input.text()
        instructor_id = self.instructor_id_input.text()

        if self.validate_age(age) and self.validate_email(email):
            session = Session()
            instructor = Instructor(
                name=name, age=int(age), email=email, instructor_id=int(instructor_id)
            )
            session.add(instructor)
            session.commit()
            session.close()
            self.update_instructor_dropdown()
            self.update_display_table()
        else:
            QMessageBox.warning(self, "Invalid Data", "Please enter valid data")

    def add_course(self):
        """
        Adds a new course to the database.

        - Validates the course and instructor association.
        - Adds the course to the database.
        - Refreshes the display table with the new course data.

        Raises a warning if the instructor is invalid.
        """
        course_name = self.course_name_input.text()
        instructor_name = self.instructor_dropdown.currentText()

        session = Session()
        instructor = session.query(Instructor).filter_by(name=instructor_name).first()

        if instructor:
            course = Course(course_name=course_name, instructor=instructor)
            session.add(course)
            session.commit()
            session.close()
            self.update_display_table()
        else:
            QMessageBox.warning(
                self, "Invalid Instructor", "Please select a valid instructor"
            )

    def update_instructor_dropdown(self):
        """
        Updates the dropdown list of instructors with the latest data from the database.
        """
        session = Session()
        instructors = session.query(Instructor).all()
        instructor_names = [i.name for i in instructors]
        self.instructor_dropdown.clear()
        self.instructor_dropdown.addItems(instructor_names)
        session.close()

    def update_display_table(self):
        """
        Updates the display table with the current records of students, instructors, and courses from the database.
        """
        session = Session()
        self.table.setRowCount(0)

        students = session.query(Student).all()
        instructors = session.query(Instructor).all()
        courses = session.query(Course).all()

        for student in students:
            self.table.insertRow(self.table.rowCount())
            self.table.setItem(
                self.table.rowCount() - 1, 0, QTableWidgetItem("Student")
            )
            self.table.setItem(
                self.table.rowCount() - 1, 1, QTableWidgetItem(student.name)
            )
            self.table.setItem(
                self.table.rowCount() - 1, 2, QTableWidgetItem(str(student.student_id))
            )

        for instructor in instructors:
            self.table.insertRow(self.table.rowCount())
            self.table.setItem(
                self.table.rowCount() - 1, 0, QTableWidgetItem("Instructor")
            )
            self.table.setItem(
                self.table.rowCount() - 1, 1, QTableWidgetItem(instructor.name)
            )
            self.table.setItem(
                self.table.rowCount() - 1,
                2,
                QTableWidgetItem(str(instructor.instructor_id)),
            )

        for course in courses:
            self.table.insertRow(self.table.rowCount())
            self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem("Course"))
            self.table.setItem(
                self.table.rowCount() - 1, 1, QTableWidgetItem(course.course_name)
            )
            self.table.setItem(
                self.table.rowCount() - 1, 2, QTableWidgetItem(str(course.course_id))
            )

        session.close()

    def delete_record(self):
        """
        Deletes the selected record (student, instructor, or course) from the database.

        - Determines the type of record and removes it from the database.
        - Refreshes the display table with updated records.
        """
        current_row = self.table.currentRow()
        if current_row != -1:
            record_type = self.table.item(current_row, 0).text()
            record_id = int(self.table.item(current_row, 2).text())

            session = Session()

            if record_type == "Student":
                student = session.query(Student).filter_by(student_id=record_id).first()
                if student:
                    session.delete(student)
            elif record_type == "Instructor":
                instructor = (
                    session.query(Instructor).filter_by(instructor_id=record_id).first()
                )
                if instructor:
                    session.delete(instructor)
            elif record_type == "Course":
                course = session.query(Course).filter_by(course_id=record_id).first()
                if course:
                    session.delete(course)

            session.commit()
            session.close()
            self.update_display_table()

    def validate_age(self, age):
        """
        Validates if the given age is a digit.

        :param age: The age to validate.
        :type age: str
        :return: True if the age is valid, otherwise False.
        :rtype: bool
        """
        return age.isdigit()

    def validate_email(self, email):
        """
        Validates if the given email follows the correct email format.

        :param email: The email to validate.
        :type email: str
        :return: True if the email is valid, otherwise False.
        :rtype: bool
        """
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    # Create backup
    def create_backup_button(self):
        """
        Creates buttons for backup and restore functionality.

        - Adds a 'Backup Database' button to backup the current database state.
        - Adds a 'Restore Database' button to restore the database from a backup.
        """
        backup_tab = QWidget()
        layout = QVBoxLayout()

        backup_btn = QPushButton("Backup Database")
        backup_btn.clicked.connect(self.backup_database)
        layout.addWidget(backup_btn)

        restore_btn = QPushButton("Restore Database")
        restore_btn.clicked.connect(self.restore_database)
        layout.addWidget(restore_btn)

        backup_tab.setLayout(layout)
        self.tabs.addTab(backup_tab, "Backup/Restore")

    def backup_database(self):
        """
        Backs up the current database state to a JSON file.

        - Prompts the user to save the backup file.
        - Dumps all data from the database into a JSON file.
        - Shows a success message if the backup was successful.
        - Shows an error message if the backup failed.
        """
        try:
            backup_path, _ = QFileDialog.getSaveFileName(
                self, "Save Backup", "", "JSON Files (*.json);;All Files (*)"
            )
            if backup_path:
                metadata = MetaData()
                metadata.reflect(bind=engine)

                backup_data = {}
                session = Session()

                for table in metadata.sorted_tables:
                    backup_data[table.name] = [
                        {
                            column.name: getattr(row, column.name)
                            for column in table.columns
                        }
                        for row in session.query(table).all()
                    ]

                with open(backup_path, "w") as f:
                    json.dump(backup_data, f, indent=2, default=str)

                session.close()

                QMessageBox.information(
                    self,
                    "Backup Successful",
                    f"Database backup created at {backup_path}",
                )
        except Exception as e:
            QMessageBox.critical(self, "Backup Failed", f"An error occurred: {str(e)}")

    def restore_database(self):
        """
        Restores the database from a selected backup JSON file.

        - Prompts the user to select a backup file.
        - Restores the data from the file into the database.
        - Shows a success message if the restore was successful.
        - Shows an error message if the restore failed.
        """
        try:
            backup_path, _ = QFileDialog.getOpenFileName(
                self, "Open Backup", "", "JSON Files (*.json);;All Files (*)"
            )
            if backup_path:
                with open(backup_path, "r") as f:
                    backup_data = json.load(f)

                session = self.Session()
                metadata = MetaData()
                metadata.reflect(bind=self.engine)

                for table_name, rows in backup_data.items():
                    table = metadata.tables[table_name]
                    session.execute(table.delete())
                    for row in rows:
                        session.execute(table.insert().values(**row))

                session.commit()
                session.close()

                QMessageBox.information(
                    self,
                    "Restore Successful",
                    "Database has been restored from the backup.",
                )
                self.update_display_table()  # Refresh the display after restore
        except Exception as e:
            QMessageBox.critical(self, "Restore Failed", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementApp()
    window.show()
    sys.exit(app.exec_())
