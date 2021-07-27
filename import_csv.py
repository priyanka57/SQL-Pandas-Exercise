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
    # if_exists{‘fail’, ‘replace’, ‘append’}, default ‘fail’
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

