import streamlit as st

def settings(user):
    st.markdown("<h1 style='text-align: center;'>CSV Import</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>Settings for {user[1]}</h3>", unsafe_allow_html=True)
    # Add settings options here
