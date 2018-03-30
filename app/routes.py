from flask import Flask
from flask import render_template, flash, redirect, url_for
from flask import request
from flask import send_from_directory
from pdftotext import convert_pdf_to_txt
from data_extract import extractor
import os

from app import app
from app.forms import LoginForm

def convert_file(source, destination):

    raw_text = convert_pdf_to_txt(source)
    text_file = open(destination, "w")
    text_file.write(raw_text)
    text_file.close()
    extractor(destination, os.path.join(app.root_path, 'converted/result.csv'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        f = request.files['pdf']
        f.save(os.path.join(app.root_path, 'uploads/result.pdf'))
        convert_file(os.path.join(
            app.root_path, 'uploads/result.pdf'), os.path.join(app.root_path, 'converted/result.txt'))
        return send_from_directory('converted',
                                   'result.csv', as_attachment=True)
    return render_template('upload.html')


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('index.html')
    return render_template('login.html', title='Sign In', form=form)
