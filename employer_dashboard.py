import subprocess
import sys
import customtkinter as ctk
from PIL import Image
from post_job import open_post_job_window
from view_jobs import open_view_jobs_window
from view_interviews import open_view_interviews_window  # ✅ New import

def employer_dashboard(user):
    """Main Employer Dashboard"""

    window = ctk.CTkToplevel()
    window.title("Employer Dashboard")
    window.geometry("700x450")
    window.configure(fg_color="#E8EAF6")
    window.resizable(False, False)

    # === Left: Image Frame ===
    left_frame = ctk.CTkFrame(window, width=300, fg_color="#E8EAF6")
    left_frame.pack(side="left", fill="both")

    try:
        logo_image = ctk.CTkImage(light_image=Image.open("images/employer.png"), size=(300, 450))
        image_label = ctk.CTkLabel(left_frame, image=logo_image, text="")
        image_label.pack(fill="both", expand=True)
    except:
        ctk.CTkLabel(left_frame, text="Image Not Found", font=("Arial", 18, "bold")).pack(expand=True)

    # === Right: Dashboard Buttons ===
    right_frame = ctk.CTkFrame(window, fg_color="#E8EAF6")
    right_frame.pack(side="right", fill="both", expand=True, padx=30, pady=30)

    # Welcome Message
    ctk.CTkLabel(right_frame, text=f"Welcome, {user['username']}!",
                 font=("Arial", 22, "bold"), text_color="#333").pack(pady=20)

    # Buttons
    ctk.CTkButton(right_frame, text="➕ Post New Job", width=250, height=45, font=("Arial", 16, "bold"),
                  fg_color="#4CAF50", text_color="white",
                  command=lambda: (window.destroy(), open_post_job_window(user))).pack(pady=10)

    ctk.CTkButton(right_frame, text="📋 View Posted Jobs", width=250, height=45, font=("Arial", 16, "bold"),
                  fg_color="#2196F3", text_color="white",
                  command=lambda: (window.destroy(), open_view_jobs_window(user))).pack(pady=10)

    # ✅ NEW Button: View Interviews
    ctk.CTkButton(right_frame, text="🗓 View Interviews", width=250, height=45, font=("Arial", 16, "bold"),
                  fg_color="#8E24AA", text_color="white",
                  command=lambda: (window.destroy(), open_view_interviews_window(user))).pack(pady=10)
    
    def logout():
        window.destroy()
        subprocess.Popen([sys.executable, "login.py"])
        

    # Logout
    ctk.CTkButton(right_frame, text="🚪 Logout", width=150, height=40, font=("Arial", 14, "bold"),
                  fg_color="#F44336", text_color="white", command=logout).pack(pady=30)

    window.mainloop()
