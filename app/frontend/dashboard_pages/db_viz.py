import streamlit as st
import pandas as pd
import requests

def db_viz(user):
    st.markdown(f"<h3 style='text-align: center;'>Database Visualization</h3>", unsafe_allow_html=True)
    
    try:
        response = requests.get("http://127.0.0.1:5000/diseases")
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json().get("diseases")
        diseases = pd.DataFrame(data)
        if user["isAdmin"]:
            st.data_editor(diseases, num_rows="dynamic")
        else:
            st.dataframe(diseases)
    except requests.exceptions.RequestException as e:
        st.error(f"No data available, please upload data inside the database.")