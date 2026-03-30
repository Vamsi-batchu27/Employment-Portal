# 💼 Smart Job Portal Application

A GUI-based desktop application built with Python that streamlines the hiring process for both job seekers and employers — featuring secure authentication, real-time job search, resume management, and robust database operations.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Database Schema](#database-schema)
- [Screenshots](#screenshots)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The **Smart Job Portal Application** is a desktop solution designed to address inefficiencies in the traditional hiring pipeline. It provides a clean, intuitive interface for candidates to search and apply for jobs, and for employers to post listings and manage applications — all within a single, locally-run application.

---

## ✨ Features

### 👤 Authentication & Access Control
- Secure user registration and login for both **Candidates** and **Employers**
- **Hashed password storage** to protect user credentials
- **Role-based access control (RBAC)** ensuring users only access features relevant to their role

### 🔍 Job Search & Filtering
- Real-time job search with dynamic filtering by keyword, location, category, and more
- Instant results update as filter criteria change

### 📄 Resume Management
- Resume upload functionality for candidates
- Organized storage and retrieval of uploaded documents

### 📢 Job Posting (Employer)
- Employers can create, edit, and delete job listings
- Full CRUD support for managing job postings and applicant data

### 🗃️ Database Operations
- SQL-based CRUD operations for all entities: users, job listings, applications, and profiles
- Input validation and exception handling to prevent bad data and ensure a smooth experience
- Optimized queries for fast data retrieval

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.x |
| GUI Framework | Tkinter |
| Database | SQL (SQLite / MySQL) |
| IDE | PyCharm |
| Password Security | Hashing (e.g., `hashlib` / `bcrypt`) |

---

## 📁 Project Structure

```
smart-job-portal/
│
├── main.py                  # Application entry point
├── auth/
│   ├── login.py             # Login screen and authentication logic
│   ├── register.py          # Registration screen
│   └── password_utils.py    # Password hashing utilities
│
├── employer/
│   ├── dashboard.py         # Employer dashboard
│   ├── post_job.py          # Job posting form
│   └── manage_listings.py   # View/edit/delete listings
│
├── candidate/
│   ├── dashboard.py         # Candidate dashboard
│   ├── job_search.py        # Search and filter jobs
│   ├── apply.py             # Job application screen
│   └── resume_upload.py     # Resume upload functionality
│
├── database/
│   ├── db_connection.py     # Database connection setup
│   ├── schema.sql           # SQL schema definition
│   └── queries.py           # Reusable query functions
│
├── assets/                  # Icons, images, fonts
├── requirements.txt         # Python dependencies
└── README.md
```

> **Note:** Update this structure to match your actual project layout.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- SQLite (built-in) or MySQL Server

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/smart-job-portal.git
   cd smart-job-portal
   ```

2. **Create and activate a virtual environment** *(recommended)*
   ```bash
   python -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python database/db_connection.py
   ```
   This will create and initialize the database using the schema defined in `schema.sql`.

5. **Run the application**
   ```bash
   python main.py
   ```

---

## 🗄️ Database Schema

The application uses the following core tables:

| Table | Description |
|---|---|
| `users` | Stores all user accounts (candidates & employers) with hashed passwords and roles |
| `job_listings` | All job postings created by employers |
| `applications` | Tracks candidate applications to specific jobs |
| `resumes` | Stores resume file paths/metadata linked to candidates |
| `profiles` | Extended profile information for users |

---

## 🔐 Security

- All passwords are **hashed before storage** — plain-text passwords are never saved to the database.
- **Role-based access control** prevents candidates from accessing employer features and vice versa.
- User inputs are **validated and sanitized** before database operations to prevent injection attacks.
- Exception handling is implemented throughout to gracefully manage errors without exposing sensitive information.

---

## 🖼️ Screenshots

> Add screenshots of your application here.

```
screenshots/
├── login_screen.png
├── candidate_dashboard.png
├── job_search.png
├── employer_dashboard.png
└── post_job_form.png
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature-name`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👩‍💻 Author

**Your Name**  
[GitHub](https://github.com/your-username) • [LinkedIn](https://linkedin.com/in/your-profile)

---

> Built with ❤️ using Python & Tkinter
