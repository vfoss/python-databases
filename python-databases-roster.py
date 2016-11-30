# "Many Students in Many Courses"
# by Vicki Foss

# Week 4 Assignment for the course "Using Databases with Python"
# University of Michigan MOOC (Coursera)
# Course website: https://www.coursera.org/learn/python-databases/

# This assignment is to create a Python program to build a set of tables using the 
# Many-to-Many approach to store enrollment and role data. This application will read 
# roster data in JSON format, parse the file, and then produce an SQLite database that 
# contains a User, Course, and Member table and populate the tables from the data file.

# Note: This script was written for use with Python 2.7.12, and is available online at
# https://github.com/vfoss/python-databases/blob/master/python-databases-roster.py


# Import modules needed for this script:
import urllib
import json
import sqlite3
import os

# Set working directory to the directory containing this python script. 
# This is where the SQLite database created by this script will be stored and saved.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Open a connection to the SQLite database file "rosterdb.sqlite" 
# (or create file if it does not already exist in the directory).
conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

# Set up the tables we want in the SQLite database; 
# overwrite the tables "User", "Member" and "Course" if they already exist.
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

# For this script, we will be using the JSON data provided in the class, and which I've 
# stored in my github account at the following address:
url = 'https://raw.githubusercontent.com/vfoss/python-databases/master/roster_data.json'

# Preview the first several lines of the roster_data.json file:
# [
#   [
#     "Szymon",
#     "si110",
#     1
#   ],
#   [
#     "Safi",
#     "si110",
#     0
#   ],

# Note that this script could be modified to load similarly structured JSON data from 
# another URL or even a local file, while preserving the structure of the SQLite database
# and the functionality of this script. Since that level of customization is not required
# for this assignment, this script will automatically use the data provided in the class
# to populate the desired SQLite database.

# Fetch URL and read its contents:
str_data = urllib.urlopen(url).read()

# Deserialize data and store as a Python object:
json_data = json.loads(str_data)

# Insert our JSON data into the SQLite database we have set up above:
for entry in json_data:

    name = entry[0];
    title = entry[1];
    role = entry[2]
        # role: 1 = instructor; 0 = student

    cur.execute('''INSERT OR IGNORE INTO User (name) 
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title) 
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]
    
    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ? )''', 
        ( user_id, course_id, role ) )

# Commit changes and close the connection to the database file:
conn.commit()
conn.close()
