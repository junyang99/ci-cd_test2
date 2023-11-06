from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

app = Flask(__name__)

# Use GitHub secrets or environment variables to configure your database URI
db_user = os.getenv('MYSQL_USER', 'root')
db_pass = os.getenv('MYSQL_PASSWORD', 'root')
db_host = os.getenv('MYSQL_HOST', 'localhost')
db_name = os.getenv('MYSQL_DATABASE', 'HR Portal')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}/{db_name}'
db = SQLAlchemy(app)

try:
    with app.app_context():
        # Try to execute a simple query
        result = db.engine.execute('SELECT 1')
        print(next(result))  # Should print out the result of the query if successful
        print("Database connection successful.")
except Exception as e:
    print("Error connecting to the database.")
    print(str(e))
