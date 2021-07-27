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
