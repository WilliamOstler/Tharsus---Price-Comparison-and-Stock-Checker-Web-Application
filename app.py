
from flask import Flask, render_template, request, send_file
from pandas import read_excel
from flask_sqlalchemy import SQLAlchemy
import os


UPLOAD_FOLDER = 'uploads/'
app = Flask("excel-app")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/output", methods=["POST"])
def output():
    if request.method == "POST":
        if request.form.get("openFile"):
            file = request.files["excel_file"]
            fileName = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
            db = read_excel("./"+UPLOAD_FOLDER+"/"+fileName)
            columnNames = db.columns
            columnNames = columnNames.to_list()
            data = db.values
            return render_template("output.html", columnNames=columnNames, data=data, fileName=fileName)

        elif request.form.get("newData"):
            fileName = request.form.get("fileName")
            price = 10 #a random number to see if it works
            db = read_excel("./"+UPLOAD_FOLDER+"/"+fileName)
            db['Cost'] = db['Quantity needed'] * price #price should be scraped from the website
            columnNames = db.columns
            columnNames = columnNames.to_list()
            data = db.values
            db.to_excel("./"+UPLOAD_FOLDER+"/"+fileName, sheet_name="Updated", index=False)
            return render_template("output.html", columnNames=columnNames, data=data, fileName=fileName)


@app.route('/download/<fileName>')
def download(fileName):
    file_path = UPLOAD_FOLDER + fileName
    return send_file(file_path, as_attachment=True, attachment_filename='')

app.run(port=8080, debug=True)