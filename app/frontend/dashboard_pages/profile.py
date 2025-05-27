import streamlit as st
import requests

def profile(user):
    st.markdown("<h1 style='text-align: center;'>Your profile</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:1.5rem;'>User: <b>{user['name']}</b></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:1.5rem;'>Email: <span>{user['email']}</span></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:1.5rem;'>Is Admin: <b>{True if user['isAdmin'] == 1 else False}</b></h3>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Update your password")

    with st.form("update_password_form"):
        old_password = st.text_input("Your password", type="password")
        new_password = st.text_input("New password", type="password")
        confirm_password = st.text_input("Confirm password", type="password")
        submitted = st.form_submit_button("Update Password", use_container_width=True)
        if submitted:
            if not old_password or not new_password or not confirm_password:
                st.error("All fields are required.")
            elif new_password != confirm_password:
                st.error("New password and confirm password do not match.")
            else:
                response = requests.post(
                    "http://api:5000/update_password",
                    json={
                        "email": user["email"],
                        "old_password": old_password,
                        "new_password": new_password,
                        "confirm_password": confirm_password
                    }
                )
                if response.status_code == 200:
                    st.success("Password updated successfully!")
                else:
                    st.error(response.json().get("message", "Failed to update password."))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Logout", icon=":material/logout:"):
            st.session_state['page'] = 'login'
            st.session_state['logged_in'] = False
            st.session_state['user'] = None
            st.rerun()