import csv
import re

# how about we get all the college and departement names form the csv itself
def id_index(name):
    name = name.replace(" ", "")
    if name in student_index:
        return student_index.index(name)+1
    else:
        print("id error"+name)
        exit()

def course_index(name):
    name = name.replace(" ", "")
    if name in courses:
        return courses.index(name)+1
    else:
        print("course error"+name)
        exit()

def grade_index(name):
    name = name.replace(" ", "")
    if name in grades:
        return grades.index(name)+1
    else:
        print("grade error"+name)
        exit()



def dept_index(name):
    name = name.replace(" ", "")
    if name in department:
        return department.index(name)+1
    for dep in department:
        if re.search(name, dep):
            return department.index(dep)+1
    else:
        print("error dept "+name)
        exit()
        return -1

def clg_index(name):
    
    name = name.replace(" ", "")
    if (name in colleges):
        return colleges.index(name)+1

    for cg in colleges:
        if re.search(name, cg):
            return colleges.index(cg)+1
    else:
        print(list(enumerate(colleges,1)))
        print("error clg "+name)
        exit()        
        return -1


department = []
with open('dept.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for dept in reader:
        department.append(dept[0].replace(" ", ""))

# for r in (list(enumerate(department, 1))):
#     print(r)

colleges = []
with open('college.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for clg in reader:
        colleges.append(clg[0].replace(" ", ""))

courses = []
with open('course.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for course in reader:
        courses.append(course[0].replace(" ", ""))

grades = []
with open('grade.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for grade in reader:
        grades.append(grade[0].replace(" ", ""))

# for r in (list(enumerate(colleges, 1))):
#     print(r)

row = []
with open('result1.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for regno, deptname, course, grade, college in reader:
        row.append(regno+','+str(dept_index(deptname))+','+str(clg_index(college))+','+str(course_index(course))+','+str(grade_index(grade)))

t = []
with open('result1.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for regno, deptname, course, grade, college in reader:
        t.append(regno+','+str(dept_index(deptname))+','+str(clg_index(college)))


result = list(map(lambda s: s.split(','), row))
row = sorted(list(set(t)))

student_index = []


split_row = []
for r in row:
    split_row.append(r.split(',')[:3])
    student_index.append(r.split(',')[0])
print(student_index)

exam_id = int(input("Enter exam id:"))
with open('student.csv', 'w') as o:
    writer = csv.writer(o, delimiter=',')
    for r in split_row:
        writer.writerow([r[0],r[1],r[2],exam_id])

memo = {}
with open('result_list.csv', 'w') as o:
    writer = csv.writer(o, delimiter=',')
    for r in result:
        if r[0] in memo:
            writer.writerow([memo[r[0]],r[3], r[4], exam_id])
        else:
            memo[r[0]] = id_index(r[0])
            writer.writerow([memo[r[0]],r[3], r[4], exam_id])
        
