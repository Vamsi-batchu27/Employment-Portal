import customtkinter as ctk
from tkinter import messagebox
from database import connect_db

def open_post_job_window(user):
    window = ctk.CTkToplevel()
    window.title("Post New Job")
    window.geometry("500x600")
    window.configure(fg_color="#E8EAF6")

    ctk.CTkLabel(window, text="Post a New Job", font=("Arial", 22, "bold"), text_color="#333").pack(pady=20)

    title_entry = ctk.CTkEntry(window, placeholder_text="Job Title", width=350)
    title_entry.pack(pady=10)

    # Simulated placeholder for CTkTextbox
    desc_entry = ctk.CTkTextbox(window, height=100, width=350)
    desc_entry.insert("0.0", "Job Description...")
    desc_entry.configure(text_color="gray")
    desc_entry.pack(pady=10)

    def clear_placeholder(event):
        if desc_entry.get("1.0", "end-1c") == "Job Description...":
            desc_entry.delete("1.0", "end")
            desc_entry.configure(text_color="black")

    def restore_placeholder(event):
        if desc_entry.get("1.0", "end-1c").strip() == "":
            desc_entry.insert("0.0", "Job Description...")
            desc_entry.configure(text_color="gray")

    desc_entry.bind("<FocusIn>", clear_placeholder)
    desc_entry.bind("<FocusOut>", restore_placeholder)

    skills_entry = ctk.CTkEntry(window, placeholder_text="Required Skills (comma-separated)", width=350)
    skills_entry.pack(pady=10)

    exp_entry = ctk.CTkEntry(window, placeholder_text="Experience Required (in years)", width=350)
    exp_entry.pack(pady=10)

    def post_job():
        from employer_dashboard import employer_dashboard

        title = title_entry.get().strip()
        desc = desc_entry.get("1.0", "end").strip()
        skills = skills_entry.get().strip()

        try:
            exp = int(exp_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Experience must be a number.")
            return

        if not title or not desc or desc == "Job Description..." or not skills:
            messagebox.showerror("Error", "All fields are required.")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO jobs (employer_id, job_title, job_description, required_skills, experience_required) "
            "VALUES (%s, %s, %s, %s, %s)",
            (user['user_id'], title, desc, skills, exp)
        )
        db.commit()
        db.close()

        messagebox.showinfo("Success", "Job posted successfully!")
        window.destroy()
        employer_dashboard(user)

    ctk.CTkButton(window, text="✅ Post Job", width=200, height=40, fg_color="#4CAF50", text_color="white",
                  font=("Arial", 14, "bold"), command=post_job).pack(pady=20)

    ctk.CTkButton(window, text="🔙 Back", width=150, height=35, fg_color="#FFA500", text_color="white",
                  command=lambda: (window.destroy(), __import__("employer_dashboard").employer_dashboard(user))).pack()
