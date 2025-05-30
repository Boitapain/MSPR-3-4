import streamlit as st
import requests
from translations import load_translations

def profile(user):
    lang = st.session_state['language']
    translations = load_translations(lang)
    t = translations['profile']
    
    st.markdown(f"<h1 style='text-align: center;'>{t['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:1.5rem;'>{t['user_info']['user']} <b>{user['name']}</b></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:1.5rem;'>{t['user_info']['email']} <span>{user['email']}</span></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:1.5rem;'>{t['user_info']['country']} <span>{user['country']}</span></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:1.5rem;'>{t['user_info']['isAdmin']} <b>{True if user['isAdmin'] == 1 else False}</b></h3>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader(t['password_section']['title'])

    with st.form("update_password_form"):
        old_password = st.text_input(t['password_section']['current_password'], type="password")
        new_password = st.text_input(t['password_section']['new_password'], type="password")
        confirm_password = st.text_input(t['password_section']['confirm_password'], type="password")
        submitted = st.form_submit_button(t['password_section']['update_button'], use_container_width=True)
        if submitted:
            if not old_password or not new_password or not confirm_password:
                st.error(t['password_section']['errors']['required'])
            elif new_password != confirm_password:
                st.error(t['password_section']['errors']['mismatch'])
            else:
                response = requests.post(
                    f"{st.session_state['API_URL']}/update_password",
                    json={
                        "email": user["email"],
                        "old_password": old_password,
                        "new_password": new_password,
                        "confirm_password": confirm_password
                    }
                )
                if response.status_code == 200:
                    st.success(t['password_section']['success'])
                else:
                    st.error(response.json().get("message", t['password_section']['api_error']))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button(t['logout_button'], icon=":material/logout:"):
            st.session_state['page'] = 'login'
            st.session_state['logged_in'] = False
            st.session_state['user'] = None
            st.rerun()
