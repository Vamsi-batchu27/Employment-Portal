import customtkinter as ctk
from database import connect_db
from tkinter import messagebox
from datetime import datetime  # Import datetime module

def schedule_interview(user_id, job_id, employer_id):
    """Schedule an interview with the selected applicant"""
    interview_window = ctk.CTkToplevel()
    interview_window.title("Schedule Interview")
    interview_window.geometry("400x300")

    ctk.CTkLabel(interview_window, text=f"Schedule Interview with User ID: {user_id}", font=("Arial", 16, "bold")).pack(pady=10)

    date_entry = ctk.CTkEntry(interview_window, placeholder_text="Enter Date (YYYY-MM-DD)", width=300)
    date_entry.pack(pady=5)

    time_entry = ctk.CTkEntry(interview_window, placeholder_text="Enter Time (HH:MM AM/PM)", width=300)
    time_entry.pack(pady=5)

    mode_entry = ctk.CTkEntry(interview_window, placeholder_text="Enter Mode (Online/In-Person)", width=300)
    mode_entry.pack(pady=5)

    def confirm_interview():
        date = date_entry.get().strip()
        time = time_entry.get().strip()
        mode = mode_entry.get().strip()

        if not date or not time or not mode:
            messagebox.showerror("Error", "All fields are required!")
            return

        # ✅ Convert time to 24-hour format
        try:
            time_24hr = datetime.strptime(time, "%I:%M %p").strftime("%H:%M:%S")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format! Use 'HH:MM AM/PM' (e.g., 11:00 AM).")
            return

        db = connect_db()
        cursor = db.cursor()

        # Insert interview data with user_id, job_id, and employer_id
        cursor.execute("""
            INSERT INTO interviews (user_id, job_id, employer_id, interview_date, interview_time, mode) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, job_id, employer_id, date, time_24hr, mode))

        db.commit()
        db.close()

        messagebox.showinfo("Success", f"Interview Scheduled on {date} at {time} ({mode})")
        interview_window.destroy()

    # Buttons
    ctk.CTkButton(interview_window, text="Confirm", fg_color="#4CAF50", text_color="white", width=200, height=40,
                font=("Arial", 14, "bold"), corner_radius=10, command=confirm_interview).pack(pady=10)

    ctk.CTkButton(interview_window, text="Cancel", fg_color="#FF9800", text_color="white", width=200, height=40,
                font=("Arial", 14, "bold"), corner_radius=10, command=interview_window.destroy).pack(pady=5)
