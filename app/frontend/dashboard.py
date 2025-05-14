import streamlit as st
from dashboard_pages.home import home
from dashboard_pages.csv_import import csv_import
from dashboard_pages.db_viz import db_viz
from dashboard_pages.stats import stats
from dashboard_pages.profile import profile

def dashboard(user):
    # Initialize session state for dashboard page if it doesn't exist
    if 'dashboard_page' not in st.session_state:
        st.session_state['dashboard_page'] = 'home'

    st.markdown(
    """
    <style>
    /* Customize the sidebar container */
    [data-testid="stSidebar"] {
        background-color: #D1D5DB !important;
        width: fit-content !important; /* Use a fixed width for consistency */
    }

    /* Customize text inside the sidebar */
    [data-testid="stSidebar"] span {
        font-weight: bold; /* Optional: Make the text bold */
    }               

    </style>
    """,
    unsafe_allow_html=True
)
    # Sidebar with navigation buttons
    with st.sidebar:
        st.markdown("""
        <h1>Disease Track<img style="width:40px;" src='https://mspr-team.gitbook.io/~gitbook/image?url=https%3A%2F%2F4141789323-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Forganizations%252Fu9WT6puw9kHCPITtWSCY%252Fsites%252Fsite_dWsRi%252Ficon%252FSHNWRyAl3InsU3QGPMP5%252FCoronavirus.png%3Falt%3Dmedia%26token%3Dd44d9f14-0f59-49c2-8fe0-3c80809684b8&width=32&dpr=2&quality=100&sign=e351430e&sv=2'/></h1>
        """,unsafe_allow_html=True)
        # Home button
        st.button("Home", type="tertiary", icon=":material/home:", on_click=lambda: st.session_state.update({"dashboard_page": "home"}))
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)



        # CSV Import button
        st.header("Data Management")
        if user["isAdmin"]:
            st.button("CSV Import", type="tertiary", icon=":material/download:", on_click=lambda: st.session_state.update({"dashboard_page": "csv_import"}))
        
        # Database Visualization button
        st.button("Database", type="tertiary", icon=":material/database:", on_click=lambda: st.session_state.update({"dashboard_page": "database"}))
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        
        st.header("Data Visualization")
        # Database Visualization button
        st.button("Statistics", type="tertiary", icon=":material/monitoring:", on_click=lambda: st.session_state.update({"dashboard_page": "statistics"}))
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        
        
        # Settings button
        st.header("Settings")
        st.button("Profile", type="tertiary", icon=":material/person:", on_click=lambda: st.session_state.update({"dashboard_page": "profile"}))
    
    # Display the appropriate page based on session state
    if st.session_state['dashboard_page'] == 'home':
        home(user)
    elif st.session_state['dashboard_page'] == 'csv_import':
        csv_import(user)
    elif st.session_state['dashboard_page'] == 'database':
        db_viz(user)
    elif st.session_state['dashboard_page'] == 'statistics':
        stats(user)
    elif st.session_state['dashboard_page'] == 'profile':
        profile(user)
if __name__ == "__main__":
    dashboard("User")