### Importing Data from CSV to the Database
import sqlite3
import pandas as pd
import os

# Get path of the current working directory
dirpath = os.getcwd()
DB_CONN = dirpath + "/student_major.db"
INPUT_CSV = dirpath + "/question_three.csv"

# If file exists and ends with .csv extension, read it else raise an error
if INPUT_CSV.endswith('.csv'):
    csv_df = pd.read_csv(INPUT_CSV, sep=',')
else:
    raise FileNotFoundError("No CSV file found, check location.")

try:
    # Connect to database
    conn = sqlite3.connect(DB_CONN)
    # write to the SQLite DB, first create the table
    csv_df.to_sql("MyTable", conn, if_exists='replace', index=False)

# Print error, if any
except sqlite3.Error as e:
    print(e)

# Close database connection
finally:
    conn.close()
