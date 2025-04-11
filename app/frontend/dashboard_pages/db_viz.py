import streamlit as st
import pandas as pd
import requests
import time
import os

api_url = os.getenv('API_URL', 'http://127.0.0.1:5000') 

def db_viz(user):
    st.markdown(f"<h3 style='text-align: center;'>Database Visualization 🔬</h3>", unsafe_allow_html=True)
    
    if 'updated' in st.session_state:
        st.session_state.pop("updated")
        st.rerun()
    
    try:
        response = requests.get("f{api_url}/diseases")
        response.raise_for_status()  
        # Get data from the response or session state
        data = response.json().get("diseases")
        diseases = pd.DataFrame(data, columns=[
            "Id", "Nom", "Country_Region", "Confirmed", "Deaths", "Recovered", 
            "Active", "New_cases", "New_deaths", "New_recovered"
        ])
        # Display data editor if user is admin, otherwise display the dataframe
        if user["isAdmin"]:
            diseases_edited = st.data_editor(
                diseases, 
                column_config={
                    "Id": st.column_config.NumberColumn(
                        default=0,
                    ),
                }, 
                num_rows="dynamic"
            )
            if st.button("Update database"):
                data_json = diseases_edited.to_json(orient="records")
                response = requests.put("f{api_url}/update_diseases_route", json={"diseases": data_json}, headers={"Content-Type": "application/json"})
                if response.status_code == 200:
                    my_bar = st.progress(0, text="Updating database...")

                    for percent_complete in range(100):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete + 1, text=f"Updating database... {percent_complete + 1}%")
                    time.sleep(1)
                    my_bar.empty()
                    st.session_state.update({"df": diseases_edited})
                    st.session_state["updated"] = True
                    st.rerun()
                else:
                    st.error("Failed to update database, please ensure there is no empty field.")

        else:
            st.dataframe(diseases)
    except requests.exceptions.RequestException as e:
        st.error(f"No data available, please upload data inside the database.")