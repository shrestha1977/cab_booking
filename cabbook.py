import sqlite3
import streamlit as st
from datetime import datetime
from hashlib import sha256
import pandas as pd

# Initialize the Database
def init_db():
    try:
        conn = sqlite3.connect('cab_booking.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                pickup TEXT,
                dropoff TEXT,
                car_type TEXT,
                payment_type TEXT,
                booking_date TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                rating INTEGER,
                feedback TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                complaint TEXT,
                complaint_date TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                query_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                query TEXT,
                query_date TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS suggestions (
                suggestion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                suggestion TEXT,
                suggestion_date TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        st.error(f"Error initializing database: {e}")

# User Registration Function
def register_user(username, password):
    try:
        conn = sqlite3.connect('cab_booking.db')
        c = conn.cursor()
        hashed_password = sha256(password.encode()).hexdigest()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        st.success("User registered successfully!")
    except sqlite3.Error as e:
        st.error(f"Error during registration: {e}")

# User Login Function
def login_user(username, password):
    try:
        conn = sqlite3.connect('cab_booking.db')
        c = conn.cursor()
        hashed_password = sha256(password.encode()).hexdigest()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        data = c.fetchone()
        return data
    except sqlite3.Error as e:
        st.error(f"Error during login: {e}")
    finally:
        conn.close()

# Book a Ride
def book_ride(username):
    st.subheader("Book a Ride")
    pickup = st.text_input("Pickup Location")
    dropoff = st.text_input("Dropoff Location")
    car_type = st.selectbox("Select Car Type", ["Sedan", "SUV", "Luxury"])
    payment_type = st.selectbox("Payment Type", ["Cash", "Card", "UPI"])

    if st.button("Book Ride"):
        if pickup and dropoff:
            try:
                conn = sqlite3.connect('cab_booking.db')
                c = conn.cursor()
                booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("INSERT INTO bookings (username, pickup, dropoff, car_type, payment_type, booking_date) VALUES (?, ?, ?, ?, ?, ?)",
                          (username, pickup, dropoff, car_type, payment_type, booking_date))
                conn.commit()
                conn.close()
                st.success("Ride booked successfully!")
            except sqlite3.Error as e:
                st.error(f"Error booking ride: {e}")
        else:
            st.error("Please enter both Pickup and Dropoff locations.")

# Lost Item Support
def lost_item_support(username):
    st.subheader("Lost Item Support")
    complaint = st.text_area("Describe the lost item")
    if st.button("Submit"):
        if complaint:
            try:
                conn = sqlite3.connect('cab_booking.db')
                c = conn.cursor()
                complaint_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("INSERT INTO complaints (username, complaint, complaint_date) VALUES (?, ?, ?)",
                          (username, complaint, complaint_date))
                conn.commit()
                conn.close()
                st.success("Lost item report submitted.")
            except sqlite3.Error as e:
                st.error(f"Error reporting lost item: {e}")
        else:
            st.error("Please describe the lost item.")

# Lodge Complaint
def lodge_complaint(username):
    st.subheader("Lodge a Complaint")
    complaint = st.text_area("Enter your complaint")
    if st.button("Submit Complaint"):
        if complaint:
            try:
                conn = sqlite3.connect('cab_booking.db')
                c = conn.cursor()
                complaint_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("INSERT INTO complaints (username, complaint, complaint_date) VALUES (?, ?, ?)",
                          (username, complaint, complaint_date))
                conn.commit()
                conn.close()
                st.success("Complaint lodged successfully.")
            except sqlite3.Error as e:
                st.error(f"Error lodging complaint: {e}")
        else:
            st.error("Please enter a complaint.")

# Feedback and Ratings
def feedback_and_ratings(username):
    st.subheader("Feedback and Ratings")
    rating = st.slider("Rate your experience", 1, 5)
    feedback = st.text_area("Leave your feedback")
    if st.button("Submit Feedback"):
        if feedback:
            try:
                conn = sqlite3.connect('cab_booking.db')
                c = conn.cursor()
                c.execute("INSERT INTO feedback (username, rating, feedback) VALUES (?, ?, ?)",
                          (username, rating, feedback))
                conn.commit()
                conn.close()
                st.success("Feedback submitted successfully.")
            except sqlite3.Error as e:
                st.error(f"Error submitting feedback: {e}")
        else:
            st.error("Please leave your feedback.")

# Ask a Query
def ask_query(username):
    st.subheader("Ask a Query")
    query = st.text_area("Enter your question")
    if st.button("Submit Query"):
        if query:
            try:
                conn = sqlite3.connect('cab_booking.db')
                c = conn.cursor()
                query_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("INSERT INTO queries (username, query, query_date) VALUES (?, ?, ?)",
                          (username, query, query_date))
                conn.commit()
                conn.close()
                st.success("Query submitted successfully!")
            except sqlite3.Error as e:
                st.error(f"Error submitting query: {e}")
        else:
            st.error("Please enter a question.")

# Give Suggestions
def give_suggestions(username):
    st.subheader("Give Suggestions")
    suggestion = st.text_area("Enter your suggestion")
    if st.button("Submit Suggestion"):
        if suggestion:
            try:
                conn = sqlite3.connect('cab_booking.db')
                c = conn.cursor()
                suggestion_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("INSERT INTO suggestions (username, suggestion, suggestion_date) VALUES (?, ?, ?)",
                          (username, suggestion, suggestion_date))
                conn.commit()
                conn.close()
                st.success("Suggestion submitted successfully!")
            except sqlite3.Error as e:
                st.error(f"Error submitting suggestion: {e}")
        else:
            st.error("Please enter a suggestion.")

# Dashboard
def dashboard(username):
    st.sidebar.title("Dashboard")
    options = [
        "Book a Ride", 
        "Lost Item Support", 
        "Lodge Complaint", 
        "Feedback and Ratings", 
        "Ask a Query", 
        "Give Suggestions"
    ]
    choice = st.sidebar.radio("Choose an Option", options)

    if choice == "Book a Ride":
        book_ride(username)
    elif choice == "Lost Item Support":
        lost_item_support(username)
    elif choice == "Lodge Complaint":
        lodge_complaint(username)
    elif choice == "Feedback and Ratings":
        feedback_and_ratings(username)
    elif choice == "Ask a Query":
        ask_query(username)
    elif choice == "Give Suggestions":
        give_suggestions(username)

# Main Application
def main():
    st.title("Online Cab Booking System")
    init_db()

    menu = ["Home", "Login", "Register", "Dashboard"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.write("Welcome to the Online Cab Booking System.")
    elif choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state["username"] = username
                st.session_state["logged_in"] = True
                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")
    elif choice == "Register":
        st.subheader("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            register_user(username, password)
    elif choice == "Dashboard":
        if "logged_in" in st.session_state and st.session_state["logged_in"]:
            dashboard(st.session_state["username"])
        else:
            st.error("Please log in to access the dashboard.")

if __name__ == "__main__":
    main()
