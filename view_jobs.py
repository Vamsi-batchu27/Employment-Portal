import customtkinter as ctk
from database import connect_db
from view_applications import open_applications_window  # Viewer for job applications

def open_view_jobs_window(user):
    window = ctk.CTkToplevel()
    window.title("View Posted Jobs")
    window.geometry("600x500")
    window.configure(fg_color="#E8EAF6")
    window.resizable(False, False)

    # === Header Bar ===
    header_frame = ctk.CTkFrame(window, fg_color="#E8EAF6")
    header_frame.pack(fill="x", pady=10, padx=15)

    ctk.CTkLabel(header_frame, text="📋 Your Posted Jobs",
                 font=("Arial", 22, "bold"), text_color="#333").pack(side="left")

    def go_back():
        from employer_dashboard import employer_dashboard
        window.destroy()
        employer_dashboard(user)

    ctk.CTkButton(header_frame, text="🔙 Back", width=100, height=35,
                  fg_color="#FFA500", text_color="white",
                  font=("Arial", 12, "bold"), corner_radius=8,
                  command=go_back).pack(side="right")

    # === Canvas & Scrollable Frame ===
    canvas = ctk.CTkCanvas(window, height=380, bg="#FFFFFF", highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(window, orientation="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
    scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=(0, 10))

    scroll_frame = ctk.CTkFrame(canvas, fg_color="#FFFFFF")
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())

    scroll_frame.bind("<Configure>", on_frame_configure)

    # === Load Jobs from DB ===
    def load_jobs():
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs WHERE employer_id = %s", (user['user_id'],))
        jobs = cursor.fetchall()
        db.close()

        if not jobs:
            ctk.CTkLabel(scroll_frame, text="No jobs posted yet.",
                         font=("Arial", 14), text_color="#555").pack(pady=20)
            return

        for job in jobs:
            card = ctk.CTkFrame(scroll_frame, fg_color="#E8EAF6", corner_radius=10)
            card.pack(fill="x", padx=10, pady=8)

            # Job details
            ctk.CTkLabel(card, text=job['job_title'], font=("Arial", 14, "bold"),
                         text_color="#333").pack(anchor="w", padx=10, pady=(8, 0))

            ctk.CTkLabel(card, text=f"Skills: {job['required_skills']}", font=("Arial", 12),
                         text_color="#555").pack(anchor="w", padx=10)

            ctk.CTkLabel(card, text=f"Experience Required: {job['experience_required']} years",
                         font=("Arial", 12), text_color="#555").pack(anchor="w", padx=10)

            ctk.CTkLabel(card, text=job['job_description'], font=("Arial", 12),
                         text_color="#444", wraplength=560, justify="left").pack(anchor="w", padx=10, pady=(4, 10))

            # View Applications button
            def open_and_close(j):
                window.destroy()  # ✅ Close current window first
                open_applications_window(j, user)

            ctk.CTkButton(card, text="👥 View Applications", width=160, height=35,
                        font=("Arial", 12), fg_color="#2196F3", text_color="white",
                        command=lambda j=job: open_and_close(j)).pack(anchor="e", padx=10, pady=(0, 10))


    load_jobs()
