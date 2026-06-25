# Campus Placement Management System

## Overview

Campus Placement Management System is a web-based application developed using Python Flask, SQLite, HTML, CSS, and Bootstrap. The system helps placement officers manage student records, company details, eligibility checks, job applications, and application statuses through a centralized dashboard.

## Features

### Admin Authentication

* Secure Admin Login
* Session Management
* Logout Functionality

### Student Management

* Add New Students
* View Student Records
* Search Students by Roll Number
* Duplicate Student Prevention

### Company Management

* Add New Companies
* View Company Details
* Search Companies by Name
* Duplicate Company Prevention

### Eligibility Checker

* Automatically checks student eligibility based on:

  * CGPA
  * Number of Backlogs
* Displays eligible companies for each student

### Application Management

* Students can apply to eligible companies
* Prevents duplicate applications
* Tracks application status

### Status Tracking

Application statuses include:

* Applied
* Shortlisted
* Selected
* Rejected

### Dashboard Analytics

* Total Students
* Total Companies
* Total Applications
* Average CGPA
* Placement Readiness Score

## Technology Stack

### Frontend

* HTML5
* CSS3
* Bootstrap 5

### Backend

* Python
* Flask

### Database

* SQLite

## Project Structure

```text
CampusPlacementManagement/
│
├── app.py
├── create_db.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── students.html
│   ├── add_company.html
│   ├── companies.html
│   ├── eligibility.html
│   ├── applications.html
│   └── dashboard.html
│
└── static/
```

## How to Run

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Create Database

```bash
python create_db.py
```

### 6. Run Application

```bash
python app.py
```

### 7. Open Browser

```text
http://127.0.0.1:5000
```

## Default Admin Credentials

```text
Username: admin
Password: admin123
```

## Future Enhancements

* Edit/Delete Students
* Edit/Delete Companies
* Placement Statistics Charts
* Export Reports to Excel/PDF
* Student Login Portal
* Cloud Deployment

## Author

Karthik V

Developed as a placement management solution for educational institutions.
