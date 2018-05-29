from flask import Flask
from flask import render_template
from flask import jsonify
from sqlalchemy import and_, or_

from app import app
from app.models import *


@app.route('/')
def index():
    exam_list = []
    for exam in Exam.query.all():
        new_exam = {}
        new_exam['id'] = exam.id
        new_exam['name'] = exam.name
        exam_list.append(new_exam)

    return render_template('index.html', exam_list=exam_list)

@app.route("/api/exams/<int:exam_id>", defaults={'college_id': None, 'department_id': None})
@app.route("/api/exams/<int:exam_id>/colleges/<int:college_id>", defaults={'department_id': None})
@app.route("/api/exams/<int:exam_id>/colleges/<int:college_id>/departments/<int:department_id>")
def exam_api(exam_id, college_id, department_id):
    """Return details about exam."""

    # Make sure exam exists.
    
    exam = Exam.query.get(exam_id)
    if exam is None:
        return jsonify({"error": "Invalid exam_id"}), 422

    if college_id is None:
        # Get all result.
        cpercent_list = []
        college_ranks = exam.college_ranks
        
        for clg in college_ranks:
            cpercent_list.append([College.query.get(clg.college_id).name, clg.pass_percent])

        return jsonify({
                "exam_name": exam.name,
                "college_pass_percentage": cpercent_list
            })
    else:
        college = College.query.get(college_id)
        if college is None:
                return jsonify({"error": "Invalid college_id"}), 422
        if department_id is None:
            dpercent_list = []

            cpp = CollegeRank.query.filter(and_(CollegeRank.college_id==college_id, CollegeRank.exam_id==exam_id)).first().pass_percent
            department_ranks = DepartmentRank.query.filter(and_(DepartmentRank.exam_id==exam_id, DepartmentRank.college_id==college_id)).all()
            
            for dept in department_ranks:
                dpercent_list.append([Department.query.get(dept.department_id).name, dept.pass_percent])

            return jsonify({
                    "exam_name": exam.name,
                    "college_name": college.name,
                    "college_pass_percent": cpp,
                    "department_pass_percentage": dpercent_list
                })
        else:
            department = Department.query.get(department_id)
            if department is None:
                return jsonify({"error": "Invalid department_id"}), 422
            
            dpp = DepartmentRank.query.filter(and_(DepartmentRank.exam_id==exam_id,
                                                    DepartmentRank.college_id==college_id,
                                                    DepartmentRank.department_id==department_id)).first().pass_percent

            sgpa = []
            sl = Student.query.filter(and_(Student.exam_id==exam_id,
                                    Student.college_id==college_id,
                                    Student.department_id==department_id)).all()
            for s in sl:
                sgpa.append([s.register_no, s.sgpa])

            

            return jsonify({
                "exam_name": exam.name,
                "college_name": college.name,
                "department_name": department.name,
                "department_pass_percent": dpp,
                "sgpa": sgpa
            })

            
