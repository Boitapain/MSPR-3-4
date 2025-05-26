import streamlit as st
import pandas as pd
import requests
import plotly.express as px

def stats(user):
    st.markdown("<h1 id='main-title' style='text-align: center;'>Disease Statistics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<section aria-labelledby='main-title'>", unsafe_allow_html=True)

    try:
        # Fetch data from the API
        response = requests.get("http://api:5000/diseases")
        response.raise_for_status()
        
        # Parse the response data
        data = response.json().get("diseases")
        if not data:
            st.warning("No data available to display.")
            return
        
        # Convert data to a DataFrame
        df = pd.DataFrame(data, columns=[
            "Id", "Name", "Date", "Country", "Confirmed", "Deaths", "Recovered", 
            "New_cases", "New_deaths", "New_recovered"
        ])
        
        if not df.empty:
            # Convert the "Date" column to datetime for filtering
            df["Date"] = pd.to_datetime(df["Date"])
            df["YearMonth"] = df["Date"].dt.to_period("M")
            months = sorted(df["YearMonth"].unique())
            month_pairs = [(months[i], months[i + 1]) for i in range(len(months) - 1)]

            # Interface utilisateur
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📅 Select a consecutive month range")
                selected_pair = st.selectbox(
                    "Month range:",
                    options=month_pairs,
                    format_func=lambda x: f"{x[0]} to {x[1]}"
                )
            with col2:
                st.markdown("#### 📊 Select the statistic to display")
                stat_options = ["Confirmed", "Deaths", "Recovered", "New_cases", "New_deaths", "New_recovered"]
                selected_stat = st.selectbox("Statistic:", stat_options)
            
            # Filtrage
            start_month, end_month = selected_pair
            df = df[(df["YearMonth"] >= start_month) & (df["YearMonth"] <= end_month)]
            
            if df.empty:
                st.warning("No data available for the selected month range.")
                return
            
            disease_options = ["All"] + df["Name"].unique().tolist()
            selected_disease = st.selectbox("🦠 Select the disease to display", disease_options)
            
            if selected_disease != "All":
                df = df[df["Name"] == selected_disease]
            
            summary_df = df.groupby("Country")[selected_stat].sum().reset_index()

            # Carte choroplèthe
            fig = px.choropleth(
                df,
                locations="Country",
                locationmode="country names",
                color=selected_stat,
                hover_name="Country",
                title=f"Disease Spread by Country ({selected_stat})",
                color_continuous_scale=[[0, "#FFFFFF"], [1, "#FF4D00"]]
            )
            fig.update_layout(geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"))
            st.plotly_chart(fig)

            # Tableau accessible
            st.markdown("### 📋 Raw Data Table (Accessible)")
            table_df = summary_df.sort_values(by=selected_stat, ascending=False)
            st.table(table_df)
        else:
            st.warning("No data available to display.")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data from the API: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    
    st.markdown("</section>", unsafe_allow_html=True)

if __name__ == "__main__":
    stats(None)
