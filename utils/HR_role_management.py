from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import and_
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:3306/hr portal"
CORS(app)
db = SQLAlchemy(app)

#data json:
# {      "department": "banana",
#        "description": "banana",
#        "role_name": "banana",
#        "skills": ["python", "java", "c++"]   }

class Role(db.Model):
    role_name = db.Column(db.String(20), primary_key=True)
    role_desc = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(20), nullable=False)
    skills = db.relationship('RoleSkill', backref='role', lazy=True)

class RoleSkill(db.Model):
    role_name = db.Column(db.String(20), db.ForeignKey('role.role_name'), primary_key=True)
    skill_name = db.Column(db.String(50), primary_key=True)

class Open_position(db.Model):
    Role_Name = db.Column(db.String(20), db.ForeignKey('role.role_name'), primary_key=True)
    Starting_Date = db.Column(db.Date)
    Ending_Date = db.Column(db.Date)

def field_check(field):
    min_length = 2
    if isinstance(field, list):
        print("is list")
        if all(len(item.strip()) >= min_length for item in field):
            return None  # No validation error
        else:
            return "Each skill should have at least "+ str(min_length) +" letters"

    else:
        if not field or field.strip() == '':
            return "Missing fields"
        elif len(field) <= min_length:
            return "Need to input at least "+ str(min_length) +" letters"
    return None

@app.route('/HR/role_admin', methods=['POST'])
def create_role():
    if request.is_json:
        try:
            data = request.get_json()
            title = data.get('role_name')
            description = data.get('description')
            department_name = data.get('department')
            skills = data.get('skills')

            # Check if title is unique
            if Role.query.filter_by(role_name=title).first():
                return jsonify({
                    'message': 'Role name already exists',
                    'data': {"role_name": title}
                }), 400

            fields_error = {}

            title_error = field_check(title)
            if title_error:
                fields_error['role_name'] = title_error

            description_error = field_check(description)
            if description_error:
                fields_error['description'] = description_error

            department_error = field_check(department_name)
            if department_error:
                fields_error['department'] = department_error

            if isinstance(skills, list):
                skills_error = field_check(skills)
                if skills_error:
                    fields_error['skills'] = skills_error
            else:
                fields_error['skills'] = "Skills should be a list"

            # print(fields_error)

            # Check if any field is missing
            if fields_error:
                return jsonify({
                    'message': 'Required fields are missing or invalid',
                    'data': fields_error
                }), 400

            # Create the role listing
            role = Role(role_name=title, role_desc=description, department=department_name)
            db.session.add(role)

            for skill in skills:
                role_skill = RoleSkill(role_name=title, skill_name=skill)
                db.session.add(role_skill)

            db.session.commit()

            return jsonify({
                'message': 'Role listing created successfully'
            }), 201

        except Exception as e:
            # Unexpected error in code
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            # print(ex_str)
            print(str(e))

            return jsonify({
                "code": 500,
                "message": "internal error: " + str(e)
            }), 500
        
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Please use a valid json request"
    }), 400




@app.route('/HR/role_admin', methods=['GET'])
def get_role():

    # Get query parameters from the URL
    role_name_query = request.args.get('role_name')
    department_query = request.args.get('department')
    sort_by = request.args.get('sort_by')
    exact_match = request.args.get('exact_match')

    # Query roles with optional filtering and sorting
    #example:
    #http://localhost:5000/HR/role_admin?role_name=YourRoleName&department=YourDepartment7sort_by=role_name
    
    #Create the base query
    roles_query = Role.query

    # Create separate filter conditions for role_name and department
    filters = []

    if role_name_query:
         # Check if 'exact_match' is provided in the query
        if exact_match and exact_match.lower() == 'true':
            # Filter by exact role name match
            roles_query = roles_query.filter(Role.role_name == role_name_query)
        else:
            # Filter by partial role name match
            filters.append(Role.role_name.like(f'%{role_name_query}%'))

    if department_query:
        filters.append(Role.department.like(f'%{department_query}%'))

    # Combine filter conditions using 'and_' to ensure both filters are applied
    if filters:
        roles_query = roles_query.filter(and_(*filters))

    if sort_by:
        if sort_by == 'role_name':
            roles_query = roles_query.order_by(Role.role_name)
        elif sort_by == 'department':
            roles_query = roles_query.order_by(Role.department)

    roles = roles_query.all()

    if not roles:  # Check if the list is empty
        # Return an error response indicating no data found
        return jsonify({'error': 'No roles found matching the criteria'}), 404

    # roles = roles_query.all()
    role_data = []
    
    for role in roles:
        status = "inactive"
        start_date = "null"
        end_date = "null"

        open_position = Open_position.query.filter_by(Role_Name=role.role_name).all()

        #check if there is an open position and whether is has a date - set status to active if date has not passed
        if (open_position):
            start_date = open_position[0].Starting_Date
            end_date = open_position[0].Ending_Date
            if start_date is not None and end_date is not None:
                if end_date > datetime.now().date():
                    status = "active"

        #get all skills for each role
        skills = [skill.skill_name for skill in role.skills]

        #append all roles into roles_data list
        role_data.append({
            'department': role.department,
            'description': role.role_desc,
            'skills': skills,
            'role_name': role.role_name,
            'start_date': start_date,
            'end_date': end_date,
            'status': status
        })
    return jsonify({'roles': role_data})

@app.route('/HR/role_admin', methods=['PUT'])
def update_role():
    if request.is_json:
        try:
            data = request.get_json()
            title = data.get('role_name')
            description = data.get('description')
            department_name = data.get('department')
            skills = data.get('skills')

            role = Role.query.filter_by(role_name=title).first()

            if not role:
                return jsonify({'message': 'Role not found'}), 404
            
            #field validation if it exists
            fields_error = {}

            if 'description' in data:
                description_error = field_check(description)
                if description_error:
                    fields_error['description'] = description_error

            if 'department' in data:
                department_error = field_check(department_name)
                if department_error:
                    fields_error['department'] = department_error

            if 'skills' in data:
                if isinstance(skills, list):
                    skills_error = field_check(skills)
                    if skills_error:
                        fields_error['skills'] = skills_error
                else:
                    fields_error['skills'] = "Skills should be a list"

            # Check if any field is missing
            if fields_error:
                return jsonify({
                    'message': 'Required fields are missing or invalid',
                    'data': fields_error
                }), 400

            # Update the role data with the new values
            if 'description' in data:
                role.role_desc = description

            if 'department' in data:
                role.department = department_name
            
            if 'skills' in data:
                # Filter out skills that are already associated with the role
                new_skills = [skill for skill in skills if skill not in [s.skill_name for s in role.skills]]

                # Add new skills
                for skill in new_skills:
                    role_skill = RoleSkill(role_name=title, skill_name=skill)
                    db.session.add(role_skill)

            # Commit the changes to the database
            db.session.commit()

            #get skills for json response
            skills = [skill.skill_name for skill in role.skills]

            return jsonify({
                'message': 'Role updated successfully',
                'data': {
                    'role_name': role.role_name,
                    'role_desc': role.role_desc,
                    'department': role.department,
                    'skills': skills
                }}), 200

        except Exception as e:
            print(str(e))

            return jsonify({
                "code": 500,
                "message": "internal error: " + str(e)
            }), 500
        
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Please use a valid json request"
    }), 400

if __name__ == '__main__':
    CORS(app)
    app.run(port = 5018, debug=True)