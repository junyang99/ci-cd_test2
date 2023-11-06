# Connected
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/HR Portal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Checked


class Skill(db.Model):
    __tablename__ = 'Skill'

    Skill_Name = db.Column(db.String(50), nullable=False, primary_key=True)
    Skill_Desc = db.Column(db.String, nullable=False)

    def __init__(self, Skill_Name, Skill_Desc):
        self.Skill_Name = Skill_Name
        self.Skill_Desc = Skill_Desc

    def json(self):
        return {
            'Skill_Name': self.Skill_Name,
            'Skill_Desc': self.Skill_Desc
        }


class Open_Position(db.Model):
    __tablename__ = 'Open_Position'

    Position_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    Role_Name = db.Column(db.String(20), nullable=False)
    Starting_Date = db.Column(db.Date, nullable=False)
    Ending_Date = db.Column(db.Date, nullable=False)

    def __init__(self, Position_ID, Role_Name, Starting_Date, Ending_Date):
        self.Position_ID = Position_ID
        self.Role_Name = Role_Name
        self.Starting_Date = Starting_Date
        self.Ending_Date = Ending_Date

    def json(self):
        return {
            'Position_ID': self.Position_ID,
            'Role_Name': self.Role_Name,
            'Starting_Date': self.Starting_Date,
            'Ending_Date': self.Ending_Date
        }

# Checked


class Access_Control(db.Model):
    __tablename__ = 'Access_Control'

    Access_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    Access_Control_Name = db.Column(db.String(20), nullable=False)

    def __init__(self, Access_ID, Access_Control_Name):
        self.Access_ID = Access_ID
        self.Access_Control_Name = Access_Control_Name

    def json(self):
        return {
            'Access_ID': self.Access_ID,
            'Access_Control_Name': self.Access_Control_Name
        }

# Checked


class Staff(db.Model):
    __tablename__ = 'Staff'

    Staff_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    Country = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Access_ID = db.Column(db.Integer, db.ForeignKey(
        'Access_Control.Access_ID'), nullable=False)  # Foreign key reference
    # access_control = db.relationship(Access_Control, backref='staff', lazy=True)

    def __init__(self, Staff_ID, Staff_FName, Staff_LName, Dept, Country, Email, Access_ID):
        self.Staff_ID = Staff_ID
        self.Staff_FName = Staff_FName
        self.Staff_LName = Staff_LName
        self.Dept = Dept
        self.Country = Country
        self.Email = Email
        self.Access_ID = Access_ID

    def json(self):
        return {
            'Staff_ID': self.Staff_ID,
            'Staff_FName': self.Staff_FName,
            'Staff_LName': self.Staff_LName,
            'Dept': self.Dept,
            'Country': self.Country,
            'Email': self.Email,
            'Access_ID': self.Access_ID
        }


class Staff_Skill(db.Model):
    __tablename__ = 'Staff_Skill'

    Staff_ID = db.Column(db.Integer, db.ForeignKey(
        'Staff.Staff_ID'), primary_key=True)
    Skill_Name = db.Column(db.String(50), db.ForeignKey(
        'Skill.Skill_Name'), primary_key=True)

    staff = db.relationship('Staff', backref='staff_skills')
    skill = db.relationship('Skill', backref='staff_skills')

    def __init__(self, Staff_ID, Skill_Name):
        self.Staff_ID = Staff_ID
        self.Skill_Name = Skill_Name

    def json(self):
        return {
            'Staff_ID': self.Staff_ID,
            'Skill_Name': self.Skill_Name
        }


class Application(db.Model):
    __tablename__ = 'Application'

    Application_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    Position_ID = db.Column(db.Integer, db.ForeignKey(
        'Open_Position.Position_ID'), nullable=False)
    Staff_ID = db.Column(db.Integer, db.ForeignKey(
        'Staff.Staff_ID'), nullable=False)
    Application_Date = db.Column(db.Date, nullable=False)
    Cover_Letter = db.Column(db.String, nullable=False)
    Application_Status = db.Column(db.Integer, nullable=False)

    def __init__(self, Application_ID, Position_ID, Staff_ID, Application_Date, Cover_Letter, Application_Status):
        self.Application_ID = Application_ID
        self.Position_ID = Position_ID
        self.Staff_ID = Staff_ID
        self.Application_Date = Application_Date
        self.Cover_Letter = Cover_Letter
        self.Application_Status = Application_Status

    def json(self):
        return {
            'Application_ID': self.Application_ID,
            'Position_ID': self.Position_ID,
            'Staff_ID': self.Staff_ID,
            'Application_Date': self.Application_Date,
            'Cover_Letter': self.Cover_Letter,
            'Application_Status': self.Application_Status,
        }


@app.route('/Application')
def get_all():
    ApplicationList = Application.query.all()
    if ApplicationList:
        return jsonify({
            'code': 200,
            'data': {
                'Application': [Application.json() for Application in ApplicationList]
            }
        }
        )
    return {
        'code': 400,
        'message': 'There is no records of applicant'
    }
    

@app.route('/Application/<string:Role_Name>')
def get_application(Role_Name):
    open_position_data = Open_Position.query.filter_by(Role_Name=Role_Name).first()
    app_position_id = open_position_data.Position_ID
    applications = Application.query.filter_by(Position_ID=app_position_id).all()

    start_date = open_position_data.Starting_Date
    end_date = open_position_data.Ending_Date

    if applications:
        application_data = []
        for application in applications:
            staff_skills = Staff_Skill.query.filter_by(
                Staff_ID=application.Staff_ID).all()
            staff_skill_data = [skill.Skill_Name for skill in staff_skills]

            staff_data = Staff.query.filter_by(Staff_ID=application.Staff_ID).first()
            staff_name = staff_data.Staff_FName + ' ' + staff_data.Staff_LName

            application_data.append({
                'Application_ID': application.Application_ID,
                'Position_ID': application.Position_ID,
                'Staff_ID': application.Staff_ID,
                'Application_Date': application.Application_Date,
                'Cover_Letter': application.Cover_Letter,
                'Application_Status': application.Application_Status,
                'Staff_Skill': staff_skill_data,
                'Staff_Name': staff_name,
                'Start_Date': start_date,
                'End_Date': end_date,
            })

        return jsonify({
            'code': 200,
            'applications': application_data
        })

    return jsonify({
        'code': 404,
        'message': 'No applications found for the specified Position_ID'
    }), 404


if __name__ == '__main__':
    app.run(port=5004, debug=True)
