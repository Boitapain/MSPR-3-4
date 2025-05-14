import streamlit as st

def home(user):
    st.markdown(f"<h3 style='text-align: center;'>Welcome back, {user['name']}! 👋</h3>", unsafe_allow_html=True)

    st.markdown(
        """
        #
        <p style='text-align: center; font-size: 18px;'>
        This is your Disease Tracking Dashboard. Here, you can monitor and analyze disease data, 
        manage datasets, and gain insights into global health trends.
        </p>
        <hr>
        <h4 style='text-align: center;'>What would you like to do today?</h4>
        <ul style='font-size: 16px;'>
            <li>📊 <b>View Statistics:</b> Explore disease trends and visualize data on an interactive map.</li>
            <li>📂 <b>Manage Data:</b> Review existing records or imports new data as an admin in the database.</li>
            <li>🔍 <b>Analyze Trends:</b> Dive deeper into the data to uncover patterns and insights.</li>
        </ul>
        <p style='text-align: center; font-size: 16px;'>
        Use the sidebar to navigate through the dashboard and access the tools you need.
        </p>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    home({"name": "Test User"})