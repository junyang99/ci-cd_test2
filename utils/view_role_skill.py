#Connected
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
        

class Skill(db.Model):
    __tablename__ = 'Skill'

    Skill_Name = db.Column(db.String(50), nullable=False, primary_key=True)
    Skill_Desc = db.Column(db.String, nullable=False)
    # Dept = db.Column(db.String(100), nullable=False)

    def __init__(self, Skill_Name, Skill_Desc):
        self.Skill_Name = Skill_Name
        self.Skill_Desc = Skill_Desc
        # self.Dept = Dept

    def json(self):
        return {
            'Skill_Name': self.Skill_Name,
            'Skill_Desc': self.Skill_Desc
            # 'Dept' : self.Dept
        }

class Role_Skill(db.Model):
    __tablename__ = 'Role_Skill'

    Role_Name = db.Column(db.String(20),db.ForeignKey('Role.Role_Name'), nullable=False, primary_key=True)
    Skill_Name = db.Column(db.String(50), db.ForeignKey('Skill.Skill_Name'), nullable=False, primary_key = True)


    def __init__(self, Role_Name, Skill_Name):
        self.Role_Name = Role_Name
        self.Skill_Name = Skill_Name


    def json(self):
        return {
            'Role_Name': self.Role_Name,
            'Role_Desc': self.Skill_Name
        }


@app.route('/Role_Skill')
def get_all():
    Role_SkillList = Role_Skill.query.all()
    if Role_SkillList:
        return jsonify({
            'code': 200,
            'data': {
                'Roles-Skill': [Role_Skill.json() for Role_Skill in Role_SkillList]
            }
        }
        )
    return {
        'code': 400,
        'message': 'There is no records of Roles-Skill'
    }

@app.route('/Role_Skill/<string:Role_Name>')
def get_role_skills(Role_Name):
    role_skills = Role_Skill.query.filter_by(Role_Name=Role_Name).all()
    
    if role_skills:
        return jsonify({
            'code': 200,
            'data': {
                'Role-Skill': [role_skill.json() for role_skill in role_skills]
            }
        })
    
    return {
        'code': 400,
        'message': 'Role' + Role_Name + ' does not exist.'
    }

@app.route('/Skill')
def get_all_skill():
    SkillList = Skill.query.all()
    if SkillList:
        return jsonify({
            'code': 200,
            'data': {
                'Skill': [Skill.json() for Skill in SkillList]
            }
        }
        )
    return {
        'code': 400,
        'message': 'There is no records of Skill'
    }

if __name__ == '__main__':
    app.run(port=5011, debug=True)
