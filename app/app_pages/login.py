import streamlit as st
from api.db import get_user

def login():
    # Display the title and subtitle
    st.markdown("<h1 style='text-align: center;'>Disease track 🦠</h1>", unsafe_allow_html=True)
    st.subheader("Login")
    
    # Input fields for email and password
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    # Create columns for buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Login button
        if st.button("Login", key="login_button", type="primary", icon=":material/login:"):
            user = get_user(email)
            if user:
                # Store user data in session state and navigate to dashboard
                st.session_state['user'] = user
                st.session_state['page'] = 'dashboard'
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                # Show error message if login fails
                st.error("Invalid email or password")
    
    with col2:
        # Create Account button
        st.button("Create Account", type="primary", icon=":material/person_add:", on_click=lambda: st.session_state.update({"page": "create_account"}), key="create_account_button")

if __name__ == "__main__":
    login()