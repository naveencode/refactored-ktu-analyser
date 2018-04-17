from app import db
from sqlalchemy import and_, or_

class Exam(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    students = db.relationship("Student", backref="exam", lazy=True)

    def __repr__(self):
        return '<#id{} {}>\n'.format(self.id, self.name)

    # def add_exam(self, name):
    #     e = Exam(name=name)
    #     db.session.add(e)
    #     db.session.commit()


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    register_no = db.Column(db.String(15), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey("colleges.id"), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)
    sgpa = db.Column(db.Float)
    results = db.relationship("Result", backref="student", lazy=True)

    # def add_student(self, register_no, department_id, college_id):
    #     s = Student(register_no=register_no, department_id=department_id, college_id=college_id)
    #     db.session.add(s)
    #     db.session.commit()
    def __repr__(self):
        return '<{}>\n'.format(self.register_no)

    def find_sgpa(self):
        all_courses = self.results
        creditsum = 0
        total = 0
        for i in all_courses:
            credit = Course.query.get(i.course_id).credit
            point = Grade.query.get(i.grade_id).point
            creditsum += credit
            total += (credit*point)
        if creditsum == 0:
            self.sgpa = 0.0
            return
        
        self.sgpa = (total/creditsum)

        


class Result(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey("grades.id"), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)
    

    # def add_result(self, student_id, course_id, grade_id):
    #     r = Result(student_id=student_id, course_id=course_id, grade_id=grade_id)
    #     db.session.add(r)
    #     db.session.commit()
    def __repr__(self):
        return '<id#{} result row>\n'.format(self.student_id)


class Grade(db.Model):
    __tablename__ = "grades"    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(15), nullable=False)
    point = db.Column(db.Float, nullable=False)

    # def add_grade(self, symbol, point):
    #     g = Grade(symbol=symbol, point=point)
    #     db.session.add(g)
    #     db.session.commit()
    def __repr__(self):
        return '<id#{} Grade {}>\n'.format(self.id, self.symbol)

class College(db.Model):
    __tablename__ = "colleges"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # def add_college(self, name):
    #     c = College(name=name)
    #     db.session.add(c)
    #     db.session.commit()

    def clg_passpercent(self, exam_id):
        depts = Department.query.all()
        for dept in depts:
            dept.dept_passpercent(college_id=self.id, exam_id=exam_id)
        
        deptranks = DepartmentRank.query.filter(and_(DepartmentRank.college_id==self.id, DepartmentRank.exam_id==exam_id)).all()
        cr = CollegeRank(college_id=self.id, exam_id=exam_id)
        failed = 0
        total = 0
        for rank in deptranks:
            total += rank.total
            failed += rank.failed
        if total > 0:
            cr.total = total
            cr.failed = failed
            cr.pass_percent = ((total-failed)*100)/total
            db.session.add(cr)
            db.session.commit()


        

    def __repr__(self):
        return '<id#{} {}>\n'.format(self.id, self.name)


class Department(db.Model):
    __tablename__ = "departments"    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def dept_passpercent(self, college_id, exam_id):
        
        students = Student.query.filter(and_(Student.college_id == college_id, Student.exam_id == exam_id, Student.department_id == self.id))

        dr = DepartmentRank(department_id=self.id, college_id=college_id, exam_id=exam_id)
        
        failed = 0
        total = 0
        for s in students:
            total = total + 1
            r = s.results
            for i in r:
                # Warning: Table dependence!
                if not(Grade.query.get(i.grade_id).id in [1,2,3,4,5,6,7]):
                    failed = failed + 1
                    break
        if total > 0:
            dr.pass_percent = ((total-failed)*100)/total
            dr.total = total
            dr.failed = failed
            db.session.add(dr)
            db.session.commit()
            

    def __repr__(self):
        return '<id#{} {}>\n'.format(self.id, self.name)


class DepartmentRank(db.Model):
    __tablename__ = "departmentranks"
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey("colleges.id"), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)
   

    total = db.Column(db.Integer, nullable=False)
    failed = db.Column(db.Integer, nullable=False)

    pass_percent = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<id#{} d#{} c#{} {}%>\n'.format(self.id, self.department_id, self.college_id, self.pass_percent)

    

class CollegeRank(db.Model):
    __tablename__ = "collegeranks"
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey("colleges.id"), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)

    total = db.Column(db.Integer, nullable=False)
    failed = db.Column(db.Integer, nullable=False)

    pass_percent = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return '<id#{} c#{} {}%>\n'.format(self.id, self.college_id, self.pass_percent)

class Course(db.Model):
    __tablename__ = "courses"    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(15), nullable=False)
    credit = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<id#{} Course {}>\n'.format(self.id, self.code)
    # def add_course(self, code, credit):
    #     c = Course(code=code, credit=credit)
    #     db.session.add(c)
    #     db.session.commit()

            