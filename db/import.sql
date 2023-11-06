-- Drop HR Portal database if it exists
DROP DATABASE IF EXISTS `HR Portal`;

-- Create the HR Portal database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `HR Portal`;

-- Use the HR Portal database
USE `HR Portal`;

-- Create the Role table
CREATE TABLE IF NOT EXISTS Role (
    Role_Name VARCHAR(20) PRIMARY KEY,
    Role_Desc TEXT,
    Department VARCHAR(50)
);


-- Create the Skill table
CREATE TABLE IF NOT EXISTS Skill (
    Skill_Name VARCHAR(50) PRIMARY KEY,
    Skill_Desc TEXT
);

-- Create the Access_Control table
CREATE TABLE IF NOT EXISTS Access_Control (
    Access_ID INT PRIMARY KEY,
    Access_Control_Name VARCHAR(20)
);

-- Create the Staff table
CREATE TABLE IF NOT EXISTS Staff (
    Staff_ID INT PRIMARY KEY,
    Staff_FName VARCHAR(50) NOT NULL,
    Staff_LName VARCHAR(50) NOT NULL,
    Dept VARCHAR(50) NOT NULL,
    Country VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Access_ID INT,
    FOREIGN KEY (Access_ID) REFERENCES Access_Control(Access_ID)
);

-- Create the Role_Skill table
CREATE TABLE IF NOT EXISTS Role_Skill (
    Role_Name VARCHAR(20),
    Skill_Name VARCHAR(50),
    PRIMARY KEY (Role_Name, Skill_Name),
    FOREIGN KEY (Role_Name) REFERENCES Role(Role_Name),
    FOREIGN KEY (Skill_Name) REFERENCES Skill(Skill_Name)
);

-- Create the Staff_Skill table
CREATE TABLE IF NOT EXISTS Staff_Skill (
    Staff_ID INT,
    Skill_Name VARCHAR(50),
    PRIMARY KEY (Staff_ID, Skill_Name),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID),
    FOREIGN KEY (Skill_Name) REFERENCES Skill(Skill_Name)
);

-- Create the Open_Position table
CREATE TABLE IF NOT EXISTS Open_Position (
    Position_ID INT AUTO_INCREMENT,
    Role_Name VARCHAR(20) NOT NULL,
    Starting_Date DATE,
    Ending_Date DATE,
    PRIMARY KEY (Position_ID),
    FOREIGN KEY (Role_Name) REFERENCES Role(Role_Name)
);

-- Create the Application table
CREATE TABLE IF NOT EXISTS Application (
    Application_ID INT AUTO_INCREMENT,
    Position_ID INT NOT NULL,
    Staff_ID INT NOT NULL,
    Application_Date DATE NOT NULL,
    Cover_Letter TEXT,
    Application_Status INT NOT NULL,
    PRIMARY KEY (Application_ID),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID),
    FOREIGN KEY (Position_ID) REFERENCES Open_Position(Position_ID)
);
