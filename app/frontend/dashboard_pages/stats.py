import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os

api_url = os.getenv('API_URL', 'http://127.0.0.1:5000') 

def stats(user):
    st.markdown("<h3 style='text-align: center;'>Disease Statistics</h3>", unsafe_allow_html=True)
    
    try:
        response = requests.get("f{api_url}/diseases")
        response.raise_for_status()  
        # Get data from the response or session state
        data = response.json().get("diseases")
        df = pd.DataFrame(data, columns=[
            "Id", "Nom", "Country_Region", "Confirmed", "Deaths", "Recovered", 
            "Active", "New_cases", "New_deaths", "New_recovered"
        ])
    
        if not df.empty:
            # User selection for disease and statistics
            disease_options = ["All"] + df["Nom"].unique().tolist()
            selected_disease = st.selectbox("Select the disease to display", disease_options)
            
            if selected_disease != "All":
                df = df[df["Nom"] == selected_disease]
            
            stat_options = [
                "Total Confirmed Cases by Country",
                "Total Deaths by Country",
                "Total Recovered by Country",
                "New Cases by Country",
                "New Deaths by Country",
                "New Recovered by Country",
                "Confirmed vs Deaths Scatter Plot",
                "Recovered Cases Pie Chart",
                "Confirmed Cases Line Chart",
                "Deaths Area Chart"
            ]
            selected_stat = st.selectbox("Select the statistic to display", stat_options)
            
            if selected_stat == "Total Confirmed Cases by Country":
                fig = px.bar(df, x='Country_Region', y='Confirmed', color='Nom', title='Total Confirmed Cases by Country')
            elif selected_stat == "Total Deaths by Country":
                fig = px.bar(df, x='Country_Region', y='Deaths', color='Nom', title='Total Deaths by Country')
            elif selected_stat == "Total Recovered by Country":
                fig = px.bar(df, x='Country_Region', y='Recovered', color='Nom', title='Total Recovered by Country')
            elif selected_stat == "New Cases by Country":
                fig = px.bar(df, x='Country_Region', y='New_cases', color='Nom', title='New Cases by Country')
            elif selected_stat == "New Deaths by Country":
                fig = px.bar(df, x='Country_Region', y='New_deaths', color='Nom', title='New Deaths by Country')
            elif selected_stat == "New Recovered by Country":
                fig = px.bar(df, x='Country_Region', y='New_recovered', color='Nom', title='New Recovered by Country')
            elif selected_stat == "Confirmed vs Deaths Scatter Plot":
                fig = px.scatter(df, x='Confirmed', y='Deaths', color='Country_Region', title='Confirmed vs Deaths Scatter Plot')
            elif selected_stat == "Recovered Cases Pie Chart":
                fig = px.pie(df, names='Country_Region', values='Recovered', title='Recovered Cases Pie Chart')
            elif selected_stat == "Confirmed Cases Line Chart":
                fig = px.line(df, x='Country_Region', y='Confirmed', color='Nom', title='Confirmed Cases Line Chart')
            elif selected_stat == "Deaths Area Chart":
                fig = px.area(df, x='Country_Region', y='Deaths', color='Nom', title='Deaths Area Chart')
            
            st.plotly_chart(fig)
        else:
            st.warning("No data available to display")
    except requests.exceptions.RequestException as e:
        st.error(f"No data available, please upload data inside the database.")

if __name__ == "__main__":
    stats(None)