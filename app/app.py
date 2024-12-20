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

    if st.session_state['user']:
        dashboard(st.session_state['user'])
    elif st.session_state.get("page") == "create_account":
        create_account()
        if st.session_state['new_user']:
            st.session_state['page'] = None
    else:
        login()
        st.button("Create Account", on_click=navigate_to_create_account)

if __name__ == "__main__":
    main()