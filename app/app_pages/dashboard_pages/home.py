import streamlit as st

def home(user):
    st.markdown("<h1 style='text-align: center;'>Home</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>Welcome back, {user[1]}! 👋</h3>", unsafe_allow_html=True)
