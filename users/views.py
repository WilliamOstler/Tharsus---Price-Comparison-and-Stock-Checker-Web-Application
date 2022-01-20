# IMPORTS
import logging
from flask import Blueprint, render_template, flash, redirect, url_for, session, request, send_file
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
import os
from app import db, UPLOAD_FOLDER, app
from models import User
from users.forms import RegisterForm, LoginForm
from pandas import read_excel
from werkzeug.utils import secure_filename
from Search import CreateSearch

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')

# VIEWS
# view registration
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash('Email address already exists')
            return render_template('register.html', form=form)

        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        surname=form.lastname.data,
                        password=form.password.data,
                        role='user')

        db.session.add(new_user)
        db.session.commit()


        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(user.password, form.password.data):

            return render_template('login.html', form=form)

        login_user(user)

        return redirect(url_for('users.upload_file'))

    return render_template('login.html', form=form)


@users_blueprint.route('/search', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db = read_excel("./" + UPLOAD_FOLDER + "/" + filename, skiprows = 4)
            data = db.values
            search = CreateSearch.search(data, request.values['Quantity'], CreateSearch.get_search_id())


            return render_template('Results.html', searchID=search)

    return render_template('search.html')

@users_blueprint.route('/download', methods=['GET'])
def download_file():
    path = f'BOMInputTemplate/Example_BOM_1.xlsx'
    return send_file(path)



@users_blueprint.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    request.form.get('download')
    path = f"SearchResults/BOMSearch{request.form.get('id')}results.xlsx"
    return send_file(path, as_attachment=True)



@users_blueprint.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('users.login'))
