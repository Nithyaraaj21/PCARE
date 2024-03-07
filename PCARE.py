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
    return False, None

# Function to handle property rental and maintenance selection
def handle_rental_maintenance_selection():
    st.title("Choose Option")
    option = st.radio("Choose an option:", ("Rental + Maintenance", "Maintenance Only"))
    if option == "Rental + Maintenance":
        st.write("You chose Rental + Maintenance")
        handle_property_details()
    elif option == "Maintenance Only":
        st.write("You chose Maintenance Only")
        handle_property_details()

# Function to handle input of property details
def handle_property_details():
    st.title("Property Details")
    st.subheader("Address Details")
    country = st.text_input("Country")
    state = st.text_input("State")
    city = st.text_input("City")
    town = st.text_input("Town")
    address = st.text_area("Address")

    st.subheader("Property Description")
    square_meter = st.number_input("Total Square Meter", min_value=0)
    num_bedrooms = st.number_input("Number of Bedrooms", min_value=0)
    equipped = st.checkbox("Equipped")
    exceptional_property = st.checkbox("Exceptional Property")
    has_swimming_pool = st.checkbox("Has Swimming Pool")
    has_party_hall = st.checkbox("Has Party Hall")

    st.write("You entered the following property details:")
    st.write(f"Country: {country}")
    st.write(f"State: {state}")
    st.write(f"City: {city}")
    st.write(f"Town: {town}")
    st.write(f"Address: {address}")
    st.write(f"Total Square Meter: {square_meter}")
    st.write(f"Number of Bedrooms: {num_bedrooms}")
    st.write(f"Equipped: {equipped}")
    st.write(f"Exceptional Property: {exceptional_property}")
    st.write(f"Has Swimming Pool: {has_swimming_pool}")
    st.write(f"Has Party Hall: {has_party_hall}")

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
        login_successful, username = login()
        if login_successful:
            st.success("Login successful!")
            session_state.registered = False
            handle_rental_maintenance_selection()

def save_property_details(property_details):
    with open('property_details.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(property_details)

# Function to handle input of property details
def handle_property_details():
    st.title("Property Details")
    st.subheader("Address Details")
    country = st.text_input("Country")
    state = st.text_input("State")
    city = st.text_input("City")
    town = st.text_input("Town")
    address = st.text_area("Address")

    st.subheader("Property Description")
    square_meter = st.number_input("Total Square Meter", min_value=0)
    num_bedrooms = st.number_input("Number of Bedrooms", min_value=0)
    equipped = st.checkbox("Equipped")
    exceptional_property = st.checkbox("Exceptional Property")
    has_swimming_pool = st.checkbox("Has Swimming Pool")
    has_party_hall = st.checkbox("Has Party Hall")

    if st.button("Save Property Details"):
        property_details = [country, state, city, town, address, square_meter, num_bedrooms, equipped, exceptional_property, has_swimming_pool, has_party_hall]
        save_property_details(property_details)
        st.success("Property details saved successfully!")

# Main function to run the Streamlit application
def main():
    handle_property_details()

if __name__ == "__main__":
    main()
