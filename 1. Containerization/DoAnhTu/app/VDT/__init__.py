import os

from flask import Flask, render_template, request
from flask_pymongo import MongoClient
from DB.data import students


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # connect to db

    client = MongoClient('mongodb://dbmongo:27017', connectTimeoutMS=3000)
    VDT_DB = client.VDTuser
    db = VDT_DB.user

    # a simple page that says hello

    @app.route('/')
    def hello():

        student = db.find_one({"name": "Đỗ Anh Tú"})
        print(student)
        return str(student["name"]) + " VDT"

    @app.route('/VDT')
    def VDT():
        students = db.find()
        student_data = []

        for student in students:
            person = {
                "name": student["name"],
                "birth_year": student["year_of_birth"],
                'university': student["university"]
            }
            student_data.append(person)
        print(student_data)
        return render_template("VDT.html", data_student=student_data)

    @app.route('/VDT/edit', methods=['POST'])
    def edit_user():
        person = {
            'name': request['name'],
            'year_of_birth': request['birth_year'],
            'university': request['university']
        }
        db.insert_one(person)
        return render_template("addUser.html")

    @app.route("/VDT/edit")
    def user():
        return render_template("addUser.html")

    return app
