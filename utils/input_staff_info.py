from flask import Flask, render_template, request, redirect, url_for, flash
import re
import mysql.connector
from flask_cors import cross_origin

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from view_access_control import Access_Control
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8081"}})
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/HR Portal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Access_Control(db.Model):
    __tablename__ = 'Access_Control'

    Access_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    Access_Control_Name = db.Column(db.String(20), nullable=False)
    

    def __init__(self, Access_ID , Access_Control_Name):
        self.Access_ID= Access_ID
        self.Access_Control_Name = Access_Control_Name


    def json(self):
        return {
            'Access_ID': self.Access_ID,
            'Access_Control_Name': self.Access_Control_Name
        }
class Application(db.Model):
    __tablename__ = 'Application'

    Application_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    Position_ID = db.Column(db.Integer, db.ForeignKey(
        'Open_Position.Position_ID'), nullable=False)
    Staff_ID = db.Column(db.Integer, db.ForeignKey(
        'Staff.Staff_ID'), nullable=False)
    Application_Date = db.Column(db.Date, nullable=False)
    Cover_Letter = db.Column(db.String(10000), nullable=False)
    Application_Status = db.Column(db.Integer, nullable=False)

    def __init__(self, Position_ID, Staff_ID, Application_Date, Cover_Letter, Application_Status):
        # self.Application_ID = Application_ID
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

class Staff(db.Model):
    __tablename__ = 'Staff'

    Staff_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    Country = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Access_ID = db.Column(db.Integer, db.ForeignKey('Access_Control.Access_ID'), nullable=False)  # Foreign key reference
    access_control = db.relationship(Access_Control, backref='staff', lazy=True)

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

class Role(db.Model):
    __tablename__ = 'Role'

    Role_Name = db.Column(db.String(20), nullable=False, primary_key=True)
    Role_Desc = db.Column(db.String(100), nullable=False)
    Department = db.Column(db.String(100), nullable=False)

    def __init__(self, Role_Name, Role_Desc, Department):
        self.Role_Name = Role_Name
        self.Role_Desc = Role_Desc
        self.Department = Department

    def json(self):
        return {
            'Role_Name': self.Role_Name,
            'Role_Desc': self.Role_Desc,
            'Department' : self.Department
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


@app.route('/create_application', methods=['POST'])
def create_application():
    if request.method == 'POST':
        data = request.get_json()
        # Extract data from the request
        position_id = data.get('Position_ID')
        staff_id = data.get('Staff_ID')
        application_date = data.get('Application_Date')
        cover_letter = data.get('Cover_Letter')
        application_status = data.get('Application_Status')

        # Create a new Application instance
        new_application = Application(
            Position_ID=position_id,
            Staff_ID=staff_id,
            Application_Date=application_date,
            Cover_Letter=cover_letter,
            Application_Status=application_status
        )

        # Add the new application to the database
        db.session.add(new_application)
        db.session.commit()

        return jsonify({'message': 'Application created successfully'})
    

@app.route('/Staff/applications/<int:Staff_ID>', methods=['GET'])
def get_staff_applications(Staff_ID):
    try:
        # Retrieve applications for the specified Staff_ID
        applications = Application.query.filter_by(Staff_ID=Staff_ID).all()
        if applications:
            # Create a list to store the combined data
            combined_data = []

            for app in applications:
                # Get the position associated with the application
                position = Open_Position.query.get(app.Position_ID)

                # Get the role associated with the position
                role = Role.query.get(position.Role_Name)

                # Construct a JSON object with role_name, dept, application_date, and status
                combined_data.append({
                    'role_name': role.Role_Name,
                    'dept': role.Department,
                    'application_date': app.Application_Date,
                    'application_status': app.Application_Status,  # Include Application_Status 0: pending, 1: accepted, 2: rejected
                })

            return jsonify({
                'code': 200,
                'data': combined_data
            })
        else:
            return jsonify({
                'code': 404,
                'message': 'No applications found for the specified Staff ID.'
            }), 404
    except Exception as e:
        # Handle exceptions, log errors, and return an appropriate response
        return jsonify({
            'code': 500,
            'message': 'Internal Server Error: ' + str(e)
        }), 500

    
@app.route('/Staff/<int:Staff_ID>/roles', methods=['GET'])
def get_staff_roles(Staff_ID):
    try:
        # Retrieve roles for the specified Staff_ID from the Role table
        roles = Role.query.filter_by(Staff_ID=Staff_ID).all()

        if roles:
            # Convert the role objects to JSON format
            roles_json = [role.json() for role in roles]

            return jsonify({
                'code': 200,
                'data': roles_json
            })
        else:
            return jsonify({
                'code': 404,
                'message': 'No roles found for the specified Staff ID.'
            }), 404
    except Exception as e:
        # Handle exceptions, log errors, and return an appropriate response
        return jsonify({
            'code': 500,
            'message': 'Internal Server Error: ' + str(e)
        }), 500


if __name__ == "__main__":
    app.run(port=5016, debug=True)


