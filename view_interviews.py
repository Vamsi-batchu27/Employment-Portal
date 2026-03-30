import customtkinter as ctk
from tkinter import messagebox
from database import connect_db


def open_view_interviews_window(user):
    window = ctk.CTkToplevel()
    window.title("Scheduled Interviews")
    window.geometry("700x500")
    window.configure(fg_color="#E8EAF6")
    window.resizable(False, False)

    # Header
    ctk.CTkLabel(window, text="🗓 Scheduled Interviews",
                 font=("Arial", 22, "bold"), text_color="#333").pack(pady=15)

    # Scrollable Canvas
    canvas = ctk.CTkCanvas(window, height=380, bg="#E8EAF6", highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(window, orientation="vertical", command=canvas.yview)
    scroll_frame = ctk.CTkFrame(canvas, fg_color="#E8EAF6")
    canvas_frame = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    def load_interviews():
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT i.*, u.name AS candidate_name, j.job_title
            FROM interviews i
            JOIN users u ON i.user_id = u.user_id
            JOIN jobs j ON i.job_id = j.job_id
            WHERE i.employer_id = %s
            ORDER BY i.interview_date, i.interview_time
        """
        cursor.execute(query, (user["user_id"],))
        interviews = cursor.fetchall()
        db.close()

        if not interviews:
            ctk.CTkLabel(scroll_frame, text="No interviews scheduled yet.",
                         font=("Arial", 14), text_color="#555").pack(pady=30)
            return

        for interview in interviews:
            card = ctk.CTkFrame(scroll_frame, fg_color="white", corner_radius=10)
            card.pack(fill="x", padx=15, pady=10)

            # Info
            ctk.CTkLabel(card, text=f"{interview['candidate_name']} — {interview['job_title']}",
                         font=("Arial", 15, "bold"), text_color="#333").pack(anchor="w", padx=15, pady=(10, 2))

            info = [
                f"Date: {interview['interview_date']}",
                f"Time: {interview['interview_time']}",
                f"Mode: {interview['mode']}",
                f"Status: {interview['status']}"
            ]

            for line in info:
                ctk.CTkLabel(card, text=line, font=("Arial", 12), text_color="#555").pack(anchor="w", padx=15)

            # Cancel button
            if interview['status'] == "Scheduled":
                def cancel_interview(int_id=interview['interview_id']):
                    confirm = messagebox.askyesno("Confirm Cancel", "Are you sure you want to cancel this interview?")
                    if confirm:
                        db2 = connect_db()
                        cur2 = db2.cursor()
                        cur2.execute("UPDATE interviews SET status = 'Cancelled' WHERE interview_id = %s", (int_id,))
                        db2.commit()
                        db2.close()
                        messagebox.showinfo("Cancelled", "Interview marked as cancelled.")
                        window.destroy()
                        open_view_interviews_window(user)

                ctk.CTkButton(card, text="Cancel Interview", width=160, height=35,
                              font=("Arial", 12, "bold"), fg_color="#F44336", text_color="white",
                              command=cancel_interview).pack(anchor="e", padx=15, pady=10)

    load_interviews()

    # Scroll config
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=(0, 10))
    scrollbar.pack(side="right", fill="y")
    
    def go_back():
        from employer_dashboard import employer_dashboard  # ✅ moved inside function
        window.destroy()
        employer_dashboard(user)
        
    ctk.CTkButton(window, text="🔙 Back", command=go_back).pack(pady=10)