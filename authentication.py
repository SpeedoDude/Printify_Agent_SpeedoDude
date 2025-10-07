
import streamlit as st
from user_database import UserDB

def login_page():
    st.title("Login")
    
    db = UserDB()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if db.authenticate_user(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success("Logged in successfully.")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

def signup_page():
    st.title("Sign Up")

    db = UserDB()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])

    if st.button("Sign Up"):
        success, message = db.add_user(username, password, role)
        if success:
            st.success(message)
        else:
            st.error(message)
