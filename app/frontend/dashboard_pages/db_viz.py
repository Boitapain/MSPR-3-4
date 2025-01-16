import streamlit as st
import pandas as pd
import requests

def db_viz(user):
    st.markdown(f"<h3 style='text-align: center;'>Database Visualization 🔬</h3>", unsafe_allow_html=True)
    
    try:
        response = requests.get("http://127.0.0.1:5000/diseases")
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json().get("diseases")
        diseases = pd.DataFrame(data, columns=[
            "Id", "Nom", "Country_Region", "Confirmed", "Deaths", "Recovered", 
            "Active", "New_cases", "New_deaths", "New_recovered"
        ])
        if user["isAdmin"]:
            st.write()
            diseases_edited = st.data_editor(diseases,key="diseases_edit", disabled=("Id", ), num_rows="dynamic")
            if st.button("Update database"):
                data_json = diseases_edited.to_json(orient="records")
                response = requests.post("http://127.0.0.1:5000/update_diseases_route", json={"diseases": data_json}, headers={"Content-Type": "application/json"})
                if response.status_code == 200:
                    st.success("Database updated successfully")
                else:
                    st.error("Failed to update database, please ensure there is no empty field.")

        else:
            st.dataframe(diseases)
    except requests.exceptions.RequestException as e:
        st.error(f"No data available, please upload data inside the database.")