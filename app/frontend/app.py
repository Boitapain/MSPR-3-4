import streamlit as st
from login import login
from create_account import create_account
from dashboard import dashboard

def navigate_to_create_account():
    st.session_state["page"] = "create_account"

def main():
    # Initialize session state variables if they don't exist
    if 'new_user' not in st.session_state:
        st.session_state['new_user'] = False
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Set the page configuration
    st.set_page_config(
        page_title="Disease Track",
        page_icon="🦠",
        layout="centered",
        initial_sidebar_state="auto",
    )

    # Navigate to the appropriate page based on session state
    if st.session_state['logged_in'] or st.session_state.get("page") == "dashboard":
        # If the user is logged in or the page is set to "dashboard", show the dashboard
        dashboard(st.session_state['user'])
    elif st.session_state.get("page") == "create_account":
        # If the page is set to "create_account", show the create account page
        create_account()
        if st.session_state['new_user']:
            # Reset the page state after account creation
            st.session_state['page'] = None
    else:
        # Otherwise, show the login page
        login()

if __name__ == "__main__":
    main()