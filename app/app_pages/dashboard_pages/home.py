import streamlit as st

def home(user):
    st.markdown(f"<h3 style='text-align: center;'>Welcome back, {user['name']}! 👋</h3>", unsafe_allow_html=True)
    # Add more dashboard content here

if __name__ == "__main__":
    home({"name": "Test User"})