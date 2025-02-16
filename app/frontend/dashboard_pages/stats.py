import streamlit as st
import pandas as pd
import requests
import plotly.express as px

def stats(user):
    st.markdown("<h3 style='text-align: center;'>Disease Statistics</h3>", unsafe_allow_html=True)
    
    try:
        response = requests.get("http://127.0.0.1:5000/diseases")
        response.raise_for_status()  
        # Get data from the response or session state
        data = response.json().get("diseases")
        df = pd.DataFrame(data, columns=[
            "Id", "Nom", "Country_Region", "Confirmed", "Deaths", "Recovered", 
            "Active", "New_cases", "New_deaths", "New_recovered"
        ])
    
        if not df.empty:
            # User selection for statistics
            stat_options = [
                "Total Confirmed Cases by Country",
                "Total Deaths by Country",
                "Total Recovered by Country",
                "New Cases by Country",
                "New Deaths by Country",
                "New Recovered by Country"
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
            
            st.plotly_chart(fig)
        else:
            st.warning("No data available to display")
    except requests.exceptions.RequestException as e:
        st.error(f"No data available, please upload data inside the database.")

if __name__ == "__main__":
    stats(None)