import streamlit as st
import pandas as pd
import requests
from translations import load_translations

def csv_import(user):
    t = load_translations(st.session_state.get('language', 'en'))['csv_import']
    
    st.markdown(f"<h3 style='text-align: center;'>{t['title']}</h3>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(t['file_uploader'], type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(t['preview_title'])
        st.write(df.head())
        
        if st.button(t['import_button']):
            with st.spinner(t['loading_message']):
                try:
                    json_data = df.to_json(orient='records')
                    response = requests.put(f"{st.session_state['API_URL']}/update_diseases_route", json={"diseases": json_data})
                    
                    if response.status_code == 200:
                        st.success(t['success_message'])
                    else:
                        st.error(f"{t['api_error_prefix']} {response.json().get('message')}")
                except Exception as e:
                    st.error(f"{t['general_error_prefix']} {str(e)}")