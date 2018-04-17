with open('student.csv') as f:
	reader = csv.reader(f, delimiter=',')
	for row in reader:
		r = Student(register_no=row[0], department_id=row[1], college_id=row[2], exam_id=row[3])
		db.session.add(r)

with open('result_list.csv') as f:
	reader = csv.reader(f, delimiter=',')
	for row in reader:
		r = Result(student_id=row[0], course_id=row[1], grade_id=row[2], exam_id=row[3])
		db.session.add(r)

