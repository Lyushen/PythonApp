import copy

class Course:
    """A class to represent a course."""
    def __init__(self, name, topics):
        self.name = name
        self.topics = topics  # A list of topics, which is a mutable object

class Student:
    """A class to represent a student."""
    def __init__(self, name, age, courses):
        self.name = name
        self.age = age
        self.courses = courses  # A list of Course instances, demonstrating nested objects

    def __repr__(self):
        return f"Student({self.name}, {self.age}, {[course.name for course in self.courses]})"

# Creating a student with courses
course1 = Course("Mathematics", ["Algebra", "Calculus"])
course2 = Course("Physics", ["Mechanics", "Optics"])
student1 = Student("John Doe", 20, [course1, course2])

# Creating a deep copy of the student
student2 = copy.deepcopy(student1)

# Modifying the copy's attributes and nested objects
student2.name = "Jane Doe"
student2.courses[0].name = "Advanced Mathematics"

# Original student is unaffected by changes in the copy
print("Original:", student1)
print("Deep Copy:", student2)