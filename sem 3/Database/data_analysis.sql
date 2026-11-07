-- =============================================================================
-- Data Analysis Queries Script: data_analysis.sql
-- Description: Analytical SQL queries to fulfill requirement Part 2 of Week 3 Assignment.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Query 1: Average Salary by Department
-- Requirement: Calculate average salary per department, only for departments 
--              where average salary exceeds $60,000. Must use GROUP BY and 
--              HAVING clauses together.
-- -----------------------------------------------------------------------------
SELECT 
    department,
    ROUND(AVG(salary), 2) AS average_salary
FROM 
    Instructors
GROUP BY 
    department
HAVING 
    AVG(salary) > 60000.00
ORDER BY 
    average_salary DESC;


-- -----------------------------------------------------------------------------
-- Query 2: Distinct Instructor Count for 'Spring' 2024
-- Requirement: Find the count of distinct instructors teaching in 'Spring' 2024.
--              Must use the DISTINCT keyword within the aggregate function to 
--              avoid double-counting instructors who teach multiple courses.
-- -----------------------------------------------------------------------------
SELECT 
    semester,
    year,
    COUNT(DISTINCT instructor_id) AS total_distinct_instructors
FROM 
    Courses
WHERE 
    semester = 'Spring' AND year = 2024
GROUP BY 
    semester, year;
