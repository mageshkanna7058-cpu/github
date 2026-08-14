import os
import sqlite3

import streamlit as st

from database import add_student, create_database
from calculations import GRADE_POINTS, calculate_cgpa, calculate_sgpa

st.set_page_config(
    page_title="CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

css_path = os.path.join("Assets", "style.css")
with open(css_path, encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

create_database()

st.title("🎓 CGPA Calculator")
st.write("Student Academic Management System")
st.divider()

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Dashboard",
        "Add Student",
        "Calculate SGPA",
        "Calculate CGPA",
        "View Students"
    ]
)

if menu == "Add Student":
    st.header("👨‍🎓 Add Student")

    name = st.text_input("Student Name")
    register_no = st.text_input("Register Number")
    department = st.selectbox(
        "Department",
        ["Computer Science and Engineering"]
    )
    batch = st.text_input("Batch", placeholder="2023-2027")

    if st.button("Add Student"):
        if name and register_no:
            try:
                add_student(name, register_no, department, batch)
                st.success("Student added successfully!")
            except sqlite3.IntegrityError:
                st.error("Register number already exists.")
        else:
            st.warning("Please enter all required details.")

if menu == "Dashboard":
    st.header("📊 Dashboard")

    conn = sqlite3.connect("database/cgpa.db")
    students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    subjects = conn.execute("SELECT COUNT(*) FROM subjects").fetchone()[0]
    conn.close()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Students", students)
    with col2:
        st.metric("Total Subjects", subjects)

    st.info("Use the sidebar to add students and calculate SGPA / CGPA.")

if menu == "Calculate SGPA":
    st.header("📚 Semester Details")

    register_no = st.text_input("Register Number")
    semester = st.number_input("Semester", min_value=1, max_value=8, step=1)
    number_of_subjects = st.number_input("Number of Subjects", min_value=1, max_value=15, step=1)

    subjects = []

    for i in range(number_of_subjects):
        st.subheader(f"Subject {i + 1}")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            code = st.text_input("Subject Code", key=f"code{i}")

        with col2:
            name = st.text_input("Subject Name", key=f"name{i}")

        with col3:
            grade = st.selectbox("Grade", list(GRADE_POINTS.keys()), key=f"grade{i}")

        with col4:
            credit = st.number_input("Credit", min_value=1.0, max_value=10.0, step=0.5, key=f"credit{i}")

        subjects.append({
            "code": code,
            "name": name,
            "grade": grade,
            "credit": credit
        })

    if st.button("Calculate SGPA"):
        sgpa = calculate_sgpa(subjects)
        st.success(f"SGPA = {sgpa:.2f}")

if menu == "Calculate CGPA":
    st.header("🎯 CGPA Calculator")

    register_no = st.text_input("Register Number")
    semesters = st.number_input("Number of Semesters", min_value=1, max_value=8, step=1)

    sgpa_list = []
    for i in range(semesters):
        sgpa = st.number_input(f"Semester {i + 1} SGPA", min_value=0.0, max_value=10.0, step=0.01)
        sgpa_list.append(sgpa)

    if st.button("Calculate CGPA"):
        cgpa = calculate_cgpa(sgpa_list)
        st.success(f"🎓 Final CGPA: {cgpa:.2f}")

if menu == "View Students":
    st.header("👥 Student Records")

    conn = sqlite3.connect("database/cgpa.db")
    students = conn.execute(
        "SELECT name, register_no, department, batch FROM students ORDER BY id"
    ).fetchall()
    conn.close()

    if not students:
        st.info("No students have been added yet.")
    else:
        for name, register_no, department, batch in students:
            st.write(f"**{name}** - {register_no} | {department} | Batch: {batch}")




