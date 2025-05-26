import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os

api_url = os.getenv('API_URL', 'http://127.0.0.1:5000') 

def stats(user):
    st.markdown("<h3 style='text-align: center;'>Disease Statistics</h3>", unsafe_allow_html=True)
    
    try:
        # Fetch data from the API
        response = requests.get("http://api:5000/diseases")
        response.raise_for_status()
        
        # Parse the response data
        data = response.json().get("diseases")
        if not data:
            st.warning("No data available to display")
            return
        
        # Convert data to a DataFrame
        df = pd.DataFrame(data, columns=[
            "Id", "Name", "Date", "Country", "Confirmed", "Deaths", "Recovered", 
            "New_cases", "New_deaths", "New_recovered"
        ])
        
        if not df.empty:
            # Convert the "Date" column to datetime for filtering
            df["Date"] = pd.to_datetime(df["Date"])
            
            # Extract year and month for grouping
            df["YearMonth"] = df["Date"].dt.to_period("M")
            
            # Get the unique months available in the dataset
            months = sorted(df["YearMonth"].unique())  # Ensure months are sorted
            
            # Create a list of consecutive month pairs
            month_pairs = [(months[i], months[i + 1]) for i in range(len(months) - 1)]
            
            # Use st.columns to place date range and statistic selection side by side
            col1, col2 = st.columns(2)
            
            with col1:
                # User input for selecting a range of consecutive months
                selected_pair = st.selectbox(
                    "Select a consecutive month range",
                    options=month_pairs,
                    format_func=lambda x: f"{x[0]} to {x[1]}"
                )
            
            with col2:
                # User selection for the statistic to display
                stat_options = ["Confirmed", "Deaths", "Recovered", "New_cases", "New_deaths", "New_recovered"]
                selected_stat = st.selectbox("Select the statistic to display", stat_options)
            
            # Filter the DataFrame based on the selected month range
            start_month, end_month = selected_pair
            df = df[(df["YearMonth"] >= start_month) & (df["YearMonth"] <= end_month)]
            
            if df.empty:
                st.warning("No data available for the selected month range")
                return
            
            # User selection for disease
            disease_options = ["All"] + df["Name"].unique().tolist()
            selected_disease = st.selectbox("Select the disease to display", disease_options)
            
            if selected_disease != "All":
                df = df[df["Name"] == selected_disease]
            
            # Display a choropleth map
            fig = px.choropleth(
                df,
                locations="Country",  # Column with country names
                locationmode="country names",  # Match country names
                color=selected_stat,  # Column to determine color intensity
                hover_name="Country",  # Column to display on hover
                title=f"Disease Spread by Country ({selected_stat})",
                color_continuous_scale=[[0, "#FFFFFF"], [1, "#FF4D00"]]  # Shades of #FF4D00
            )
            fig.update_layout(geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"))
            st.plotly_chart(fig)
        else:
            st.warning("No data available to display")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data from the API: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    stats(None)