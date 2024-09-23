import json
import re

# Part 1

# Step 1.1
class Person:
    """
    A base class representing a person with name, age, and email attributes.

    :param name: The name of the person.
    :type name: str
    :param age: The age of the person, must be a positive integer.
    :type age: int
    :param email: The email address of the person, must follow a valid email format.
    :type email: str
    :raises ValueError: If any of the provided parameters are invalid.
    """
    def __init__(self, name, age, email):
        """
        Initialize a new Person instance with name, age, and email.
        """
        # Validate name
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid name")
        
        # Validate age
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Invalid age")
        
        # Validate email using a strict regular expression
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        if not isinstance(email, str) or not re.match(email_regex, email):
            raise ValueError("Invalid email address")

        self.name = name
        self.age = age
        self.__email = email

    def introduce(self):
        """
        Prints a statement introducing the person with their name and age.

        :return: None
        :rtype: None
        """
        print(f"Hello, my name is {self.name}. I am {self.age} years old.")

# Step 1.2
class Student(Person):
    """
    A class representing a student, inheriting from Person, with additional student ID 
    and a list of registered courses.

    :param name: The name of the student.
    :type name: str
    :param age: The age of the student, must be a positive integer.
    :type age: int
    :param email: The email address of the student, must follow a valid email format.
    :type email: str
    :param student_id: The unique ID of the student, must be a positive integer.
    :type student_id: int
    :raises ValueError: If any of the provided parameters are invalid.
    """
    def __init__(self, name, age, email, student_id):
        """
        Initialize a new Student instance with name, age, email, and student ID.
        """
        if type(student_id) != int or student_id < 0:
            raise ValueError("Invalid data type for student_id")
        
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """
        Registers the student for a given course.

        :param course: The course object to register the student for.
        :type course: Course
        :raises ValueError: If the provided course is not of type Course.
        :return: None
        :rtype: None
        """
        if not isinstance(course, Course):
            raise ValueError("Invalid data type")
        self.registered_courses.append(course)

    def to_json(self):
        """
        Converts the student's details to a JSON string.

        :return: A JSON representation of the student.
        :rtype: json
        """
        return json.dumps({
            "name": self.name,
            "age": self.age,
            "email": self._Person__email,
            "student_id": self.student_id,
            "registered_courses": [course.course_name for course in self.registered_courses]
        })

# Step 1.3
class Instructor(Person):
    """
    A class representing an instructor, inheriting from Person, with additional instructor ID 
    and a list of assigned courses.

    :param name: The name of the instructor.
    :type name: str
    :param age: The age of the instructor, must be a positive integer.
    :type age: int
    :param email: The email address of the instructor, must follow a valid email format.
    :type email: str
    :param instructor_id: The unique ID of the instructor, must be a positive integer.
    :type instructor_id: int
    :raises ValueError: If any of the provided parameters are invalid.
    """
    def __init__(self, name, age, email, instructor_id):
        """
        Initialize a new Instructor instance with name, age, email, and instructor ID.
        """
        if type(instructor_id) != int or instructor_id < 0:
            raise ValueError("Invalid data type for instructor_id")
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """
        Assigns the instructor to teach a given course.

        :param course: The course object to assign the instructor to.
        :type course: Course
        :return: None
        :rtype: None
        """
        self.assigned_courses.append(course)

    def to_json(self):
        """
        Converts the instructor's details to a JSON string.

        :return: A JSON representation of the instructor.
        :rtype: josn
        """
        return json.dumps({
            "name": self.name,
            "age": self.age,
            "email": self._Person__email,
            "instructor_id": self.instructor_id,
            "assigned_courses": [course.course_name for course in self.assigned_courses]
        })

# Step 1.4
class Course:
    """
    A class representing a course with course ID, course name, an instructor, 
    and a list of enrolled students.

    :param course_id: The unique ID of the course, must be a positive integer.
    :type course_id: int
    :param course_name: The name of the course.
    :type course_name: str
    :param instructor: The instructor assigned to teach the course.
    :type instructor: Instructor
    :raises ValueError: If any of the provided parameters are invalid.
    """
    def __init__(self, course_id, course_name, instructor):
        """
        Initialize a new Course instance with course ID, course name, and instructor.
        """
        if type(course_id) != int or course_id < 0:
            raise ValueError("Invalid data type for course_id")
        
        if type(course_name) != str or not course_name.strip():
            raise ValueError("Invalid data type for course_name")
        
        if not isinstance(instructor, Instructor):
            raise ValueError("Invalid data type for instructor")

        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        """
        Adds a student to the course's enrolled student list.

        :param student: The student object to enroll in the course.
        :type student: Student
        :raises ValueError: If the provided student is not of type Student.
        :return: None
        :rtype: None
        """
        if not isinstance(student, Student):
            raise ValueError("Invalid data type for student")
        self.enrolled_students.append(student)

    def to_json(self):
        """
        Converts the course details to a JSON string, including the instructor and enrolled students.

        :return: A JSON representation of the course.
        :rtype: json
        """
        return json.dumps({
            "course_id": self.course_id,
            "course_name": self.course_name,
            "instructor_id": self.instructor.to_json(),
            "enrolled_students": [student.name for student in self.enrolled_students]
        })
