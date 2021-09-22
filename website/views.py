from website.auth import login
from flask import Blueprint, render_template, request, url_for, session, redirect
from . import login_required
from .extensions import db
from .models import Canvas
import json
import ast

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    courses = Canvas().all_courses()

    if request.method == 'POST':
        course_info = request.form.get('list_courses')
        if course_info == None:
            pass
        else:
            data = json.dumps(ast.literal_eval(course_info))
            d = json.loads(data)
            Canvas().stage_course(d)
            return redirect(url_for('views.course', course_id=d['course_id']))

    staged = list(db.staged.find({'user_id':session['user']['_id']}))

    return render_template('dashboard.html', courses=courses, staged=staged)

@views.route('/dashboard/<course_id>/', methods=['GET', 'POST'])
@login_required
def course(course_id):
    id = int(course_id)
    query = {'user_id':session['user']['_id'],'course_id':id}
    dir_data = db.staged.find_one( query )
    assignments_data = db.assignments.find_one( query )
    pathway_data = db.pathways.find_one( query )

    if dir_data == None:
        return redirect(url_for('views.dashboard'))
    else:
        dir = dir_data['dir']
        assignments = assignments_data['assignments']

    return render_template('course.html', id=id, dir=dir, assignments=assignments, pathway=pathway_data)

@views.route('/dashboard/<course_id>/calculate_pathway/', methods=['POST'])
@login_required
def pathway(course_id):
    id = int(course_id)
    ideal_grade = float(request.form.get('ideal_grade'))
    m = float(request.form.get('m_value'))
    n = float(request.form.get('n_value'))
    dir = db.staged.find_one({'user_id':session['user']['_id'], 'course_id':id})['dir']

    if dir == None:
        return redirect(url_for('views.dashboard'))

    path = Canvas().pathway(dir, id, ideal_grade, m, n)
    string_path = {str(key):value for key, value in path.items()}

    query = {'user_id':session['user']['_id'],'course_id':id}
    newvalues = {
        'user_id':session['user']['_id'],
        'course_id':id,
        'pathway':string_path,
        'ideal_grade':ideal_grade,
        'm':m,
        'n':n
        }
    db.pathways.update(
        query, newvalues, upsert=True
    )

    return redirect(url_for('views.course', course_id=id))

@views.route('/dashboard/<course_id>/unstage/', methods=['GET','POST'])
@login_required
def unstage(course_id):
    id = int(course_id)
    query = {'user_id':session['user']['_id'],'course_id':id}
    db.staged.remove(query)
    db.pathways.remove(query)
    db.assignments.remove(query)

    return redirect(url_for('views.dashboard'))