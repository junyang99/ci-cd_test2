#Connected
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from invokes import invoke_http
from urllib.parse import quote
from datetime import datetime
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/HR Portal'  # Adjust the database name here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

viewStaffSkillURL = "http://localhost:5012/Staff_Skill"
roleSkillPercentURL = "http://localhost:5014/compare_skills"

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
    Role_Name = db.Column(db.String(20),db.ForeignKey('Role.Role_Name'), nullable=False)
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
            'Skill_Name': self.Skill_Name
        }
    
# specific role listings
@app.route('/Role_Listing', methods=['GET'])
def get_role_listing():
    position_id = request.args.get('position_id')
    staff_id = request.args.get('staff_id')

    if position_id and staff_id:
        # Get row from Open_Position table
        selected_role_listing = Open_Position.query.filter_by(Position_ID=position_id).first()

        today = datetime.now().date()

        if selected_role_listing.Ending_Date < today:
            return jsonify({
                'code': 400,
                'message': 'Ending date has passed.'
            }), 400

        # Use Role_Name from Open_Position table to match with Role_Name in Role table
        selected_role_info = Role.query.filter_by(Role_Name=selected_role_listing.Role_Name).first()

        # Use Role Name from Open_Position table to match with Role_Name in Role_Skill table
        selected_skill_info = Role_Skill.query.filter_by(Role_Name=selected_role_listing.Role_Name).all()

        # Retrieve Ending_Date from Open_Position table
        ending_date = selected_role_listing.Ending_Date

        staffURL = viewStaffSkillURL + "/" + str(staff_id)
        staff_skill = invoke_http(staffURL, method='GET')

        role_skill_params = {'staff_id': staff_id, 'role_name': selected_role_listing.Role_Name}
        role_skill_match = requests.get(roleSkillPercentURL, params=role_skill_params).json()

        if selected_role_info and selected_skill_info and staff_skill["code"] == 200 and role_skill_match["code"] == 200:
            return jsonify({
                'code': 200,
                'data':
                    {
                        'Role_Name': selected_role_listing.Role_Name,
                        'Role_Desc': selected_role_info.Role_Desc,
                        'Department': selected_role_info.Department,
                        'Required Skills for Role': [roleSkill.json() for roleSkill in selected_skill_info],
                        'Staff Skills': staff_skill,
                        'Role-Skill Match': role_skill_match,
                        'Ending_Date': ending_date
                    }
            })

        return jsonify({
            'code': 400,
            'message': 'Missing information for selected role listing.'
        }), 400

    return jsonify({
        'code': 400,
        'message': 'No role listing selected or no staff ID found.'
    }), 400


@app.route('/All_Role_Listing', methods=['GET'])
def get_all_role_listing():
    role_listing = Open_Position.query.all()

    if role_listing:
        # Create a list to store the joined data
        joined_data = []

        current_date = datetime.now().date()

        for role_listing_item in role_listing:
            # Find the corresponding Role object by Role_Name
            role = Role.query.filter_by(Role_Name=role_listing_item.Role_Name).first()

            if role:
                ending_date = role_listing_item.Ending_Date
                if ending_date:
                    if ending_date > current_date:
                        data = {
                            "Ending_Date": role_listing_item.Ending_Date,
                            "Position_ID": role_listing_item.Position_ID,
                            "Role_Name": role_listing_item.Role_Name,
                            "Starting_Date": role_listing_item.Starting_Date,
                            "Role_Desc": role.Role_Desc,
                            "Department": role.Department
                        }
                        joined_data.append(data)

        if joined_data:
            return jsonify({
                'code': 200,
                'data': {
                    'Role_Listing': joined_data
                }
            }), 200

    return jsonify({
        'code': 404,
        'message': 'There are no available role listings.'
    }), 404




if __name__ == '__main__':
    app.run(port=5013, debug=True)