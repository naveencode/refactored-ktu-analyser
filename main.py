from app import app, db
from app.models import Exam, Student, Result, Grade, College, Department, Course, DepartmentRank, CollegeRank


# first app is the package name and the second 
# is a variable inside the package

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Exam': Exam, 'Student': Student, 'Result': Result,
            'Grade': Grade, 'College': College, 'Department': Department,
            'Course': Course, 'DepartmentRank': DepartmentRank, 'CollegeRank': CollegeRank}