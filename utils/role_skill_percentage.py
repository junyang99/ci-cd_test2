#Connected
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from invokes import invoke_http
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/HR Portal'  # Adjust the database name here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

staff_skill_url = "http://localhost:5012/Staff_Skill"
role_skill_url = "http://localhost:5011/Role_Skill"
def normalize_skill_name(skill_name):
    return skill_name.lower().replace(" ", "")
@app.route('/compare_skills', methods=['GET'])
def compare_skills():
    try:
        staff_id = request.args.get('staff_id')
        role_name = request.args.get('role_name')

        # Get staff skills
        staff_skills_response = requests.get(f"{staff_skill_url}/{staff_id}")
        staff_skills_data = staff_skills_response.json()

        # Get role skills
        role_skills_response = requests.get(f"{role_skill_url}/{role_name}")
        role_skills_data = role_skills_response.json()

        # Check if 'data' key exists in the responses
        if 'data' not in staff_skills_data or 'data' not in role_skills_data:
            raise Exception("Invalid response format from microservices")

        # Extract skill names from responses
        staff_skills = set(skill['Skill_Name'] for skill in staff_skills_data['data']['Staff-Skill'])
        role_skills = set(skill['Role_Desc'] for skill in role_skills_data['data']['Role-Skill'])

        # Calculate percentage of matching skills
        matching_skills = staff_skills.intersection(role_skills)
        percentage_match = (len(matching_skills) / len(role_skills)) * 100

        return jsonify({
            'code': 200,
            'message': 'Skills comparison successful',
            'data': {
                'percentage_match': percentage_match
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'Internal server error: {str(e)}'
        })

if __name__ == '__main__':
    app.run(port=5014, debug=True)