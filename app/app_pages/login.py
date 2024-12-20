import streamlit as st
from api.db import get_user

def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = get_user(email)
        if user:
            st.session_state['user'] = user
            st.session_state['page'] = 'dashboard'
        else:
            st.error("Invalid email or password")

if __name__ == "__main__":
    login()