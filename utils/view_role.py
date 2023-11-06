#Connected
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/HR Portal'  # Adjust the database name here
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


@app.route('/Role')
def get_all():
    RoleList = Role.query.all()
    if RoleList:
        return jsonify({
            'code': 200,
            'data': {
                'Role': [Role.json() for Role in RoleList]
            }
        }
        )
    return {
        'code': 400,
        'message': 'There are no available roles'
    }

@app.route('/Role/<string:Role_Name>')
def find_by_Role_Name(Role_Name):
    RoleList = Role.query.filter_by(Role_Name=Role_Name).all()
    if RoleList:
        return jsonify({
            'code': 200,
            'data': {
                'Role': [Role.json() for Role in RoleList]
            }
        }
        )
    return jsonify({
        'code': 404,
        'message': 'Role not found.'
    }), 404



if __name__ == '__main__':
    app.run(port=5003, debug=True)
