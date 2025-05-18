import streamlit as st
import requests

def create_account():
    st.markdown("<h1 style='text-align: center;'>Disease track 🦠</h1>", unsafe_allow_html=True)
    st.subheader("Create Account")
    
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("Cancel", icon=":material/close:", on_click=lambda: st.session_state.update({"page": "login"})):
            st.session_state['page'] = 'login'
            st.rerun()
    
    with col2:
        if st.button("Register", type="primary", icon=":material/assignment_turned_in:"):
            if name == "" or email == "" or password == "" or confirm_password == "":
                st.error("All fields are required")
            else:
                if password == confirm_password:
                    response = requests.post("http://api:5000/register", json={
                        "name": name,
                        "email": email,
                        "password": password
                    })
                    if response.status_code == 201:
                        st.success("Account created successfully!")
                        st.session_state['new_user'] = True
                        st.session_state['page'] = 'login'
                        st.rerun()
                    else:
                        st.error("Failed to create account: " + response.json().get("message", "Unknown error"))
                else:
                    st.error("Passwords do not match")