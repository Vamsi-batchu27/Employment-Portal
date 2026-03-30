import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
from database import connect_db  # Ensure 'database.py' exists and handles DB connections

# Initialize registration window
root = ctk.CTk()
root.title("Job Management System - Register")
root.geometry("800x600")  # Wider for dual-frame layout
root.resizable(False, False)
root.configure(fg_color="#4B89DC")

# === Function to register a user ===
def register_user():
    name = reg_name_entry.get().strip()
    email = reg_email_entry.get().strip()
    username = reg_username_entry.get().strip()
    experience = reg_experience_entry.get().strip()
    password = reg_password_entry.get().strip()
    confirm_password = reg_confirm_password_entry.get().strip()
    role = "job_seeker"

    if not name or not email or not username or not experience or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required")
        return

    if not experience.isdigit() or int(experience) < 0:
        messagebox.showerror("Error", "Experience must be a valid number (0 or more)")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Username already exists")
        db.close()
        return

    cursor.execute(
        "INSERT INTO users (name, email, username, experience, password, role) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, email, username, experience, password, role)
    )
    db.commit()
    db.close()

    messagebox.showinfo("Success", "Registration Successful!")
    root.destroy()
    subprocess.Popen(["python", "login.py"])

# === Function to return to login ===
def back_to_login():
    root.destroy()
    subprocess.Popen(["python", "login.py"])

# === Left Frame: Registration Form ===
left_frame = ctk.CTkFrame(root, width=400, fg_color="#F4F4F4", corner_radius=0)
left_frame.pack(side="left", fill="both")

# Main container inside left frame
main_frame = ctk.CTkFrame(left_frame, fg_color="#FFFFFF", width=400, height=700)
main_frame.pack_propagate(False)
main_frame.pack(fill="both", expand=True)

# Registration form
reg_form_frame = ctk.CTkFrame(main_frame, fg_color="#E8EAF6", width=300, height=550)
reg_form_frame.pack_propagate(False)
reg_form_frame.place(x=50, y=20)

# Fields
def add_field(label, entry_var, y_offset, is_password=False):
    ctk.CTkLabel(reg_form_frame, text=label, text_color="#4B89DC", font=("Arial", 14)).place(x=40, y=y_offset)
    return ctk.CTkEntry(reg_form_frame, width=220, height=35, fg_color="#FFFFFF", show="*" if is_password else "").place(x=40, y=y_offset + 30)

reg_name_label = ctk.CTkLabel(reg_form_frame, text="Full Name", text_color="#4B89DC", font=("Arial", 14))
reg_name_label.place(x=40, y=20)
reg_name_entry = ctk.CTkEntry(reg_form_frame, width=220, height=35, fg_color="#FFFFFF")
reg_name_entry.place(x=40, y=50)

reg_email_label = ctk.CTkLabel(reg_form_frame, text="Email", text_color="#4B89DC", font=("Arial", 14))
reg_email_label.place(x=40, y=90)
reg_email_entry = ctk.CTkEntry(reg_form_frame, width=220, height=35, fg_color="#FFFFFF")
reg_email_entry.place(x=40, y=120)

reg_username_label = ctk.CTkLabel(reg_form_frame, text="Username", text_color="#4B89DC", font=("Arial", 14))
reg_username_label.place(x=40, y=160)
reg_username_entry = ctk.CTkEntry(reg_form_frame, width=220, height=35, fg_color="#FFFFFF")
reg_username_entry.place(x=40, y=190)

reg_experience_label = ctk.CTkLabel(reg_form_frame, text="Experience (Years)", text_color="#4B89DC", font=("Arial", 14))
reg_experience_label.place(x=40, y=230)
reg_experience_entry = ctk.CTkEntry(reg_form_frame, width=220, height=35, fg_color="#FFFFFF")
reg_experience_entry.place(x=40, y=260)

reg_password_label = ctk.CTkLabel(reg_form_frame, text="Password", text_color="#4B89DC", font=("Arial", 14))
reg_password_label.place(x=40, y=300)
reg_password_entry = ctk.CTkEntry(reg_form_frame, width=220, height=35, show="*", fg_color="#FFFFFF")
reg_password_entry.place(x=40, y=330)

reg_confirm_password_label = ctk.CTkLabel(reg_form_frame, text="Confirm Password", text_color="#4B89DC", font=("Arial", 14))
reg_confirm_password_label.place(x=40, y=370)
reg_confirm_password_entry = ctk.CTkEntry(reg_form_frame, width=220, height=35, show="*", fg_color="#FFFFFF")
reg_confirm_password_entry.place(x=40, y=400)

# Buttons
register_button = ctk.CTkButton(reg_form_frame, text="Register", fg_color="#4B89DC", text_color="#FFFFFF", width=220, height=35, command=register_user)
register_button.place(x=40, y=450)

back_button = ctk.CTkButton(reg_form_frame, text="Back to Login", fg_color="#F6CA51", text_color="#333", width=220, height=35, command=back_to_login)
back_button.place(x=40, y=500)

# Footer
footer_label = ctk.CTkLabel(main_frame, text="© 2024 Job Management System", text_color="#6C7071", font=("Arial", 9))
footer_label.place(x=100, y=670)

# === Right Frame: Image ===
right_frame = ctk.CTkFrame(root, width=400, fg_color="white", corner_radius=0)
right_frame.pack(side="left", fill="both")

try:
    image = Image.open("images/signup.png")  # Replace with your image
    image = image.resize((500, 700), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label = ctk.CTkLabel(right_frame, image=photo, text="")
    image_label.pack(fill="both", expand=True)
except Exception as e:
    ctk.CTkLabel(right_frame, text="Image\nNot Found", font=("Arial", 20, "bold")).pack(expand=True)

# === Start the app ===
root.mainloop()
