import customtkinter as ctk
from database import connect_db
from tkinter import messagebox
from schedule_interview import schedule_interview  # Import schedule_interview function

def get_employer_id(job_id):
    """Fetch the employer ID for a given job ID"""
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT employer_id FROM jobs WHERE job_id = %s", (job_id,))
    employer_result = cursor.fetchone()
    db.close()
    return employer_result[0] if employer_result else None  # Return employer_id

def view_applicants(job_id):
    """Displays job applicants as cards with schedule interview button"""
    applicants_window = ctk.CTkToplevel()
    applicants_window.title("Job Applicants")
    applicants_window.geometry("500x500")

    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.user_id, u.username, u.email, u.experience, a.applied_at 
        FROM applications a 
        JOIN users u ON a.user_id = u.user_id 
        WHERE a.job_id = %s
    """, (job_id,))
    
    applicants = cursor.fetchall()
    db.close()

    if not applicants:
        ctk.CTkLabel(applicants_window, text="No applicants yet.", font=("Arial", 14)).pack(pady=20)
    else:
        employer_id = get_employer_id(job_id)  # Fetch employer_id once
        if not employer_id:
            messagebox.showerror("Error", "Employer not found for this job.")
            applicants_window.destroy()
            return

        for applicant in applicants:
            applicant_card = ctk.CTkFrame(applicants_window, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#CCC")
            applicant_card.pack(fill="x", padx=10, pady=5)

            # Applicant Details
            applicant_details = f"👤 {applicant['username']} | ✉ {applicant['email']}"
            applicant_label = ctk.CTkLabel(applicant_card, text=applicant_details, font=("Arial", 12, "bold"))
            applicant_label.pack(anchor="w", padx=10, pady=5)

            experience_label = ctk.CTkLabel(applicant_card, text=f"🏆 Experience: {applicant['experience']} years", font=("Arial", 12), text_color="#444")
            experience_label.pack(anchor="w", padx=10, pady=2)

            applied_at_label = ctk.CTkLabel(applicant_card, text=f"🕒 Applied At: {applicant['applied_at']}", font=("Arial", 10), text_color="#666")
            applied_at_label.pack(anchor="w", padx=10, pady=2)

            # Schedule Interview Button
            schedule_button = ctk.CTkButton(applicant_card, text="Schedule Interview", fg_color="#4CAF50", text_color="white",
                                            width=200, height=30, corner_radius=10,
                                            command=lambda u_id=applicant['user_id']: schedule_interview(u_id, job_id, employer_id))
            schedule_button.pack(pady=5)

    # Back Button
    ctk.CTkButton(applicants_window, text="Back", fg_color="#FF9800", text_color="white", width=200, height=40,
                font=("Arial", 14, "bold"), corner_radius=10, command=applicants_window.destroy).pack(pady=10)
