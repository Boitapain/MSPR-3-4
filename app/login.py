import streamlit as st
from db import authenticate_user

def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Connect"):
        user = authenticate_user(email, password)
        if user:
            st.success("Logged in successfully!")
            st.session_state['user'] = user
            st.rerun()
        else:
            st.error("Invalid email or password")

if __name__ == "__main__":
    login()