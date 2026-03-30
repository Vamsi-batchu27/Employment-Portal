import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import subprocess
import os

from admin_dashboard import admin_dashboard
from database import connect_db
from job_seeker import job_seeker_dashboard
from employer_dashboard import employer_dashboard

# === Setup for resolving image path ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize login window
root = ctk.CTk()
root.title("Job Management System - Login")
root.geometry("900x600")
root.resizable(False, False)
root.configure(fg_color="#ECEFFC")  # Background color like in image

# ==== Top Title Label on Root Frame ====
title_label = ctk.CTkLabel(root, text="Job Management System", text_color="#4B89DC", font=("Arial", 26, "bold"))
title_label.place(relx=0.5, y=60, anchor="center")  # Top-center

# ==== Function to authenticate user ====
def authenticate_user():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    db.close()

    if user:
        messagebox.showinfo("Success", f"Welcome {user['username']}!")
        root.withdraw()
        if user["role"] == "job_seeker":
            job_seeker_dashboard(user)
        elif user["role"] == "employer":
            employer_dashboard(user)
        elif user["role"] == "admin":
            admin_dashboard(user)
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

# ==== Function to open the registration page ====
def open_registration():
    root.destroy()
    subprocess.Popen(["python", "registration_page.py"])

# ==== Left Frame (Image Section) ====
left_frame = ctk.CTkFrame(root, width=450, height=500, fg_color="#ECEFFC", corner_radius=0)
left_frame.place(x=0, y=80)

try:
    image_path = os.path.join(SCRIPT_DIR, "images", "login.png")
    img = Image.open(image_path)
    img = img.resize((450, 500), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    image_label = ctk.CTkLabel(left_frame, image=photo, text="")
    image_label.image = photo  # Prevent garbage collection
    image_label.pack(fill="both", expand=True)
except Exception as e:
    ctk.CTkLabel(left_frame, text="Image\nNot Found", font=("Arial", 20, "bold")).pack(expand=True)

# ==== Right Frame (Login Section) ====
right_frame = ctk.CTkFrame(root, width=450, height=500, fg_color="#ECEFFC", corner_radius=0)
right_frame.place(x=450, y=80)

# ==== Login Card ====
login_form_frame = ctk.CTkFrame(right_frame, fg_color="white", width=350, height=400, corner_radius=10)
login_form_frame.place(relx=0.5, rely=0.5, anchor="center")

login_label = ctk.CTkLabel(login_form_frame, text="Login", text_color="black", font=("Arial", 22, "bold"))
login_label.place(x=140, y=20)

login_username_label = ctk.CTkLabel(login_form_frame, text="UserName", text_color="#4B89DC", font=("Arial", 14))
login_username_label.place(x=40, y=70)
login_username_entry = ctk.CTkEntry(login_form_frame, width=260, height=35, fg_color="#FFFFFF")
login_username_entry.place(x=40, y=100)

login_password_label = ctk.CTkLabel(login_form_frame, text="Password", text_color="#4B89DC", font=("Arial", 14))
login_password_label.place(x=40, y=150)
login_password_entry = ctk.CTkEntry(login_form_frame, width=260, height=35, show="*", fg_color="#FFFFFF")
login_password_entry.place(x=40, y=180)

# ==== Show/Hide Password Toggle ====
def toggle_password():
    if show_password_var.get():
        login_password_entry.configure(show="")
    else:
        login_password_entry.configure(show="*")

show_password_var = tk.IntVar()
show_password_checkbox = ctk.CTkCheckBox(
    login_form_frame, text="Show Password", variable=show_password_var,
    command=toggle_password, text_color="black"
)
show_password_checkbox.place(x=40, y=225)

# ==== Login Button ====
login_button = ctk.CTkButton(
    login_form_frame, text="Login", fg_color="#4B89DC", text_color="white",
    width=260, height=35, command=authenticate_user
)
login_button.place(x=40, y=270)

# ==== Sign-Up Option ====
register_label = ctk.CTkLabel(login_form_frame, text="Don’t have an account", text_color="black", font=("Arial", 12))
register_label.place(x=40, y=320)

register_button = ctk.CTkButton(
    login_form_frame, text="SignUp", fg_color="#7EA6F2", text_color="white",
    width=90, height=30, command=open_registration
)
register_button.place(x=200, y=316)

# ==== Run the application ====
root.mainloop()
