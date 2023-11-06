# Connected
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/HR Portal'
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


class Staff_Skill(db.Model):
    __tablename__ = 'Staff_Skill'

    Staff_ID = db.Column(db.Integer, db.ForeignKey(
        'Staff.Staff_ID'), nullable=False, primary_key=True)
    Skill_Name = db.Column(db.String(50), db.ForeignKey(
        'Skill.Skill_Name'), nullable=False, primary_key=True)

    def __init__(self, Staff_ID, Skill_Name):
        self.Staff_ID = Staff_ID
        self.Skill_Name = Skill_Name

    def json(self):
        return {
            'Staff_ID': self.Staff_ID,
            'Skill_Name': self.Skill_Name
        }


@app.route('/Staff_Skill')
def get_all():
    Staff_SkillList = Staff_Skill.query.all()
    if Staff_SkillList:
        return jsonify({
            'code': 200,
            'data': {
                'Staff-Skill': [Staff_Skill.json() for Staff_Skill in Staff_SkillList]
            }
        }
        )
    return {
        'code': 400,
        'message': 'There is no records of Staff skill'
    }

# function to get specific staff skill
@app.route('/Staff_Skill/<int:staff_id>')
def get_staff_skills(staff_id):
    staff_skills = db.session.query(Staff_Skill, Skill.Skill_Desc).\
        join(Skill, Staff_Skill.Skill_Name == Skill.Skill_Name).\
        filter(Staff_Skill.Staff_ID == staff_id).all()

    if staff_skills:
        result = []
        for staff_skill, skill_desc in staff_skills:
            result.append({
                'Staff_ID': staff_skill.Staff_ID,
                'Skill_Name': staff_skill.Skill_Name,
                'Skill_Desc': skill_desc
            })
        return jsonify({
            'code': 200,
            'data': {
                'Staff-Skill': result
            }
        })
    
    return {
        'code': 400,
        'message': 'Invalid Staff ID'
    }




if __name__ == '__main__':
    app.run(port=5012, debug=True)
