# IMPORTS
import logging
import pyotp
from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for,session, request
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
import os
from admin.views import admin
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
    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        surname=form.lastname.data,
                        password=form.password.data,
                        admin=0)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        logging.warning('SECURITY - User registration [%s, %s]', form.email.data, request.remote_addr)

        # sends user to login page
        return redirect(url_for('users.login'))
    # if request method is GET or form not valid re-render signup page
    return render_template('register.html', form=form)


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    # if session attribute logins does not exist create attribute logins
    if not session.get('logins'):
        session['logins'] = 0
    # if login attempts is 3 or more create an error message
    elif session.get('logins') >= 3:
        flash('Number of incorrect logins exceeded')

    form = LoginForm()

    if form.validate_on_submit():

        # increase login attempts by 1
        session['logins'] += 1

        user = User.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(user.password, form.password.data):

            if session['logins'] == 3:
                flash('Number of incorrect logins exceeded')
                logging.warning('SECURITY - Login attempts exceeded [%s, %s]', form.email.data, request.remote_addr)
            elif session['logins'] == 2:
                flash('Please check your login details and try again. 1 login attempt remaining')
            else:
                flash('Please check your login details and try again. 2 login attempts remaining')

            return render_template('login.html', form=form)


        # if user is verified reset login attempts to 0
        session['logins'] = 0

        login_user(user)

        user.last_logged_in = user.current_logged_in
        user.current_logged_in = datetime.now()
        db.session.add(user)
        db.session.commit()

        logging.warning('SECURITY - Log in [%s, %s, %s]', current_user.id, current_user.email, request.remote_addr)

        if current_user.role == 'admin':
            return admin()

        else:
            return profile()

    return render_template('login.html', form=form)


# view user profile
@users_blueprint.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.firstname)


@users_blueprint.route('/upload', methods=['GET', 'POST'])
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
            db = read_excel("./" + UPLOAD_FOLDER + "/" + filename)
            data = db.values
            CreateSearch.search(data, CreateSearch.get_search_id())

            return redirect(url_for('index'))
    return render_template('upload.html')



# view user account
@users_blueprint.route('/account')
def account():
    return render_template('account.html',
                           acc_no=current_user.id,
                           email=current_user.email,
                           firstname=current_user.firstname,
                           lastname=current_user.lastname,
                           phone=current_user.phone)

@users_blueprint.route('/logout')
def logout():

    logging.warning('SECURITY - Log out [%s, %s, %s]', current_user.id, current_user.email, request.remote_addr)

    logout_user()
    return redirect(url_for('index'))
