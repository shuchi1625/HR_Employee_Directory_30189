# frontend_hr.py
import streamlit as st
import pandas as pd
from backend_hr import HRDB

db = HRDB()

st.set_page_config(page_title="HR Employee Directory", layout="wide")

# ---- Header ----
st.title("👩‍💼 HR Employee Directory & Analytics")
st.markdown("**Shuchi Iyer_30189**")

# ---- Sidebar ----
menu = ["Employee Directory", "Add Employee", "Manage Jobs", "Manage Departments", "Analytics"]
choice = st.sidebar.radio("Navigation", menu)

# ---- Employee Directory ----
if choice == "Employee Directory":
    st.header("📋 All Employees")
    data = db.list_employees()
    cols = [
        "ID",
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Hire Date",
        "Salary",
        "Job",
        "Department",
        "Manager ID",
    ]
    df = pd.DataFrame(data, columns=cols)
    st.dataframe(df, use_container_width=True)

# ---- Add Employee ----
elif choice == "Add Employee":
    st.header("➕ Add New Employee")

    jobs = db.list_jobs()
    depts = db.list_departments()
    mgrs = db.list_employees_min()

    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name *")
        last_name = st.text_input("Last Name *")
        email = st.text_input("Email *")
        phone = st.text_input("Phone")
        hire_date = st.date_input("Hire Date")
    with col2:
        salary = st.number_input("Salary", min_value=0.0, step=1000.0)
        job_id = None
        dept_id = None
        manager_id = None

        if jobs:
            job_label = st.selectbox("Job *", [f"{j[1]} (ID {j[0]})" for j in jobs])
            job_id = int(job_label.split("ID ")[1].rstrip(")"))
        else:
            st.warning("No jobs found. Add jobs in 'Manage Jobs' tab.")

        if depts:
            dept_label = st.selectbox("Department *", [f"{d[1]} (ID {d[0]})" for d in depts])
            dept_id = int(dept_label.split("ID ")[1].rstrip(")"))
        else:
            st.warning("No departments found. Add departments in 'Manage Departments' tab.")

        mgr_options = ["(None)"] + [f"{m[1]} {m[2]} (ID {m[0]})" for m in mgrs]
        mgr_label = st.selectbox("Manager (optional)", mgr_options, index=0)
        if mgr_label != "(None)":
            manager_id = int(mgr_label.split("ID ")[1].rstrip(")"))

    if st.button("Save Employee"):
        required_ok = all([first_name.strip(), last_name.strip(), email.strip(), job_id, dept_id])
        if not required_ok:
            st.error("Please fill all required fields (First/Last/Email/Job/Department).")
        else:
            try:
                db.add_employee(first_name, last_name, email, phone, hire_date, salary, job_id, dept_id, manager_id)
                st.success("Employee added successfully!")
            except Exception as e:
                st.error(f"Error adding employee: {e}")

# ---- Manage Jobs ----
elif choice == "Manage Jobs":
    st.header("💼 Jobs")

    with st.form("job_form"):
        job_title = st.text_input("Job Title *")
        min_salary = st.number_input("Min Salary", min_value=0.0, step=1000.0)
        max_salary = st.number_input("Max Salary", min_value=0.0, step=1000.0)
        submitted = st.form_submit_button("Add Job")
        if submitted:
            if job_title.strip():
                try:
                    db.add_job(job_title.strip(), min_salary, max_salary)
                    st.success("Job added successfully!")
                except Exception as e:
                    st.error(f"Error adding job: {e}")
            else:
                st.error("Job title is required.")

    jobs = db.list_jobs()
    st.subheader("Current Jobs")
    jdf = pd.DataFrame(jobs, columns=["Job ID", "Job Title", "Min Salary", "Max Salary"])
    st.dataframe(jdf, use_container_width=True)

# ---- Manage Departments ----
elif choice == "Manage Departments":
    st.header("🏢 Departments")

    with st.form("dept_form"):
        dept_name = st.text_input("Department Name *")
        location = st.text_input("Location")
        submitted = st.form_submit_button("Add Department")
        if submitted:
            if dept_name.strip():
                try:
                    db.add_department(dept_name.strip(), location.strip() if location else None)
                    st.success("Department added successfully!")
                except Exception as e:
                    st.error(f"Error adding department: {e}")
            else:
                st.error("Department name is required.")

    depts = db.list_departments()
    st.subheader("Current Departments")
    ddf = pd.DataFrame(depts, columns=["Dept ID", "Department Name", "Location"])
    st.dataframe(ddf, use_container_width=True)

# ---- Analytics ----
elif choice == "Analytics":
    st.header("📊 HR Analytics")

    # High-level salary summary
    total_emp, total_sal, avg_sal, min_sal, max_sal = db.salary_summary()
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Employees", total_emp)
    c2.metric("Total Salary", f"{total_sal:,.2f}")
    c3.metric("Avg Salary", f"{avg_sal:,.2f}")
    c4.metric("Min Salary", f"{min_sal:,.2f}")
    c5.metric("Max Salary", f"{max_sal:,.2f}")

    st.divider()

    # Employees per Department
    st.subheader("Employees per Department")
    dept_stats = db.employees_per_department()
    if dept_stats:
        dept_df = pd.DataFrame(dept_stats, columns=["Department", "Headcount"]).set_index("Department")
        st.bar_chart(dept_df)
        st.dataframe(dept_df.reset_index(), use_container_width=True)
    else:
        st.caption("No departments or employees found.")

    # Average Salary per Job
    st.subheader("Average Salary per Job")
    job_stats = db.avg_salary_per_job()
    if job_stats:
        job_df = pd.DataFrame(job_stats, columns=["Job", "Avg Salary"]).set_index("Job")
        st.bar_chart(job_df)
        st.dataframe(job_df.reset_index(), use_container_width=True)
    else:
        st.caption("No jobs/employees to calculate averages.")
