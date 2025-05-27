import streamlit as st
import pandas as pd
import requests
import time


def manage_users(user):
    st.markdown(f"<h3 style='text-align: center;'>User Management 👤</h3>", unsafe_allow_html=True)

    if 'users_updated' in st.session_state:
        st.session_state.pop("users_updated")
        st.rerun()

    try:
        response = requests.get("http://api:5000/users")
        response.raise_for_status()
        data = response.json().get("users")
        # Only show id, email, isAdmin columns
        users_df = pd.DataFrame(data, columns=[
            "id", "name", "email", "isAdmin"
        ])

        #remove currently logged in user from the list
        if user and user.get("id") in users_df["id"].values:
            users_df = users_df[users_df["id"] != user["id"]]
        # Remove columns that are completely empty
        users_df = users_df.dropna(axis=1, how='all')

        # Center the data editor and button
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            users_edited = st.data_editor(
                users_df,
                column_config={
                    "id": st.column_config.NumberColumn(required=True),
                    "email": st.column_config.TextColumn(),
                    "name": st.column_config.TextColumn(),
                    "isAdmin": st.column_config.CheckboxColumn(default=False, label="Admin"),
                },
                num_rows="dynamic"
            )
            if st.button("Update users", use_container_width=True):
                data_json = users_edited.to_json(orient="records")
                response = requests.put(
                    "http://api:5000/update_users",
                    json={"users": data_json},
                    headers={"Content-Type": "application/json"}
                )
                if response.status_code == 200:
                    my_bar = st.progress(0, text="Updating users...")
                    for percent_complete in range(100):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete + 1, text=f"Updating users... {percent_complete + 1}%")
                    time.sleep(1)
                    my_bar.empty()
                    st.session_state["users_updated"] = True
                    st.rerun()
                else:
                    st.error("Failed to update users, please ensure there is no empty field.")
    except requests.exceptions.RequestException as e:
        st.error("No user data available or failed to connect to API.")