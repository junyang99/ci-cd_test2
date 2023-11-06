from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import and_, or_, desc
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:3306/hr portal"
db = SQLAlchemy(app)
CORS(app)

class Role(db.Model):
    role_name = db.Column(db.String(20), primary_key=True)
    role_desc = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(20), nullable=False)
    skills = db.relationship('RoleSkill', backref='role', lazy=True)


class RoleSkill(db.Model):
    role_name = db.Column(db.String(20), db.ForeignKey(
        'role.role_name'), primary_key=True)
    skill_name = db.Column(db.String(50), primary_key=True)


class Open_position(db.Model):
    Position_ID = db.Column(db.String(20), primary_key=True)
    Role_Name = db.Column(db.String(20), db.ForeignKey('role.role_name'))
    Starting_Date = db.Column(db.Date, nullable=True)
    Ending_Date = db.Column(db.Date, nullable=True)

# works
# testing
# check if data input is too little or blank
# check for if ending date has passed
# check if role name does not exist
# check if ending date is earlier than starting date

#check for minimum character
# def field_check(field):
#     min_length = 2
#     if field == "":
#         return "Missing fields"
#     elif len(str(field)) < min_length:
#         return "Need to input at least " + str(min_length) + " letters"
#     return None

def date_check(starting_date, ending_date, role_name):
    today = datetime.now().date()

    # Check for empty starting_date
    if not starting_date:
        return "Starting date is empty"
    
    # Check for empty ending_date
    if not ending_date:
        return "Ending date is empty"

    # Parse dates since they are not empty
    starting_date_parsed = datetime.strptime(starting_date, '%Y-%m-%d').date()
    ending_date_parsed = datetime.strptime(ending_date, '%Y-%m-%d').date()

    # Check if starting date has passed
    if starting_date_parsed < today:
        return "Starting date has passed"

    # Check if ending_date has passed today's date
    if ending_date_parsed < today:
        return "Ending date has passed"

    # Check if ending_date is earlier than starting_date
    if ending_date_parsed < starting_date_parsed:
        return "Ending date is earlier than starting date"

    # Check if there are any existing positions with overlapping dates for the same role name
    existing_positions = Open_position.query.filter(
        Open_position.Role_Name == role_name,
        or_(
            and_(Open_position.Starting_Date <= starting_date_parsed,
                 Open_position.Ending_Date >= starting_date_parsed),
            and_(Open_position.Starting_Date <= ending_date_parsed,
                 Open_position.Ending_Date >= ending_date_parsed),
            and_(Open_position.Starting_Date >= starting_date_parsed,
                 Open_position.Ending_Date <= ending_date_parsed)
        )
    ).all()

    if existing_positions:
        return "Dates overlap with existing positions for the same role name"

    return None

def date_check2(starting_date, ending_date):
    today = datetime.now().date()
    
    # Check for empty dates and convert to None
    starting_date = None if not starting_date else starting_date
    ending_date = None if not ending_date else ending_date

    # Check for empty dates
    if not starting_date or not ending_date:
        return "Both starting date and ending date must be provided"
    
    acceptable_criteria = [None, ""]
    
    if starting_date in acceptable_criteria and ending_date in acceptable_criteria:
        return None

    try:
        # Parse dates since they are not empty
        starting_date_parsed = datetime.strptime(starting_date, '%Y-%m-%d').date()
        ending_date_parsed = datetime.strptime(ending_date, '%Y-%m-%d').date()
    except ValueError:
        # This handles incorrect date formats and invalid dates such as "2022-01-00"
        return "Invalid date format or value"

    # Check if starting date has passed
    if starting_date_parsed < today:
        return "Starting date has passed"

    # Check if ending_date is earlier than starting_date
    if ending_date_parsed < starting_date_parsed:
        return "Ending date is earlier than starting date"

    return None


def generate_position_id():
    last_position = Open_position.query.order_by(desc(Open_position.Position_ID)).first()
    if last_position:
        # Assuming Position_ID is numeric and can be converted directly to int.
        # You might need to adjust this if the Position_ID format is different.
        last_id = int(last_position.Position_ID)
        new_id = last_id + 1
    else:
        new_id = 1  # This is the first position ID if there are no positions in the DB
    return str(new_id)

def role_exists(role_name):
    return Role.query.filter_by(role_name=role_name).first() is not None

@app.route('/HR/add_open_position', methods=['POST'])
def add_open_position():
    if request.is_json:
        try:
            data = request.get_json()
            role_name = data.get('role_name')
            department = data.get('department')  # This is not used in Open_position
            skills = data.get('skills')          # This is not used in Open_position
            role_desc = data.get('role_desc')    # This is not used in Open_position

            # Validate role_name exists
            if not role_exists(role_name):
                return jsonify({
                    'message': 'Role name does not exist',
                    'data': {"role_name": role_name}
                }), 400

            # Generate a new position ID
            position_id = generate_position_id()

            # Create and add the new open position without starting and ending dates
            new_open_position = Open_position(
                Position_ID=position_id,
                Role_Name=role_name,
                Starting_Date = None,
                Ending_Date = None,
                
            )
            db.session.add(new_open_position)
            db.session.commit()

            return jsonify({
                'message': 'Open position added successfully',
                'data': {
                    'Position_ID': position_id,
                    'Role_Name': role_name,
                    "Starting_Date": "None",
                    "Ending_Date": "None"
                }
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({
                "code": 500,
                "message": "Internal error: " + str(e)
            }), 500

    else:
        return jsonify({
            "code": 400,
            "message": "Please use a valid JSON request"
        }), 400

@app.route('/HR/update_open_position', methods=['PUT'])
def update_open_position():
    if request.is_json:
        try:
            data = request.get_json()
            role_name = data.get('role_name')
            new_starting_date = data.get('starting_date')
            new_ending_date = data.get('ending_date')

            # Check if role_name exists
            if not role_exists(role_name):
                return jsonify({
                    'message': 'Role name does not exist',
                    'data': {"role_name": role_name}
                }), 400

            # Check if both dates are empty strings or None, then set them to None
            if not new_starting_date and not new_ending_date:
                new_starting_date = None
                new_ending_date = None
            else:
                # Validate dates if not empty or None
                date_error = date_check2(new_starting_date, new_ending_date)
                if date_error:
                    return jsonify({
                        'message': 'Date validation error',
                        'data': {'date_error': date_error}
                    }), 400
                # Convert dates from string to date object
                new_starting_date = datetime.strptime(new_starting_date, '%Y-%m-%d').date()
                new_ending_date = datetime.strptime(new_ending_date, '%Y-%m-%d').date()

            # Find the open position by role_name
            open_position = Open_position.query.filter_by(Role_Name=role_name).first()
            if open_position is None:
                return jsonify({'message': 'Open position not found for the given role name'}), 404

            # Update open position fields
            open_position.Starting_Date = new_starting_date
            open_position.Ending_Date = new_ending_date

            # Commit the changes to the database
            db.session.commit()

            # Return the response with None for dates if they are None
            return jsonify({
                'message': 'Open position updated successfully',
                'data': {
                    'Position_ID': open_position.Position_ID,
                    'Role_Name': open_position.Role_Name,
                    'Starting_Date': None if open_position.Starting_Date is None else open_position.Starting_Date.isoformat(),
                    'Ending_Date': None if open_position.Ending_Date is None else open_position.Ending_Date.isoformat()
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({
                "code": 500,
                "message": "Internal error: " + str(e)
            }), 500
    else:
        return jsonify({
            "code": 400,
            "message": "Please use a valid JSON request"
        }), 400

if __name__ == '__main__':
    app.run(port=5015, debug=True)
