import customtkinter as ctk
from database import connect_db

def match_jobs(user):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT skills FROM resumes WHERE user_id=%s", (user['id'],))
    resume_data = cursor.fetchone()

    if not resume_data:
        return

    user_skills = set(resume_data[0].lower().split(','))

    cursor.execute("SELECT job_title, required_skills FROM jobs")
    jobs = cursor.fetchall()
    db.close()

    matched_jobs = []
    for job in jobs:
        job_title, required_skills = job
        job_skills = set(required_skills.lower().split(','))

        if user_skills.intersection(job_skills):
            matched_jobs.append(job_title)

    job_window = ctk.CTkToplevel()
    job_window.title("Matched Jobs")

    for job in matched_jobs:
        ctk.CTkLabel(job_window, text=job, font=("Arial", 12)).pack(pady=2)
    
    ctk.CTkButton(job_window, text="Close", command=job_window.destroy).pack(pady=5)
