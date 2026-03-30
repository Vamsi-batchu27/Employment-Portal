import customtkinter as ctk
from tkinter import messagebox
from database import connect_db


def open_manage_employees_window(user):
    window = ctk.CTkToplevel()
    window.title("Manage Employers")
    window.geometry("900x550")
    window.configure(fg_color="#E8EAF6")
    window.resizable(False, False)

    # === Sidebar Navigation ===
    sidebar = ctk.CTkFrame(window, width=180, fg_color="#4B89DC")
    sidebar.pack(side="left", fill="y")

    ctk.CTkLabel(sidebar, text="Admin Panel", text_color="white",
                 font=("Arial", 18, "bold")).pack(pady=(20, 10))

    # Nav Buttons
    ctk.CTkButton(sidebar, text="📄 View Employers", width=140, fg_color="#5C6BC0",
                  text_color="white", command=lambda: load_employers()).pack(pady=10)

    ctk.CTkButton(sidebar, text="➕ Add Employer", width=140, fg_color="#4CAF50",
                  text_color="black", command=lambda: show_employer_form()).pack(pady=10)

    def go_back():
        from admin_dashboard import admin_dashboard
        window.destroy()
        admin_dashboard(user)

    ctk.CTkButton(sidebar, text="🔙 Back", width=140, fg_color="#FF9800",
                  text_color="black", command=go_back).pack(pady=10)

    # === Main Area ===
    main_frame = ctk.CTkFrame(window, fg_color="#E8EAF6")
    main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # This will be dynamically updated
    content_frame = ctk.CTkFrame(main_frame, fg_color="#E8EAF6")
    content_frame.pack(fill="both", expand=True)

    def clear_main():
        for widget in content_frame.winfo_children():
            widget.destroy()

    # === Show Form ===
    def show_employer_form(emp=None):
        clear_main()
        is_edit = emp is not None

        ctk.CTkLabel(content_frame, text="✏️ Edit Employer" if is_edit else "➕ Add Employer",
                     font=("Arial", 20, "bold"), text_color="#333").pack(pady=10)

        def labeled_entry(label, initial=""):
            ctk.CTkLabel(content_frame, text=label, font=("Arial", 12), text_color="#222").pack(pady=(10, 0))
            entry = ctk.CTkEntry(content_frame, width=280)
            entry.insert(0, initial)
            entry.pack()
            return entry

        name_entry = labeled_entry("Full Name", emp['name'] if is_edit else "")
        email_entry = labeled_entry("Email", emp['email'] if is_edit else "")
        username_entry = labeled_entry("Username", emp['username'] if is_edit else "")
        experience_entry = labeled_entry("Experience (years)", str(emp['experience']) if is_edit else "")
        password_entry = labeled_entry("Password")

        def save_employer():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            username = username_entry.get().strip()
            experience = experience_entry.get().strip()
            password = password_entry.get().strip()

            if not all([name, email, username, experience]):
                messagebox.showerror("Missing Fields", "Please complete all required fields.")
                return

            try:
                db = connect_db()
                cursor = db.cursor()

                if is_edit:
                    if password:
                        cursor.execute("""
                            UPDATE users SET name=%s, email=%s, username=%s, experience=%s, password=%s
                            WHERE user_id=%s
                        """, (name, email, username, experience, password, emp['user_id']))
                    else:
                        cursor.execute("""
                            UPDATE users SET name=%s, email=%s, username=%s, experience=%s
                            WHERE user_id=%s
                        """, (name, email, username, experience, emp['user_id']))
                else:
                    cursor.execute("""
                        INSERT INTO users (name, email, username, experience, password, role)
                        VALUES (%s, %s, %s, %s, %s, 'employer')
                    """, (name, email, username, experience, password))

                db.commit()
                db.close()
                messagebox.showinfo("Success", "Employer saved successfully.")
                load_employers()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(content_frame, text="✅ Save", fg_color="#4CAF50", text_color="white",
                      width=120, height=40, command=save_employer).pack(pady=20)

    # === Load Employer List ===
    def load_employers():
        clear_main()

        ctk.CTkLabel(content_frame, text="👥 Employers", font=("Arial", 20, "bold"),
                     text_color="#333").pack(pady=10)

        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE role = 'employer'")
        employers = cursor.fetchall()
        db.close()

        if not employers:
            ctk.CTkLabel(content_frame, text="No employers found.", font=("Arial", 14),
                         text_color="#666").pack(pady=30)
            return

        for emp in employers:
            card = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=10)
            card.pack(fill="x", padx=20, pady=10)

            ctk.CTkLabel(card, text=f"{emp['name']} | {emp['email']}",
                         font=("Arial", 14, "bold"), text_color="#222").pack(anchor="w", padx=15, pady=(10, 0))
            ctk.CTkLabel(card, text=f"Username: {emp['username']} | Experience: {emp['experience']} years",
                         font=("Arial", 12), text_color="#555").pack(anchor="w", padx=15, pady=(0, 10))

            # Edit Button Only
            btns = ctk.CTkFrame(card, fg_color="transparent")
            btns.pack(anchor="e", padx=15, pady=(0, 10))

            ctk.CTkButton(btns, text="✏️ Edit", width=100, height=35,
                          fg_color="#3F51B5", text_color="white",
                          command=lambda e=emp: show_employer_form(e)).pack(side="left", padx=5)

    load_employers()
