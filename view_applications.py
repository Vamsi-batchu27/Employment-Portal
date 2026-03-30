import customtkinter as ctk
from tkinter import messagebox
from database import connect_db

def open_applications_window(job, user):
    window = ctk.CTkToplevel()
    window.title(f"Applicants for {job['job_title']}")
    window.geometry("600x500")
    window.configure(fg_color="#E8EAF6")
    window.resizable(False, False)

    # === Title ===
    header = ctk.CTkFrame(window, fg_color="#E8EAF6")
    header.pack(fill="x", pady=10, padx=15)

    ctk.CTkLabel(header, text=f"👥 Applications for: {job['job_title']}",
                 font=("Arial", 18, "bold"), text_color="#333").pack(side="left")

    # Back to Jobs
    def back_to_jobs():
        window.destroy()
        if user['role'] == "admin":
            from admin_dashboard import admin_dashboard
            admin_dashboard(user)
        else:
            from view_jobs import open_view_jobs_window
            open_view_jobs_window(user)

    ctk.CTkButton(header, text="Back", fg_color="#FFA500", text_color="white",
                  font=("Arial", 13, "bold"), width=100, height=35,
                  command=back_to_jobs).pack(side="right")

    # === Scrollable Canvas Setup ===
    canvas = ctk.CTkCanvas(window, height=370, bg="#E8EAF6", highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(window, orientation="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(5, 10))
    scrollbar.pack(side="right", fill="y", padx=(0, 10))

    frame = ctk.CTkFrame(canvas, fg_color="#E8EAF6")
    canvas_window = canvas.create_window((0, 0), window=frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())

    frame.bind("<Configure>", on_frame_configure)

    # === Load Applicants ===
    def load_applicants():
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*, u.name, u.email, u.experience, u.user_id
            FROM applications a
            JOIN users u ON a.user_id = u.user_id
            WHERE a.job_id = %s
        """, (job['job_id'],))
        applicants = cursor.fetchall()
        db.close()

        if not applicants:
            ctk.CTkLabel(frame, text="No applications yet.",
                         font=("Arial", 14), text_color="#777").pack(pady=30)
            return

        for applicant in applicants:
            card = ctk.CTkFrame(frame, fg_color="white", corner_radius=10)
            card.pack(fill="x", padx=15, pady=10)

            ctk.CTkLabel(card, text=f"{applicant['name']} | {applicant['email']}",
                         font=("Arial", 14, "bold"), text_color="black").pack(anchor="w", padx=15, pady=(10, 0))

            ctk.CTkLabel(card, text=f"Experience: {applicant['experience']} years",
                         font=("Arial", 12), text_color="#444").pack(anchor="w", padx=15)

            ctk.CTkLabel(card, text=f"Applied At: {applicant['applied_at']}",
                         font=("Arial", 12), text_color="#555").pack(anchor="w", padx=15, pady=(0, 10))

            # Schedule Button
            ctk.CTkButton(
                card, text="Schedule Interview", width=160, height=35,
                font=("Arial", 12, "bold"), fg_color="#4BA3FF", text_color="white",
                command=lambda a=applicant: schedule_interview_form(a, job, user)
            ).pack(anchor="e", padx=15, pady=(0, 10))

    load_applicants()

    # === Interview Scheduling Popup ===
    def schedule_interview_form(applicant, job, employer):
        form_win = ctk.CTkToplevel()
        form_win.title("Schedule Interview")
        form_win.geometry("400x400")
        form_win.configure(fg_color="#E8EAF6")
        form_win.resizable(False, False)

        ctk.CTkLabel(form_win, text="📅 Schedule Interview", font=("Arial", 20, "bold"),
                     text_color="#333").pack(pady=20)

        ctk.CTkLabel(form_win, text="Interview Date (YYYY-MM-DD):", font=("Arial", 13),
                     text_color="#333").pack(pady=(10, 2))
        date_entry = ctk.CTkEntry(form_win, width=200, placeholder_text="2025-04-01")
        date_entry.pack()

        ctk.CTkLabel(form_win, text="Interview Time (HH:MM):", font=("Arial", 13),
                     text_color="#333").pack(pady=(15, 2))
        time_entry = ctk.CTkEntry(form_win, width=200, placeholder_text="14:00")
        time_entry.pack()

        ctk.CTkLabel(form_win, text="Interview Mode:", font=("Arial", 13),
                     text_color="#333").pack(pady=(15, 2))
        mode_var = ctk.StringVar(value="Online")
        ctk.CTkOptionMenu(form_win, variable=mode_var, values=["Online", "In-Person"]).pack()

        def confirm_schedule():
            date = date_entry.get().strip()
            time = time_entry.get().strip()
            mode = mode_var.get()

            if not date or not time:
                messagebox.showerror("Error", "Please enter date and time.")
                return

            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("""
                    INSERT INTO interviews (user_id, job_id, employer_id, interview_date, interview_time, mode)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    applicant['user_id'],
                    job['job_id'],
                    employer['user_id'],
                    date,
                    time,
                    mode
                ))
                db.commit()
                db.close()

                messagebox.showinfo("Success", f"Interview scheduled with {applicant['name']} on {date} at {time}.")
                form_win.destroy()
                window.destroy()
                if user['role'] == "admin":
                    from admin_dashboard import admin_dashboard
                    admin_dashboard(user)
                else:
                    from employer_dashboard import employer_dashboard
                    employer_dashboard(user)
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

        def close_form_and_go_back():
            form_win.destroy()
            window.destroy()
            if user['role'] == "admin":
                from admin_dashboard import admin_dashboard
                admin_dashboard(user)
            else:
                from employer_dashboard import employer_dashboard
                employer_dashboard(user)

        # Buttons
        button_frame = ctk.CTkFrame(form_win, fg_color="transparent")
        button_frame.pack(pady=30)

        ctk.CTkButton(button_frame, text="✅ Confirm", width=100,
                      fg_color="#4CAF50", text_color="white",
                      command=confirm_schedule).pack(side="left", padx=10)

        ctk.CTkButton(button_frame, text="Back", width=100,
                      fg_color="#F44336", text_color="white",
                      command=close_form_and_go_back).pack(side="left", padx=10)
