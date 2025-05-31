import streamlit as st
import pandas as pd
import requests
import time

def manage_users(user):
    st.markdown("<h3 style='text-align: center;'>Manage Users 👤</h3>", unsafe_allow_html=True)

    if 'users_updated' in st.session_state:
        st.session_state.pop("users_updated")
        st.rerun()

    try:
        response = requests.get(f"{st.session_state['API_URL']}/users")
        response.raise_for_status()
        data = response.json().get("users")
        users = pd.DataFrame(data, columns=[
            "id", "name", "email", "country", "isAdmin"
        ])

        if user["isAdmin"]:
            cols = st.columns([1, 4, 1])
            with cols[1]:
                users_edited = st.data_editor(
                    users,
                    column_config={
                        "id": st.column_config.NumberColumn(),
                        "name": st.column_config.TextColumn(),
                        "email": st.column_config.TextColumn(),
                        "country": st.column_config.TextColumn(
                            default="USA"
                        ),
                        "isAdmin": st.column_config.CheckboxColumn(label="Admin", default=False)
                    },
                    num_rows="dynamic"
                )
                if st.button("Update users database"):
                    users_edited["country"] = users_edited["country"].fillna("USA")
                    if users_edited.isnull().values.any():
                        st.error("Please ensure there are no empty fields before updating.")
                    else:
                        data_json = users_edited.to_json(orient="records")
                        response = requests.put(
                            f"{st.session_state['API_URL']}/update_users",
                            json={"users": data_json},
                            headers={"Content-Type": "application/json"}
                        )
                        if response.status_code == 200:
                            my_bar = st.progress(0, text="Updating users database...")
                            for percent_complete in range(100):
                                time.sleep(0.01)
                                my_bar.progress(percent_complete + 1, text=f"Updating users database... {percent_complete + 1}%")
                            time.sleep(1)
                            my_bar.empty()
                            st.session_state["users_updated"] = True
                            st.rerun()
                        else:
                            st.error("Failed to update users. Please ensure there are no empty fields.")
        else:
            cols = st.columns([1, 2, 1])
            with cols[1]:
                st.dataframe(users)
    except requests.exceptions.RequestException as e:
        st.error("No user data available or API error.")