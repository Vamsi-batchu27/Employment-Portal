import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess

# Main Window Setup
root = ctk.CTk()
root.title("Job Matching System")
root.geometry("700x400")
root.resizable(False, False)
root.configure(fg_color="#4B89DC")

# ===== Left Frame: Image =====
left_frame = ctk.CTkFrame(root, width=500, corner_radius=0)
left_frame.pack(side="left", fill="both", expand=False)

try:
    img = Image.open("images/home.png").resize((500, 400), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    image_label = ctk.CTkLabel(left_frame, image=photo, text="")
    image_label.pack(fill="both", expand=True)
except Exception as e:
    ctk.CTkLabel(left_frame, text="Image\nNot Found", font=("Arial", 20, "bold")).pack(expand=True)

# ===== Right Frame: Title + Button =====
right_frame = ctk.CTkFrame(root, fg_color="white", corner_radius=0)
right_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

# System Name & Subtitle
ctk.CTkLabel(right_frame, text="Job Matching System", text_color="black", font=("Arial", 22, "bold")).pack(pady=(100, 5))
ctk.CTkLabel(right_frame, text="Find the right job or the right hire", text_color="gray", font=("Arial", 14)).pack(pady=(0, 40))

# Login Button
def open_login():
    root.destroy()
    subprocess.Popen(["python", "login.py"])

ctk.CTkButton(right_frame, text="Login", width=200, height=40, fg_color="black", text_color="white",
              font=("Arial", 14, "bold"), command=open_login).pack(pady=(100, 0))

root.mainloop()
