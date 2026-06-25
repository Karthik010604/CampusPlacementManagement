from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "placement_secret_key"


# ---------------------------
# LOGIN MODULE
# ---------------------------

@app.route("/")
def home():

    if "admin" not in session:
        return redirect("/login")

    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/verify_login", methods=["POST"])
def verify_login():

    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "admin123":

        session["admin"] = username
        return redirect("/dashboard")

    return """
    <h2>Invalid Login</h2>
    <a href='/login'>Try Again</a>
    """


@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/login")


# ---------------------------
# STUDENT MODULE
# ---------------------------

@app.route("/register")
def register():

    if "admin" not in session:
        return redirect("/login")

    return render_template("register.html")


@app.route("/save_student", methods=["POST"])
def save_student():

    name = request.form["name"]
    rollno = request.form["rollno"]
    branch = request.form["branch"]
    cgpa = request.form["cgpa"]
    backlogs = request.form["backlogs"]
    email = request.form["email"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE rollno=? OR email=?",
        (rollno, email)
    )

    existing_student = cursor.fetchone()

    if existing_student:
        conn.close()

        return """
        <h2>Student Already Exists!</h2>
        <a href='/register'>Go Back</a>
        """

    cursor.execute("""
    INSERT INTO students
    (name, rollno, branch, cgpa, backlogs, email)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        name,
        rollno,
        branch,
        cgpa,
        backlogs,
        email
    ))

    conn.commit()
    conn.close()

    return redirect("/students")


@app.route("/students")
def students():

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    student_list = cursor.fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=student_list
    )


@app.route("/search_student")
def search_student():

    if "admin" not in session:
        return redirect("/login")

    rollno = request.args.get("rollno", "")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE rollno LIKE ?",
        ('%' + rollno + '%',)
    )

    students = cursor.fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students
    )


# ---------------------------
# COMPANY MODULE
# ---------------------------

@app.route("/add_company")
def add_company():

    if "admin" not in session:
        return redirect("/login")

    return render_template("add_company.html")


@app.route("/save_company", methods=["POST"])
def save_company():

    company_name = request.form["company_name"]
    required_cgpa = request.form["required_cgpa"]
    allowed_backlogs = request.form["allowed_backlogs"]
    job_role = request.form["job_role"]
    package_offered = request.form["package_offered"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM companies WHERE company_name=?",
        (company_name,)
    )

    existing_company = cursor.fetchone()

    if existing_company:
        conn.close()

        return """
        <h2>Company Already Exists!</h2>
        <a href='/add_company'>Go Back</a>
        """

    cursor.execute("""
    INSERT INTO companies
    (
        company_name,
        required_cgpa,
        allowed_backlogs,
        job_role,
        package_offered
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        company_name,
        required_cgpa,
        allowed_backlogs,
        job_role,
        package_offered
    ))

    conn.commit()
    conn.close()

    return redirect("/companies")


@app.route("/companies")
def companies():

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM companies")

    company_list = cursor.fetchall()

    conn.close()

    return render_template(
        "companies.html",
        companies=company_list
    )


@app.route("/search_company")
def search_company():

    if "admin" not in session:
        return redirect("/login")

    company_name = request.args.get("company_name", "")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM companies WHERE company_name LIKE ?",
        ('%' + company_name + '%',)
    )

    companies = cursor.fetchall()

    conn.close()

    return render_template(
        "companies.html",
        companies=companies
    )


# ---------------------------
# ELIGIBILITY MODULE
# ---------------------------

@app.route("/eligibility/<int:student_id>")
def eligibility(student_id):

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (student_id,)
    )

    student = cursor.fetchone()

    if not student:
        conn.close()
        return "Student Not Found"

    student_cgpa = float(student[4])
    student_backlogs = int(student[5])

    cursor.execute("""
    SELECT *
    FROM companies
    WHERE required_cgpa <= ?
    AND allowed_backlogs >= ?
    """,
    (
        student_cgpa,
        student_backlogs
    ))

    eligible_companies = cursor.fetchall()

    conn.close()

    return render_template(
        "eligibility.html",
        student=student,
        companies=eligible_companies
    )


# ---------------------------
# APPLICATION MODULE
# ---------------------------

@app.route("/apply/<int:student_id>/<int:company_id>")
def apply(student_id, company_id):

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM applications
    WHERE student_id=? AND company_id=?
    """,
    (student_id, company_id))

    existing = cursor.fetchone()

    if existing:
        conn.close()

        return """
        <h2>Already Applied!</h2>
        <a href='/students'>Back</a>
        """

    cursor.execute("""
    INSERT INTO applications
    (student_id, company_id)
    VALUES (?, ?)
    """,
    (student_id, company_id))

    conn.commit()
    conn.close()

    return redirect(f"/applications/{student_id}")


@app.route("/applications/<int:student_id>")
def applications(student_id):

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        applications.id,
        companies.company_name,
        companies.job_role,
        companies.package_offered,
        applications.status

    FROM applications

    JOIN companies
    ON applications.company_id = companies.id

    WHERE applications.student_id=?
    """,
    (student_id,))

    application_list = cursor.fetchall()

    conn.close()

    return render_template(
        "applications.html",
        applications=application_list
    )


@app.route("/update_status/<int:application_id>/<status>")
def update_status(application_id, status):

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE applications
    SET status=?
    WHERE id=?
    """,
    (status, application_id))

    conn.commit()
    conn.close()

    return redirect(request.referrer)


# ---------------------------
# DASHBOARD
# ---------------------------

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM companies")
    total_companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications")
    total_applications = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(cgpa) FROM students")
    avg_cgpa = cursor.fetchone()[0]

    if avg_cgpa is None:
        avg_cgpa = 0

    readiness_score = round((avg_cgpa / 10) * 100, 2)

    conn.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_companies=total_companies,
        total_applications=total_applications,
        avg_cgpa=round(avg_cgpa, 2),
        readiness_score=readiness_score
    )


if __name__ == "__main__":
    app.run(debug=True)