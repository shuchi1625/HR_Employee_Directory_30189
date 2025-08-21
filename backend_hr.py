# backend_hr.py
import psycopg2
from contextlib import contextmanager

# ------------------ DB CONFIG: update if needed ------------------
DB_HOST = "localhost"
DB_NAME = "Employee_Directory"   # make sure this DB exists
DB_USER = "postgres"             # your PostgreSQL username
DB_PASSWORD = "@rSHUCHI16"    # your PostgreSQL password

# ------------------ CONNECTION HELPER ------------------
@contextmanager
def get_connection():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

# ------------------ DATA ACCESS CLASS ------------------
class HRDB:
    # ===== EMPLOYEES =====
    def add_employee(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str | None,
        hire_date,           # datetime.date from Streamlit date_input
        salary: float | None,
        job_id: int | None,
        department_id: int | None,
        manager_id: int | None = None,
    ):
        with get_connection() as cur:
            cur.execute(
                """
                INSERT INTO employees
                    (first_name, last_name, email, phone_number, hire_date,
                     salary, job_id, department_id, manager_id)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """,
                (
                    first_name,
                    last_name,
                    email,
                    phone,
                    hire_date,
                    salary,
                    job_id,
                    department_id,
                    manager_id,
                ),
            )

    def list_employees(self):
        with get_connection() as cur:
            cur.execute(
                """
                SELECT
                    e.employee_id,
                    e.first_name,
                    e.last_name,
                    e.email,
                    e.phone_number,
                    e.hire_date,
                    e.salary,
                    j.job_title,
                    d.department_name,
                    e.manager_id
                FROM employees e
                LEFT JOIN jobs j ON e.job_id = j.job_id
                LEFT JOIN departments d ON e.department_id = d.department_id
                ORDER BY e.employee_id;
                """
            )
            return cur.fetchall()

    def list_employees_min(self):
        """Minimal list for selecting a manager."""
        with get_connection() as cur:
            cur.execute(
                "SELECT employee_id, first_name, last_name FROM employees ORDER BY first_name, last_name;"
            )
            return cur.fetchall()

    # ===== JOBS =====
    def add_job(self, job_title: str, min_salary: float | None, max_salary: float | None):
        with get_connection() as cur:
            cur.execute(
                """
                INSERT INTO jobs (job_title, min_salary, max_salary)
                VALUES (%s, %s, %s);
                """,
                (job_title, min_salary, max_salary),
            )

    def list_jobs(self):
        with get_connection() as cur:
            cur.execute(
                "SELECT job_id, job_title, min_salary, max_salary FROM jobs ORDER BY job_title;"
            )
            return cur.fetchall()

    # ===== DEPARTMENTS =====
    def add_department(self, department_name: str, location: str | None):
        with get_connection() as cur:
            cur.execute(
                """
                INSERT INTO departments (department_name, location)
                VALUES (%s, %s);
                """,
                (department_name, location),
            )

    def list_departments(self):
        with get_connection() as cur:
            cur.execute(
                "SELECT department_id, department_name, location FROM departments ORDER BY department_name;"
            )
            return cur.fetchall()

    # ===== ANALYTICS =====
    def employees_per_department(self):
        with get_connection() as cur:
            cur.execute(
                """
                SELECT d.department_name, COUNT(e.employee_id) AS headcount
                FROM departments d
                LEFT JOIN employees e ON d.department_id = e.department_id
                GROUP BY d.department_name
                ORDER BY headcount DESC, d.department_name;
                """
            )
            return cur.fetchall()

    def avg_salary_per_job(self):
        with get_connection() as cur:
            cur.execute(
                """
                SELECT j.job_title, ROUND(AVG(e.salary)::numeric, 2) AS avg_salary
                FROM jobs j
                LEFT JOIN employees e ON j.job_id = e.job_id
                GROUP BY j.job_title
                ORDER BY avg_salary DESC NULLS LAST, j.job_title;
                """
            )
            return cur.fetchall()

    def salary_summary(self):
        with get_connection() as cur:
            cur.execute(
                """
                SELECT
                    COUNT(*) AS total_employees,
                    COALESCE(SUM(salary), 0) AS total_salary,
                    COALESCE(ROUND(AVG(salary)::numeric, 2), 0) AS avg_salary,
                    COALESCE(MIN(salary), 0) AS min_salary,
                    COALESCE(MAX(salary), 0) AS max_salary
                FROM employees;
                """
            )
            return cur.fetchone()
