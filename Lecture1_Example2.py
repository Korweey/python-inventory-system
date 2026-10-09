
"""
name=input("Enter Students Name:\t ")
student_id=input("Enter Students ID:\t ")
student_program=input("Enter Students Program:\t ")
try:
    tuition_fee=float(input("Enter Tuition Fee:\t$ "))
except:
    print("Enter a valid tuition amount")

print("*#*"*40)
print(f"student name:\t {name}")
print(f"student ID:\t {student_id}")
print(f"student is enrolled in:\t {student_program}")
print(f"tuition fee:\t$ {tuition_fee}")

print("--MK"*30)

print("Student name:\t {}".format(name))
print("Student ID:\t {}".format(student_id))
print("Student program:\t {}".format(student_program))
print("tuition fee:\t$ {}".format(tuition_fee))



import shutil

size=shutil.get_terminal_size()
column=size.columns

print(column)
print(size.lines)

name="Qawiyy Rabiu"
Student_ID="N10038749"

print(name.rjust(column))
print(Student_ID.rjust(column))

print("##"*60)

print(name.center(column))
print(Student_ID.center(column))

print("%#%"*40)

print(name.ljust(column))
print(Student_ID.ljust(column))


from dataclasses import dataclass
"""
name="Rabiu Qawiyy"
Student_ID="N10038749"
Program="Cloud Computing"
"""
header="%40s%40s%40s"%("name","Student_ID","Program Enrolled")
print(header)

data="%40s%40s%40s"%(name, Student_ID, Program)
print(data)
"""

###########################################################################

print(f"{'name':>40}{'Student_ID':>40}{'Program Enrolled':>40}")

print(f"{name:>40}{Student_ID:>40}{Program:>40}")