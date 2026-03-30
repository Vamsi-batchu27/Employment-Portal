import os
import subprocess
import sys
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import customtkinter as ctk
from database import connect_db 

# === Fetch available jobs from DB ===
def fetch_available_jobs(filter_skills=None):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT job_id, job_title, job_description, required_skills, experience_required FROM jobs"
    if filter_skills:
        query += " WHERE required_skills LIKE %s"
        cursor.execute(query, (f"%{filter_skills}%",))
    else:
        cursor.execute(query)
    jobs = cursor.fetchall()
    db.close()
    return jobs

# === Apply for job ===
def apply_for_job(user, job):
    experience = user.get("experience", 0)
    if experience < job['experience_required']:
        messagebox.showwarning("Insufficient Experience", f"This job requires at least {job['experience_required']} years.")
        return

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM applications WHERE user_id = %s AND job_id = %s", (user['user_id'], job['job_id']))
    if cursor.fetchone():
        messagebox.showwarning("Already Applied", "You have already applied for this job.")
    else:
        cursor.execute("INSERT INTO applications (user_id, job_id) VALUES (%s, %s)", (user['user_id'], job['job_id']))
        db.commit()
        messagebox.showinfo("Success", "Application submitted successfully!")
    db.close()

# === Show job details popup ===
def show_details(j, user, reopen_dashboard_callback):
    detail_win = ctk.CTkToplevel()
    detail_win.title("Job Details")
    detail_win.geometry("500x480")
    detail_win.configure(fg_color="#E8EAF6")

    header = ctk.CTkFrame(detail_win, fg_color="#4B89DC", height=60)
    header.pack(fill="x")
    ctk.CTkLabel(header, text="Job Details", font=("Arial", 20, "bold"), text_color="white").pack(pady=15)

    content_frame = ctk.CTkFrame(detail_win, fg_color="#E8EAF6")
    content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    ctk.CTkLabel(content_frame, text="Job Title:", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 0))
    ctk.CTkLabel(content_frame, text=j['job_title'], font=("Arial", 13)).pack(anchor="w")

    ctk.CTkLabel(content_frame, text="Description:", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 0))
    ctk.CTkLabel(content_frame, text=j['job_description'], font=("Arial", 13), wraplength=440, justify="left").pack(anchor="w")

    ctk.CTkLabel(content_frame, text="Skills Required:", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 0))
    ctk.CTkLabel(content_frame, text=j['required_skills'], font=("Arial", 13)).pack(anchor="w")

    ctk.CTkLabel(content_frame, text="Experience:", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 0))
    ctk.CTkLabel(content_frame, text=f"{j['experience_required']} years", font=("Arial", 13)).pack(anchor="w")

    btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    btn_frame.pack(pady=20)

    ctk.CTkButton(btn_frame, text="Back", fg_color="#FFA500", width=120, height=40,
                  command=lambda: (detail_win.destroy(), reopen_dashboard_callback())).pack(side="left", padx=10)

    ctk.CTkButton(btn_frame, text="Apply", fg_color="#4CAF50", width=150, height=40,
                  command=lambda: apply_for_job(user, j)).pack(side="right", padx=10)

# === Update job list based on search ===
def update_job_list(jobs_canvas, jobs_frame, user, seeker_window):
    for widget in jobs_frame.winfo_children():
        widget.destroy()

    search_input = ""
    for widget in seeker_window.winfo_children():
        if isinstance(widget, ctk.CTkFrame):
            for sub in widget.winfo_children():
                if isinstance(sub, ctk.CTkFrame):
                    for entry in sub.winfo_children():
                        if isinstance(entry, ctk.CTkEntry):
                            search_input = entry.get()

    jobs = fetch_available_jobs(filter_skills=search_input.strip())

    if not jobs:
        ctk.CTkLabel(jobs_frame, text="No jobs found.", font=("Arial", 14), text_color="red").pack(pady=20)
        return

    for job in jobs:
        job_card = ctk.CTkFrame(jobs_frame, fg_color="#E8EAF6", corner_radius=10)
        job_card.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(job_card, text=job['job_title'], font=("Arial", 14, "bold"), text_color="#333").pack(anchor="w", padx=10, pady=2)
        ctk.CTkLabel(job_card, text=f"Experience: {job['experience_required']} years", font=("Arial", 12), text_color="#666").pack(anchor="w", padx=10)
        ctk.CTkLabel(job_card, text=f"Skills: {job['required_skills']}", font=("Arial", 12), text_color="#666").pack(anchor="w", padx=10)

        btn_frame = ctk.CTkFrame(job_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(btn_frame, text="View Details", fg_color="#FFA500", width=120,
                      command=lambda j=job: (seeker_window.destroy(), show_details(j, user, lambda: job_seeker_dashboard(user)))).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Apply", fg_color="#4CAF50", width=100,
                      command=lambda j=job: apply_for_job(user, j)).pack(side="right", padx=5)

    jobs_canvas.update_idletasks()
    jobs_canvas.configure(scrollregion=jobs_canvas.bbox("all"))

# === Show applied jobs window ===
def fetch_applied_jobs(user_id):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT j.job_title, j.required_skills, j.experience_required, j.job_description
        FROM jobs j
        INNER JOIN applications a ON j.job_id = a.job_id
        WHERE a.user_id = %s
    """, (user_id,))
    jobs = cursor.fetchall()
    db.close()
    return jobs

def show_applied_jobs(user, reopen_dashboard_callback):
    window = ctk.CTkToplevel()
    window.title("Applied Jobs")
    window.geometry("500x450")
    window.configure(fg_color="#E8EAF6")

    ctk.CTkLabel(window, text="Applied Jobs", font=("Arial", 18, "bold")).pack(pady=10)

    applied_jobs = fetch_applied_jobs(user["user_id"])
    if not applied_jobs:
        ctk.CTkLabel(window, text="You haven't applied to any jobs yet.", font=("Arial", 14), text_color="gray").pack(pady=20)
    else:
        scroll_canvas = ctk.CTkCanvas(window, height=300, bg="#FFFFFF", bd=0, highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(window, orientation="vertical", command=scroll_canvas.yview)
        frame = ctk.CTkFrame(scroll_canvas, fg_color="#FFFFFF")
        scroll_canvas.create_window((0, 0), window=frame, anchor="nw")

        for job in applied_jobs:
            job_card = ctk.CTkFrame(frame, fg_color="#E8EAF6", corner_radius=10)
            job_card.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(job_card, text=job['job_title'], font=("Arial", 14, "bold"), text_color="#333").pack(anchor="w", padx=10)
            ctk.CTkLabel(job_card, text=f"Skills: {job['required_skills']}", font=("Arial", 12)).pack(anchor="w", padx=10)
            ctk.CTkLabel(job_card, text=f"Experience: {job['experience_required']} years", font=("Arial", 12)).pack(anchor="w", padx=10)
            ctk.CTkLabel(job_card, text=job['job_description'], wraplength=450, justify="left", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

        frame.bind("<Configure>", lambda _: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        scroll_canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")

    ctk.CTkButton(window, text="Back", fg_color="#FFA500", width=120, height=40,
                  command=lambda: (window.destroy(), reopen_dashboard_callback())).pack(pady=20)

# === Main Dashboard Function ===
def job_seeker_dashboard(user):
    seeker_window = ctk.CTkToplevel()
    seeker_window.title("Job Seeker Dashboard")
    seeker_window.geometry("900x600")
    seeker_window.resizable(False, False)
    ctk.set_appearance_mode("light")

    # Sidebar
    sidebar = ctk.CTkFrame(seeker_window, width=200, fg_color="#4B89DC")
    sidebar.pack(side="left", fill="y")

    # Profile Image
    try:
        profile_img_path = "images/profile.png"
        profile_img = Image.open(profile_img_path).resize((80, 80), Image.LANCZOS)

        mask = Image.new('L', profile_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 80, 80), fill=255)
        profile_img.putalpha(mask)

        profile_img = ImageTk.PhotoImage(profile_img)
        profile_label = ctk.CTkLabel(sidebar, image=profile_img, text="")
        profile_label.image = profile_img
        profile_label.pack(pady=(30, 10))
    except:
        ctk.CTkLabel(sidebar, text="👤", font=("Arial", 40), text_color="white").pack(pady=(30, 10))

    ctk.CTkLabel(sidebar, text=user["username"], font=("Arial", 14, "bold"), text_color="white").pack(pady=(0, 20))

    ctk.CTkButton(
        sidebar, text="📄 View Applied Jobs", fg_color="#3A75C4", hover_color="#3366B8",
        text_color="white", width=180, height=40,
        command=lambda: (seeker_window.destroy(), show_applied_jobs(user, lambda: job_seeker_dashboard(user)))
    ).pack(pady=10)

    ctk.CTkLabel(sidebar, text="").pack(expand=True)
    def show_login_page():
        subprocess.Popen([sys.executable, "login.py"])
        
    ctk.CTkButton(
        sidebar, text="Logout", fg_color="#F44336", hover_color="#D32F2F",
        text_color="white", width=180, height=40,
        command=lambda: (seeker_window.destroy(), show_login_page())
    ).pack(pady=20)

    # Main Content
    content = ctk.CTkFrame(seeker_window, fg_color="#F4F4F4")
    content.pack(side="right", fill="both", expand=True)

    ctk.CTkLabel(content, text=f"Welcome, {user['username']}!", font=("Arial", 20, "bold"), text_color="#333").pack(pady=20)

    search_frame = ctk.CTkFrame(content, fg_color="#E8EAF6")
    search_frame.pack(fill="x", padx=20, pady=10)

    skills_entry = ctk.CTkEntry(search_frame, width=350, placeholder_text="Search jobs by skills...")
    skills_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)

    ctk.CTkButton(search_frame, text="Search", fg_color="#4B89DC", text_color="white", width=100, height=30,
                  command=lambda: update_job_list(jobs_canvas, jobs_frame, user, seeker_window)).pack(side="right", padx=10, pady=10)

    jobs_canvas = ctk.CTkCanvas(content, height=400, bg="#FFFFFF", bd=0, highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(content, orientation="vertical", command=jobs_canvas.yview)
    jobs_frame = ctk.CTkFrame(jobs_canvas, fg_color="#FFFFFF")
    jobs_window = jobs_canvas.create_window((0, 0), window=jobs_frame, anchor="nw")

    content.bind("<Configure>", lambda e: jobs_canvas.itemconfig(jobs_window, width=content.winfo_width() - 40))
    jobs_canvas.configure(yscrollcommand=scrollbar.set)
    jobs_frame.bind("<Configure>", lambda e: jobs_canvas.configure(scrollregion=jobs_canvas.bbox("all")))
    jobs_canvas.bind_all("<MouseWheel>", lambda e: jobs_canvas.yview_scroll(-1 * (e.delta // 120), "units"))

    jobs_canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
    scrollbar.pack(side="right", fill="y")

    update_job_list(jobs_canvas, jobs_frame, user, seeker_window)
    seeker_window.mainloop()
