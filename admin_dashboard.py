import os
import sys
import customtkinter as ctk
from PIL import Image
from manage_employees import open_manage_employees_window
from view_jobs import open_view_jobs_window
from view_all_jobs import open_all_jobs_window
from view_reports import open_reports_window  # ✅ Import the new file

def admin_dashboard(user):
    window = ctk.CTkToplevel()
    window.title("Admin Dashboard")
    window.geometry("700x450")
    window.configure(fg_color="#E8EAF6")
    window.resizable(False, False)

    left_frame = ctk.CTkFrame(window, width=300, fg_color="#E8EAF6")
    left_frame.pack(side="left", fill="both")

    try:
        img = ctk.CTkImage(light_image=Image.open("images/employer.png"), size=(300, 450))
        ctk.CTkLabel(left_frame, image=img, text="").pack(fill="both", expand=True)
    except:
        ctk.CTkLabel(left_frame, text="Admin\nImage Not Found", font=("Arial", 18, "bold")).pack(expand=True)

    right_frame = ctk.CTkFrame(window, fg_color="#E8EAF6")
    right_frame.pack(side="right", fill="both", expand=True, padx=30, pady=30)

    ctk.CTkLabel(right_frame, text=f"Welcome, {user['username']} (Admin)", font=("Arial", 22, "bold"),
                 text_color="#333").pack(pady=20)

    ctk.CTkButton(right_frame, text="🔍 View All Jobs", width=250, height=45, font=("Arial", 16, "bold"),
                  fg_color="#2196F3", text_color="white",
                  command=lambda: (window.destroy(), open_all_jobs_window(user))).pack(pady=10)

    ctk.CTkButton(right_frame, text="👥 Manage Employees", width=250, height=45, font=("Arial", 16, "bold"),
                  fg_color="#673AB7", text_color="white",
                  command=lambda: (window.destroy(), open_manage_employees_window(user))).pack(pady=10)

    # ✅ View Reports Button
    ctk.CTkButton(right_frame, text="📊 View Reports", width=250, height=45, font=("Arial", 16, "bold"),
                  fg_color="#009688", text_color="white",
                  command=lambda: (window.destroy(), open_reports_window(user))).pack(pady=10)

    def restart_login():
        window.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)


    ctk.CTkButton(right_frame, text="🚪 Logout", width=150, height=40, font=("Arial", 14, "bold"),
              fg_color="#F44336", text_color="white",
              command=lambda: restart_login()).pack(pady=30)
    window.mainloop()
