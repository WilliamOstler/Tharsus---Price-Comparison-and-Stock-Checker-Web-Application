
from flask import Flask, render_template, request, send_file

from flask_sqlalchemy import SQLAlchemy
import os


UPLOAD_FOLDER = 'uploads/'
app = Flask("excel-app")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://csc2033_team36:Net8BondSaps@cs-db.ncl.ac.uk:3306/csc2033_team36'
#app.config['SQLALCHEMY_BINDS'] = {
    #'parts':        'mysql+mysqlconnector://csc2033_team36:Net8BondSaps@cs-db.ncl.ac.uk:3306/csc2033_team36/tables/parts',
    #'prices':      'mysql+mysqlconnector://csc2033_team36:Net8BondSaps@cs-db.ncl.ac.uk:3306/csc2033_team36/tables/prices'
#}
db = SQLAlchemy(app)


@app.route("/")
def homepage():
    return render_template("home.html")

@app.route('/download/<fileName>')
def download(fileName):
    file_path = UPLOAD_FOLDER + fileName
    return send_file(file_path, as_attachment=True, attachment_filename='')

#app.run(port=8080, debug=True)