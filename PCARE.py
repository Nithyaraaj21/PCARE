import streamlit as st
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to load user credentials from CSV file
def load_user_credentials():
    user_credentials = {}
    if os.path.exists('user_credentials.csv'):
        with open('user_credentials.csv', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_credentials[row['username']] = {'password': row['password'], 'email': row['email']}
    return user_credentials

# Function to save user credentials to CSV file
def save_user_credentials(user_credentials):
    with open('user_credentials.csv', 'w', newline='') as file:
        fieldnames = ['username', 'password', 'email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for username, data in user_credentials.items():
            writer.writerow({'username': username, 'password': data['password'], 'email': data['email']})

# Function to send registration confirmation email
def send_registration_email(username, email):
    subject = "Registration Confirmation"
    body = f"Dear {username},\n\nThank you for registering with Pcare. Your account has been successfully created. Please login using the provided link."
    sender_email = "nithyaraaj@outlook.com"
    sender_password = "Rithanya031021"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    # Send email using SMTP
    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())

# Function for user registration
def registration():
    st.title("Registration")
    new_username = st.text_input("Choose a Username")
    new_email = st.text_input("Enter your Email Address")
    new_password = st.text_input("Choose a Password", type='password')
    if st.button("Register"):
        user_credentials = load_user_credentials()
        if new_username in user_credentials:
            st.error("Username already exists! Please choose another one.")
        else:
            user_credentials[new_username] = {'password': new_password, 'email': new_email}
            save_user_credentials(user_credentials)
            st.success("Registration successful! You can now login.")
            send_registration_email(new_username, new_email)
            return True, new_username
    return False, None

# Function for user login
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        user_credentials = load_user_credentials()
        if username in user_credentials and password == user_credentials[username]['password']:
            st.success("Logged in as {}".format(username))
            return True, username
        else:
            st.error("Invalid username or password")
            return False, None

# Main function to run the Streamlit application
def main():
    session_state = st.session_state
    if 'registered' not in session_state:
        session_state.registered = False
        session_state.username = None

    if not session_state.registered:
        session_state.registered, session_state.username = registration()

    if session_state.registered:
        st.write("Please login with your new credentials.")
        login_successful, _ = login()
        if login_successful:
            st.success("Login successful!")
            session_state.registered = False

if __name__ == "__main__":
    main()
