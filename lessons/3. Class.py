from traceback import print_tb


class Student:
    def __init__(self, name):
        self.name = name
        self.height = 170

student = Student('Seb')

print(student.name)
print(student.height)