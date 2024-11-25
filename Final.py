import streamlit as st
import sqlite3
from hashlib import sha256
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed_password = sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed_password = sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user

# --- Resume Builder ---
questions = [
    "What is your full name?",
    "What is your email address?",
    "What is your phone number?",
    "What is your current job title?",
    "What is your work experience?",
    "What are your key skills?",
    "What is your education background?",
    "What are your certifications and awards?",
    "What is your desired job position?",
    "What are your hobbies and interests?",
    "Do you have any references? If so, please provide their contact information."
]

def generate_pdf(responses):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50
    line_spacing = 20

    # Helper function for multi-line text
    def draw_multiline_text(c, x, y, text, max_width=400):
        from reportlab.lib.utils import simpleSplit
        lines = simpleSplit(text, "Helvetica", 12, max_width)
        for line in lines:
            c.drawString(x, y, line)
            y -= line_spacing
        return y

    c.drawString(100, y, f"Name: {responses[0]}")
    y -= line_spacing
    c.drawString(100, y, f"Email: {responses[1]}")
    y -= line_spacing
    c.drawString(100, y, f"Phone: {responses[2]}")
    y -= line_spacing
    c.drawString(100, y, f"Job Title: {responses[3]}")
    y -= line_spacing * 2

    y = draw_multiline_text(c, 100, y, f"Work Experience:\n{responses[4]}")
    y = draw_multiline_text(c, 100, y, f"Key Skills:\n{responses[5]}")
    y = draw_multiline_text(c, 100, y, f"Education:\n{responses[6]}")
    y = draw_multiline_text(c, 100, y, f"Certifications:\n{responses[7]}")
    y = draw_multiline_text(c, 100, y, f"Desired Position:\n{responses[8]}")
    y = draw_multiline_text(c, 100, y, f"Hobbies and Interests:\n{responses[9]}")
    y = draw_multiline_text(c, 100, y, f"References:\n{responses[10]}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def resume_builder():
    st.subheader("Resume Builder")
    with st.form("resume-form"):
        responses = []
        for q in questions:
            if "experience" in q.lower() or "skills" in q.lower() or "hobbies" in q.lower():
                response = st.text_area(q)
            else:
                response = st.text_input(q)
            responses.append(response)
        submitted = st.form_submit_button("Generate Resume")

    if submitted:
        if all(responses):
            st.write("Generating your resume... Please wait.")
            resume_buffer = generate_pdf(responses)
            st.success("Resume successfully generated!")
            st.download_button(label="Download Generated Resume", data=resume_buffer, file_name="generated_resume.pdf")
        else:
            st.error("Please fill out all fields before submitting.")

# --- Main Function ---
def main():
    st.title("User Authentication and Resume Builder")

    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if st.session_state.logged_in:
        st.success(f"Welcome, {st.session_state.username}!")
        resume_builder()
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.info("You have logged out.")
    else:
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            st.subheader("Login")
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login"):
                if verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome, {username}!")
                else:
                    st.error("Invalid username or password.")

        elif choice == "Register":
            st.subheader("Register")
            
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.button("Register"):
                if new_password == confirm_password:
                    try:
                        add_user(new_username, new_password)
                        st.success("User registered successfully! You can now log in.")
                    except sqlite3.IntegrityError:
                        st.error("Username already exists. Please choose a different username.")
                else:
                    st.error("Passwords do not match.")

if __name__ == "__main__":
    init_db()
    main()
