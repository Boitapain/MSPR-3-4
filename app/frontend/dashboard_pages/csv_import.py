import streamlit as st
import pandas as pd
import requests
import time

def csv_import(user):
    st.markdown(f"<h3 style='text-align: center;'>CSV Import ↧</h3>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of the uploaded CSV file:")
        st.write(df.head())
        
        if st.button("Import CSV into Database"):
            with st.spinner("Importing..."):
                try:
                    # Convert DataFrame to JSON
                    json_data = df.to_json(orient='records')
                    
                    # Send the JSON data to the backend API
                    response = requests.put("http://127.0.0.1:5000/update_diseases_route", json={"diseases": json_data})
                    
                    if response.status_code == 200:
                        st.success("CSV imported successfully!")
                    else:
                        st.error(f"Failed to import CSV: {response.json().get('message')}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")