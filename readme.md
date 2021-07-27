# Student Majors Exercise 
Project readme file created. 

## Author: Priyanka Goyal

-------------------------------------------
## PREREQUISITES:

1. RHEL 7
2. python3 --version: 3.7.11
3. git --version: 1.8.3.1
-------------------------------------------
## PREPARATIONS:

1. Initialized git enabled cu_project directory to track all the commits.
2. Used ```create_db.py``` to create a SQLite3 local db.
3. Created 'answers.py' to submit answers to the data exercise.
4. Added a new unique record to the student table.
-------------------------------------------
## QUESTIONS:
1. Anwer written using Sub query and Multiple INNER JOINS - two methods added. 
2. Answer written using Left Joins, aggregate functions like COUNT(), SUM() and using GROUP BY. 
3. Export CSV file from the database using Pandas. Use ```export_csv.py``` to run the Python script separately.
4. Import CSV file into the database using Pandas. Use ```import_csv.py``` to run the Python script separately.

For Question4: I uploaded the students names in a new table than the already existing students table as
it was creating integrity violation. I was looking for 'UPSERT' type of functionality but in Pandas it only
exists at the Table level, not at the records level. I wanted to add a check that if the name exist in table student then
pass else insert student name. But with the incoming data from .csv file makes it hard to create a testcase. 
Here, validating would be making sure the student names are available before trying to UPDATE that change. 

If I was using students table, then the whole table was overfilling with repeatitive values, getting dropped or raising ValueError. 
If I had used the combination of Student, major then update won't work because it would update all of the students having multiple subjects.

I would be open to discuss the solution for this question. Thank you. 
