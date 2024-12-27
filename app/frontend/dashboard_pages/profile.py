import streamlit as st

def profile(user):
    st.markdown("<h1 style='text-align: center;'>Profile</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>User Profile: {user['name']}</h3>", unsafe_allow_html=True)
    # Add more profile details here
