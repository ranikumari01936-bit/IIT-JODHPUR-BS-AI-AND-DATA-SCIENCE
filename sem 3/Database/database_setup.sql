-- 1. Create Students Table
CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- 2. Create Instructors Table
CREATE TABLE Instructors (
    instructor_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    salary DECIMAL(10, 2)
);

-- 3. Create Courses Table (With Foreign Key to Instructors)
CREATE TABLE Courses (
    course_id INT PRIMARY KEY,
    title VARCHAR(100),
    semester VARCHAR(20),
    year INT,
    instructor_id INT,
    FOREIGN KEY (instructor_id) REFERENCES Instructors(instructor_id)
);

-- 4. Create Enrollments Table (With Foreign Keys to Students and Courses)
CREATE TABLE Enrollments (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- INSERTING SAMPLE DATA
INSERT INTO Students (student_id, name) VALUES (1, 'Rahul'), (2, 'Priya'), (3, 'Amit'), (4, 'Neha');
INSERT INTO Instructors (instructor_id, name, department, salary) VALUES (101, 'Dr. Sharma', 'Computer Science', 75000.00), (102, 'Dr. Verma', 'Computer Science', 85000.00), (103, 'Dr. Gupta', 'Mathematics', 50000.00), (104, 'Dr. Singh', 'Physics', 65000.00);
INSERT INTO Courses (course_id, title, semester, year, instructor_id) VALUES (201, 'Database Systems', 'Spring', 2024, 101), (202, 'Operating Systems', 'Spring', 2024, 101), (203, 'Calculus II', 'Spring', 2024, 103), (204, 'Quantum Mechanics', 'Fall', 2023, 104);
INSERT INTO Enrollments (student_id, course_id) VALUES (1, 201), (1, 203), (2, 201), (2, 202), (3, 204), (4, 201);