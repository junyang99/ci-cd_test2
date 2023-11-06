#Connected
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from view_access_control import Access_Control
import os

app = Flask(__name__)

db_user = os.getenv('DB_USER', 'root')  # default to 'root' if not set
db_pass = os.getenv('DB_PASSWORD', 'root')  # default to 'root' if not set
db_host = os.getenv('DB_HOST', '127.0.0.1')  # default to 'localhost' if not set
db_name = os.getenv('DB_NAME', 'HR Portal')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}:3306/{db_name}'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/HR Portal'
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

# get all staff
@app.route('/Staff')
def get_all():
    staff_list = Staff.query.all()
    if staff_list:
        return jsonify({
            'code': 200,
            'data': {
                'Staff': [staff.json() for staff in staff_list]
            }
        })
    return {
        'code': 400,
        'message': 'There are no available staff members'
    }

# get staff by staff id
@app.route('/Staff/<int:Staff_ID>')
def find_by_staff_id(Staff_ID):
    staff = Staff.query.filter_by(Staff_ID=Staff_ID).first()
    if staff:
        return jsonify({
            'code': 200,
            'data': staff.json()
        })
    return jsonify({
        'code': 404,
        'message': 'Staff not found.'
    }), 404
if __name__ == '__main__':
    app.run(port=5008, debug=True)
