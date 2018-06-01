from flask import Flask, request
from flask import render_template
from flask import jsonify
from sqlalchemy import and_, or_

from app import app
from app.models import *


    # if exam is None:
    #     return "<h1> Error : Invalid exam id </h1>", 422


@app.route('/', methods=['POST', 'GET'], defaults={'exam_id': None, 'college_id': None, 'department_id': None})
@app.route("/exams/<int:exam_id>", defaults={'college_id': None, 'department_id': None})
@app.route("/exams/<int:exam_id>/colleges/<int:college_id>", defaults={'department_id': None})
@app.route("/exams/<int:exam_id>/colleges/<int:college_id>/departments/<int:department_id>")
def index(exam_id, college_id, department_id):

    exam_list = []
    data = []
    for exam in Exam.query.all():
        exam_list.append({'id': exam.id, 'name': exam.name})

    if(not exam_id and request.method == 'GET'):
        return render_template('base.html', exam_list=exam_list)
        

    if request.method == 'POST' or exam_id:
        if not exam_id:
            exam_id = request.form.get('exam')
        exam = Exam.query.get(exam_id)
        if college_id:
            college = College.query.get(college_id)
            if department_id:
                department = Department.query.get(department_id);
                exam_details = {'exam_name': exam.name, 'exam_id': exam.id, 'college_name': college.name, 'college_id': college.id,
                                'department_name': department.name, 'department_id': department.id}

                student_ranks = Student.query.filter(and_(Student.exam_id==exam_id,
                                            Student.college_id==college_id,
                                            Student.department_id==department_id)).all()
                for student in student_ranks:
                    data.append({
                        'name': student.register_no,
                        'value': student.sgpa
                    })

                table_details = {
                                'caption': exam.name + " | " + college.name + " | " + department.name,
                                'headers': ['Register No', 'SGPA']
                }
                
                return render_template('index.html', page_depth=3, data=data, exam_details=exam_details, exam_list=exam_list, table_details=table_details)

            else:
                exam_details = {'exam_name': exam.name, 'exam_id': exam.id, 'college_name': college.name, 'college_id': college.id}
                department_ranks = DepartmentRank.query.filter(and_(DepartmentRank.exam_id==exam_id, DepartmentRank.college_id==college_id)).all()
                for dept in department_ranks:
                    data.append({ 
                                        'name': Department.query.get(dept.department_id).name,
                                        'value': dept.pass_percent,
                                        'id': dept.department_id
                                        })
                table_details = {
                                'caption': exam.name + " | " + college.name,
                                'headers': ['Rank', 'Department Name', 'Pass Percentage']
                }
                return render_template('index.html', page_depth=2, data=data, exam_details=exam_details, exam_list=exam_list, table_details=table_details)
        else:
            exam_details = {'exam_name': exam.name, 'exam_id': exam.id}
            college_ranks = exam.college_ranks
            for clg in college_ranks:
                data.append({ 
                                'name': College.query.get(clg.college_id).name,
                                'value': clg.pass_percent,
                                'id': clg.college_id
                                })
            table_details = {
                                'caption': exam.name,
                                'headers': ['Rank', 'College Name', 'Pass Percentage']
                }
            return render_template('index.html', page_depth=1, data=data, exam_details=exam_details, exam_list=exam_list, table_details=table_details)

            


      


# API Sample Implementation

        

# @app.route("/exams/<int:exam_id>/colleges/<int:college_id>")
# def department(exam_id, college_id):
#     exam_list = []

#     for exam in Exam.query.all():
#         new_exam = {}
#         new_exam['id'] = exam.id
#         new_exam['name'] = exam.name
#         exam_list.append(new_exam)


#     exam = Exam.query.get(exam_id)
#     college = College.query.get(college_id)
#     exam_details = {'exam_name': exam.name, 'exam_id': exam.id, 'college_name': college.name, 'college_id': college.id}

#     department_ranks = DepartmentRank.query.filter(and_(DepartmentRank.exam_id==exam_id, DepartmentRank.college_id==college_id)).all()
#     pass_list = []
#     for dept in department_ranks:
#         pass_list.append({ 
#                                'name': Department.query.get(dept.department_id).name,
#                                'pass_percent': dept.pass_percent,
#                                'id': dept.department_id
#                               })

#     return render_template('rank.html', pass_list=pass_list, exam_details=exam_details, exam_list=exam_list)



# @app.route("/api/exams/<int:exam_id>", defaults={'college_id': None, 'department_id': None})
# @app.route("/api/exams/<int:exam_id>/colleges/<int:college_id>", defaults={'department_id': None})
# @app.route("/api/exams/<int:exam_id>/colleges/<int:college_id>/departments/<int:department_id>")
# def exam_api(exam_id, college_id, department_id):
#     """Return details about exam."""

#     # Make sure exam exists.
    
#     exam = Exam.query.get(exam_id)
#     if exam is None:
#         return jsonify({"error": "Invalid exam_id"}), 422

#     if college_id is None:
#         # Get all result.
#         cpercent_list = []
#         college_ranks = exam.college_ranks
        
#         for clg in college_ranks:
#             cpercent_list.append([College.query.get(clg.college_id).name, clg.pass_percent])

#         return jsonify({
#                 "exam_name": exam.name,
#                 "college_pass_percentage": cpercent_list
#             })
#     else:
#         college = College.query.get(college_id)
#         if college is None:
#                 return jsonify({"error": "Invalid college_id"}), 422
#         if department_id is None:
#             dpercent_list = []

#             cpp = CollegeRank.query.filter(and_(CollegeRank.college_id==college_id, CollegeRank.exam_id==exam_id)).first().pass_percent
#             department_ranks = DepartmentRank.query.filter(and_(DepartmentRank.exam_id==exam_id, DepartmentRank.college_id==college_id)).all()
            
#             for dept in department_ranks:
#                 dpercent_list.append([Department.query.get(dept.department_id).name, dept.pass_percent])

#             return jsonify({
#                     "exam_name": exam.name,
#                     "college_name": college.name,
#                     "college_pass_percent": cpp,
#                     "department_pass_percentage": dpercent_list
#                 })
#         else:
#             department = Department.query.get(department_id)
#             if department is None:
#                 return jsonify({"error": "Invalid department_id"}), 422
            
#             dpp = DepartmentRank.query.filter(and_(DepartmentRank.exam_id==exam_id,
#                                                     DepartmentRank.college_id==college_id,
#                                                     DepartmentRank.department_id==department_id)).first().pass_percent

#             sgpa = []
#             sl = Student.query.filter(and_(Student.exam_id==exam_id,
#                                     Student.college_id==college_id,
#                                     Student.department_id==department_id)).all()
#             for s in sl:
#                 sgpa.append([s.register_no, s.sgpa])

            

#             return jsonify({
#                 "exam_name": exam.name,
#                 "college_name": college.name,
#                 "department_name": department.name,
#                 "department_pass_percent": dpp,
#                 "sgpa": sgpa
#             })

            
