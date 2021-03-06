# ------------Answers to the Data Exercise---------------


##### PREPARATIONS: 
### Add a new unique student record to the student table, notating and showing your work in the file created above.
INSERT INTO student (id, first_name, last_name, dob) VALUES (7, 'Priyanka', 'Goyal', '1990-05-07');


##### QUESTIONS:
### What students by first name, last name, and major name sorted alphabetically by last name have majors from the Engineering or Language Arts departments?
select s.first_name, s.last_name, major_name 
from student_major sm 
INNER JOIN 
(select m.id as maj_id, m.major_name from major m 
INNER JOIN
(SELECT d.id as depart_id from department d where d.department_name in ('Engineering', 'Language Arts'))
on m.department_id = depart_id)
on sm.major_id = maj_id
INNER JOIN
student s on s.id = sm.student_id
ORDER BY s.last_name asc;

# Another way
select s.first_name, s.last_name, TEMP.major_name 
from student_major sm 
INNER JOIN
(SELECT m.id as maj_id, m.major_name from major m where m.department_id in (
SELECT d.id as depart_id from department d where d.department_name in ('Engineering', 'Language Arts'))) as TEMP
on sm.major_id = TEMP.maj_id
INNER JOIN
student s on s.id = sm.student_id
ORDER BY s.last_name asc;


### How many students are there per major and major department?
# count of students per major
select m.id, m.major_name, count(sm.major_id) as student_major_count 
from major m
LEFT JOIN student_major sm 
on m.id = sm.major_id
GROUP BY m.id;

# Count of students per major department
Select d.id, d.department_name, SUM(student_major_count) as student_dept_count
from department d 
LEFT JOIN 
(select major.department_id as depart_id, count(sm.major_id) as student_major_count 
 from major
LEFT JOIN student_major sm 
 on major.id = sm.major_id
GROUP BY major.id) 
on d.id = depart_id
GROUP BY d.id;


### Exporting Dataset from the Database to the CSV file
import sqlite3
import pandas as pd
import os

# Get path of the current working directory
dirpath = os.getcwd()
DB_CONN = dirpath + "/student_major.db"
OUTPUT_CSV = dirpath + "/question_three.csv"

# Question query
query = "SELECT res.first_name as first_name, " \
        "res.last_name as last_name, m.major_name as major_name" \
        " from (select s.first_name, s.last_name, sm.major_id" \
        " from student_major sm LEFT join student s" \
        " on s.id = sm.student_id) as res INNER join" \
        " major m on res.major_id = m.id;"

try:
    # Connect to database
    conn = sqlite3.connect(DB_CONN)
    # Read SQL query and create an object from the database connection
    table = pd.read_sql_query(query, conn)
    # write to the csv
    table.to_csv(OUTPUT_CSV, index=False)

# Print error, if any
except sqlite3.Error as e:
    print(e)

# Close database connection
finally:
    conn.close()


### Importing Data from CSV to the Database
import sqlite3
import pandas as pd
import os

# Get path of the current working directory
dirpath = os.getcwd()
DB_CONN = dirpath + "/student_major.db"
INPUT_CSV = dirpath + "/question_three.csv"

def check_if_csv_valid(df):
    # Check if dataframe is empty
    if df.empty:
        print("Empty file. Finishing execution")
        return False

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")

    # Primary Key Check
    # Won't work here as one student is taking multiple courses
    # Won't work here as one course is been taken by multiple students
    # if df['pk'].is_unique:
    #    pass
    # else:
    #    raise Exception("Primary Key check is violated")
    return True


if INPUT_CSV.endswith('.csv'):
    # To read only student names column separated by a comma from the input file
    csv_df = pd.read_csv(INPUT_CSV, sep=',', usecols=['first_name', 'last_name'])
else:
    raise FileNotFoundError("No CSV file found, check location.")

try:
    # Connect to database
    conn = sqlite3.connect(DB_CONN)

    # Check if CSV Dataframe is valid
    if check_if_csv_valid(csv_df):
        pass
    else:
        raise Exception("Invalid input CSV file.")

    # write to the SQLite DB in the student table
    # From Pandas Docs:
    # if_exists{???fail???, ???replace???, ???append???}, default ???fail???
    #
    # How to behave if the table already exists.
    #
    #         fail: Raise a ValueError.
    #
    #         replace: Drop the table before inserting new values.
    #
    #         append: Insert new values to the existing table.
    #
    # I wanted to use student table but it was messing up the original table
    # fail, replace and append all three options are giving undesirable results with 'student' table
    # It's adding null values to the blank columns
    # I wanted to say that if record exists in the table student then pass else insert
    # Pandas does not have 'UPSERT' functionality
    # I am solely creating a separate table to store students name
    csv_df.to_sql("MyTable", conn, if_exists='replace', index=False)

# Print error, if any
except sqlite3.Error as e:
    print(e)

# Close database connection
finally:
    conn.close()
