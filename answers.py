# Answers to the Data Exercise

# PREPARATIONS: 
# Add a new unique student record to the student table, notating and showing your work in the file created above.
insert into student (id, first_name, last_name, dob) values (7, 'Priyanka', 'Goyal', '1990-05-07');

# QUESTIONS:
# What students by first name, last name, and major name sorted alphabetically by last name have majors from the Engineering or Language Arts departments?
select s.first_name, s.last_name, TEMP.major_name 
from student_major sm 
inner join 
(SELECT m.id as maj_id, m.major_name from major m where m.department_id in (
SELECT d.id as depart_id from department d where d.department_name in ('Engineering', 'Language Arts'))) as TEMP
on sm.major_id = TEMP.maj_id
INNER JOIN
student s on s.id = sm.student_id
order by s.last_name asc;

# How many students are there per major and major department?


