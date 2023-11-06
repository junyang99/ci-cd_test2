import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey

class Role(db.Model):
    __tablename__ = 'Role'

    Role_Name = db.Column(db.String(20), nullable=False, primary_key=True)
    Role_Desc = db.Column(db.String(100), nullable=False)
    # Dept = db.Column(db.String(100), nullable=False)

    def __init__(self, Role_Name, Role_Desc):
        self.Role_Name = Role_Name
        self.Role_Desc = Role_Desc
        # self.Dept = Dept

    def json(self):
        return {
            'Role_Name': self.Role_Name,
            'Role_Desc': self.Role_Desc,
            # 'Dept' : self.Dept
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

#tested
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

#Yet to test
class Staff_Skill(db.Model):
    __tablename__ = 'Staff_Skill'

    Staff_ID = db.Column(db.Integer, db.ForeignKey('Staff.Staff_ID'), nullable=False, primary_key=True)
    Skill_Name = db.Column(db.String(50), db.ForeignKey('Skill.Skill_Name'), nullable=False, primary_key = True)


    def __init__(self, Staff_ID, Skill_Name):
        self.Staff_ID = Staff_ID
        self.Skill_Name = Skill_Name


    def json(self):
        return {
            'Staff_ID': self.Staff_ID,
            'Skill_Name': self.Skill_Name
        }


class Open_Position(db.Model):
    __tablename__ = 'Open_Position'

    Position_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    Role_Name = db.Column(db.String(20), nullable=False)
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
    access_control = db.relationship(
        Access_Control, backref='staff', lazy=True)

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


class Application(db.Model):
    __tablename__ = 'Application'

    Application_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    Position_ID = db.Column(db.Integer, db.ForeignKey(
        'Open_Position.Position_ID'), nullable=False)
    Staff_ID = db.Column(db.Integer, db.ForeignKey(
        'Staff.Staff_ID'), nullable=False)
    Application_Date = db.Column(db.Date, nullable=False)
    Cover_Letter = db.Column(db.String(10000), nullable=False)
    Application_Status = db.Column(db.Integer, nullable=False)

    def __init__(self, Application_ID, Position_ID, Staff_ID, Application_Date, Cover_Letter, Application_Status):
        self.Application_ID = Application_ID
        self.Position_ID = Position_ID
        self.Staff_ID = Staff_ID
        self.Application_Date = Application_Date
        self.Cover_Letter = Cover_Letter
        self.Application_Status = Application_Status

    def json(self):
        return {
            'Application_ID': self.Application_ID,
            'Position_ID': self.Position_ID,
            'Staff_ID': self.Staff_ID,
            'Application_Date': self.Application_Date,
            'Cover_Letter': self.Cover_Letter,
            'Application_Status': self.Application_Status,
        }
