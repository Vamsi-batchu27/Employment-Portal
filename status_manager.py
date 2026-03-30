import mysql.connector
from tkinter import messagebox
from database import connect_db

def show_application_status(user, job):
    """Displays the application status and interview details (if scheduled)."""
    db = connect_db()
    cursor = db.cursor(dictionary=True)

    # Check if user has applied for the job
    cursor.execute("SELECT applied_at FROM applications WHERE user_id = %s AND job_id = %s", (user['user_id'], job['job_id']))
    application = cursor.fetchone()

    if not application:
        messagebox.showinfo("Application Status", f"You have not applied for '{job['job_title']}' yet.")
        db.close()
        return

    # Check if interview is scheduled
    cursor.execute("""
        SELECT interview_date, interview_time, mode, status 
        FROM interviews 
        WHERE user_id = %s AND job_id = %s
    """, (user['user_id'], job['job_id']))
    interview = cursor.fetchone()

    db.close()

    if interview:
        interview_info = (f"Application Submitted: {application['applied_at']}\n"
                        f"Interview Date: {interview['interview_date']}\n"
                        f"Interview Time: {interview['interview_time']}\n"
                        f"Mode: {interview['mode']}\n"
                        f"Status: {interview['status']}")
    else:
        interview_info = f"Application Submitted: {application['applied_at']}\nInterview: Not Scheduled"

    messagebox.showinfo("Application Status", f"You have applied for '{job['job_title']}' successfully!\n\n{interview_info}")
