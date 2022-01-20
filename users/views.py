"""
Contains the majority of the flask views for the web app.
"""
import os
from flask import Blueprint, render_template, flash, redirect, url_for, request, send_file
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from pandas import read_excel
from app import db, UPLOAD_FOLDER, app
from models import User
from users.forms import RegisterForm, LoginForm
from execute_search import create_search

# Instantiates the blurprints
users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register view. Contains the register form that allows a user to register for an account.
    """
    # Instantiate the register form object
    form = RegisterForm()

    if form.validate_on_submit():
        # Check to see if email inputted is already in use.
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email address already exists')
            return render_template('register.html', form=form)

        # If all inputs are validated, then create new User object and add it to the User table
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        surname=form.lastname.data,
                        password=form.password.data,
                        role='user')
        db.session.add(new_user)
        db.session.commit()

        # After acount is created, redirect to the login page.
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login view. Contains the login form that allows a user log into their account.
    """
    # Instantiate the login form
    form = LoginForm()

    if form.validate_on_submit():

        # Retrieve details of the account which is trying to log in
        user = User.query.filter_by(email=form.email.data).first()

        # If login details are incorrect, then re-render login page
        if not user or not check_password_hash(user.password, form.password.data):
            return render_template('login.html', form=form)

        # If login details are correct, then log in and render Part Search page
        login_user(user)
        return redirect(url_for('users.upload_file'))

    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    """
    Logout view. Allow users to log out of an account.
    """
    logout_user()
    return redirect(url_for('users.login'))


@users_blueprint.route('/search', methods=['GET', 'POST'])
@login_required
def upload_file():
    """
    View for creating a part search. Retrieves the BOM uploaded and uses the data to call the
    create_search methods. This view requires the user to be logged in.
    """
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Read the Excel spreadsheet (BOM)
            bill_of_materials = read_excel("./" + UPLOAD_FOLDER + "/" + filename, skiprows = 4)
            data = bill_of_materials.values

            # Create an individual search id for the search
            search_id = create_search.get_search_id()
            # Call the create_search.search method to create a search
            create_search.search(data, request.values['Quantity'], search_id)

            # Return results to user
            return render_template('Results.html', searchID=search_id)

    return render_template('search.html')


@users_blueprint.route('/download', methods=['GET'])
@login_required
def download_file():
    """
    View which allows the user to download a BOM template file, which they can use to create
    searches.
    """
    path = 'BOMInputTemplate/BOM_Template.xlsx'
    return send_file(path)


@users_blueprint.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    """
    Allows the user to download search results in the form of an Excel Spreadsheet
    """
    request.form.get('download')
    path = f"SearchResults/BOMSearch{request.form.get('id')}results.xlsx"
    return send_file(path, as_attachment=True)
