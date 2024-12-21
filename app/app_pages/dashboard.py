import streamlit as st
from app_pages.dashboard_pages.home import home
from app_pages.dashboard_pages.profile import profile
from app_pages.dashboard_pages.settings import settings

def dashboard(user):
    if 'dashboard_page' not in st.session_state:
        st.session_state['dashboard_page'] = 'home'

    st.markdown("""
    <style>
        h1 {
            text-shadow: 2px 2px 6px rgba(168, 168, 168, 1);
        }
        [data-testid=stSidebar] {
            background-color: #6EE7B7;
        }
        .stButton button{
                display: flex;  
                margin: 10px auto;
        }
        .stButton button:hover{
                color:black;
                transition: 0.5s;
                transform: scale(1.1);
        }
        .stButton button span {
            font-size: 2.5rem;
            margin-right: 20px;
            text-align: center;
            text-shadow: 2px 2px 6px rgba(100, 100, 100, 1);
        }
        .stButton button div {
            font-size: 1.25rem;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.button("Home",type="tertiary", icon=":material/home:", on_click=lambda: st.session_state.update({"dashboard_page": "home"}))
        
        st.divider()
        
        st.button("CSV Import",type="tertiary", icon=":material/download:", on_click=lambda: st.session_state.update({"dashboard_page": "settings"}))
        
        st.divider()
        
        st.button("Account",type="tertiary", icon=":material/account_circle:", on_click=lambda: st.session_state.update({"dashboard_page": "profile"}))

    if st.session_state['dashboard_page'] == 'home':
        home(user)
    elif st.session_state['dashboard_page'] == 'profile':
        profile(user)
    elif st.session_state['dashboard_page'] == 'settings':
        settings(user)

if __name__ == "__main__":
    dashboard("User")