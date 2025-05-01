import streamlit as st

def profile(user):
    st.markdown("<h1 style='text-align: center;'>Your profile</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:1.5rem;'>User: <b>{user['name']}</b></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:1.5rem;'>Email: <span style='color:blue;'>{user['email']}</span></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:1.5rem;'>Is Admin: <b>{True if user['isAdmin'] == 1 else False}</b></h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Logout", icon=":material/logout:"):
            st.session_state['page'] = 'login'
            st.session_state['logged_in'] = False
            st.session_state['user'] = None
            st.rerun()

    
