import streamlit as st
from api.db import add_user

def create_account():
    st.title("Create Account")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if password == confirm_password:
            add_user(name, email, password)
            st.success("Account created successfully!")
            st.session_state['new_user'] = True
            st.session_state['page'] = 'login'
            st.rerun()
        else:
            st.error("Passwords do not match")

if __name__ == "__main__":
    create_account()