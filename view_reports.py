import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox, filedialog
from database import connect_db

def fetch_kpis():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='job_seeker'")
    job_seekers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='employer'")
    employers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications")
    total_applications = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM interviews WHERE status='Scheduled'")
    scheduled_interviews = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM interviews WHERE status='Completed'")
    completed_interviews = cursor.fetchone()[0]

    cursor.execute("SELECT user_id, username, email, role FROM users")
    users_data = cursor.fetchall()

    cursor.execute("SELECT job_id, job_title, experience_required FROM jobs")
    jobs_data = cursor.fetchall()

    db.close()
    return (job_seekers, employers, total_jobs, total_applications, scheduled_interviews, completed_interviews, users_data, jobs_data)

def export_to_excel(metrics, users_data, jobs_data):
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save KPI Report As"
        )
        if not file_path:
            return  # Cancelled

        report_name = "Job Matching System KPI Report"

        with pd.ExcelWriter(file_path) as writer:
            summary = pd.DataFrame({"Report Name": [report_name]})
            summary.to_excel(writer, sheet_name="KPI_Report", index=False, startrow=0)

            data = {
                "Metric": [
                    "Total Job Seekers", "Total Employers", "Total Jobs Posted", 
                    "Total Applications", "Scheduled Interviews", "Completed Interviews"
                ],
                "Count": metrics[:6]
            }

            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name="KPI_Report", index=False, startrow=3)

            users_df = pd.DataFrame(users_data, columns=["User ID", "Username", "Email", "Role"])
            users_df.to_excel(writer, sheet_name="Users", index=False)

            jobs_df = pd.DataFrame(jobs_data, columns=["Job ID", "Job Title", "Experience Required"])
            jobs_df.to_excel(writer, sheet_name="Jobs", index=False)

        messagebox.showinfo("Success", f"KPI Report saved to:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export Excel file.\n{str(e)}")

def create_graph(metrics, parent_frame):
    labels = [
        "Job Seekers", "Employers", "Jobs", 
        "Applications", "Scheduled Interviews", "Completed Interviews"
    ]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, metrics)
    ax.set_title("System KPIs Overview")
    ax.set_ylabel("Count")
    plt.xticks(rotation=30)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

def open_reports_window(user):
    window = ctk.CTkToplevel()
    window.title("\ud83d\udcca Admin Reports")
    window.geometry("700x700")
    window.configure(fg_color="#E8EAF6")

    # Divide into top, middle, bottom
    top_frame = ctk.CTkFrame(window, fg_color="#E8EAF6", height=80)
    top_frame.pack(fill="x", pady=5)

    middle_frame = ctk.CTkFrame(window, fg_color="#E8EAF6")
    middle_frame.pack(fill="both", expand=True, pady=5)

    bottom_frame = ctk.CTkFrame(window, fg_color="#E8EAF6", height=60)
    bottom_frame.pack(fill="x", pady=5)

    ctk.CTkLabel(top_frame, text="System KPI Report", font=("Arial", 22, "bold"), text_color="#673AB7").pack(pady=10)

    try:
        metrics = fetch_kpis()
        users_data = metrics[6]
        jobs_data = metrics[7]

        canvas = ctk.CTkCanvas(middle_frame, bg="#E8EAF6", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(middle_frame, orientation="vertical", command=canvas.yview)
        scroll_frame = ctk.CTkFrame(canvas, fg_color="#E8EAF6")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        table_frame = ctk.CTkFrame(scroll_frame, fg_color="#FFFFFF")
        table_frame.pack(pady=5, padx=20, fill="both", expand=False)

        header_font = ("Arial", 12, "bold")
        data_font = ("Arial", 11)

        headers = ["Metric", "Count"]
        values = [
            ["Total Job Seekers", metrics[0]],
            ["Total Employers", metrics[1]],
            ["Total Jobs Posted", metrics[2]],
            ["Total Applications", metrics[3]],
            ["Scheduled Interviews", metrics[4]],
            ["Completed Interviews", metrics[5]]
        ]

        for col, header in enumerate(headers):
            label = ctk.CTkLabel(table_frame, text=header, font=header_font, text_color="#333")
            label.grid(row=0, column=col, padx=8, pady=6)

        for row, (metric, count) in enumerate(values, start=1):
            ctk.CTkLabel(table_frame, text=metric, font=data_font).grid(row=row, column=0, padx=8, pady=4, sticky="w")
            ctk.CTkLabel(table_frame, text=str(count), font=data_font).grid(row=row, column=1, padx=8, pady=4, sticky="e")

        create_graph(metrics[:6], scroll_frame)

        ctk.CTkButton(bottom_frame, text="\ud83d\udcc5 Download as Excel", width=150, fg_color="#4CAF50", text_color="white",
                      command=lambda: export_to_excel(metrics, users_data, jobs_data)).pack(side="left", padx=15, pady=10)

        def go_back():
            import admin_dashboard
            window.destroy()
            admin_dashboard.admin_dashboard(user)

        ctk.CTkButton(bottom_frame, text="\ud83d\udd19 Back", width=120, fg_color="#FF5722",
                      command=go_back).pack(side="right", padx=15, pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load reports.\n{str(e)}")
