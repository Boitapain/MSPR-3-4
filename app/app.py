import streamlit as st
from app_pages.login import login
from app_pages.create_account import create_account
from app_pages.dashboard import dashboard

def navigate_to_create_account():
    st.session_state["page"] = "create_account"

def main():
    if 'new_user' not in st.session_state:
        st.session_state['new_user'] = False
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    st.set_page_config(
        page_title="Disease Track",
        page_icon="🦠",
        layout="centered",
        initial_sidebar_state="auto",
    )

    if st.session_state['logged_in'] or st.session_state.get("page") == "dashboard":
        dashboard(st.session_state['user'])
        
    elif st.session_state.get("page") == "create_account":
        create_account()
        if st.session_state['new_user']:
            st.session_state['page'] = None
    else:
        login()

if __name__ == "__main__":
    main()