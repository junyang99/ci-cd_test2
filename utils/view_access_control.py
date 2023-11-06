#Connected
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

#Check that it is connected to database
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


@app.route('/Access_Control')
def get_all():
    Access_ControlList = Access_Control.query.all()
    if Access_ControlList:
        return jsonify({
            'code': 200,
            'data': {
                'Access': [Access_Control.json() for Access_Control in Access_ControlList]
            }
        }
        )
    return {
        'code': 400,
        'message': 'There are no available access control'
    }


if __name__ == '__main__':
    app.run(port=5005, debug=True)