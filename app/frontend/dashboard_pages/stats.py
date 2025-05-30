import streamlit as st
import pandas as pd
import requests
import plotly.express as px

from translations import load_translations

def stats(user):
    lang = st.session_state['language']
    translations = load_translations(lang)
    t = translations['stats']
    
    st.markdown(f"<h1 id='main-title' style='text-align: center;'>{t['title']}</h1>", unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{st.session_state['API_URL']}/diseases")
        response.raise_for_status()
        data = response.json().get("diseases")
        
        if not data:
            st.warning(t['data_fetch']['no_data'])
            return
            
        df = pd.DataFrame(data, columns=[
            "Id", "Name", "Date", "Country", "Confirmed", "Deaths", "Recovered", 
            "New_cases", "New_deaths", "New_recovered"  # Keep original English column names
        ])
        
        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"])
            df["YearMonth"] = df["Date"].dt.to_period("M")
            months = sorted(df["YearMonth"].unique())
            month_pairs = [(months[i], months[i + 1]) for i in range(len(months) - 1)]

            # UI in translated labels, but keep English values
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"#### {t['filters']['month_range']['title']}")
                selected_pair = st.selectbox(
                    t['filters']['month_range']['label'],
                    options=month_pairs,
                    format_func=lambda x: t['filters']['month_range']['format'].format(start=x[0], end=x[1])
                )
            with col2:
                st.markdown(f"#### {t['filters']['statistic']['title']}")
                selected_stat = st.selectbox(
                    t['filters']['statistic']['label'], 
                    options=["Confirmed", "Deaths", "Recovered", "New_cases", "New_deaths", "New_recovered"]  # English values
                )
            
            # Rest of the code remains the same...
            start_month, end_month = selected_pair
            df = df[(df["YearMonth"] >= start_month) & (df["YearMonth"] <= end_month)]
            
            disease_options = ["All"] + df["Name"].unique().tolist()  # English disease names
            selected_disease = st.selectbox(t['filters']['disease']['label'], disease_options)
            
            if selected_disease != "All":
                df = df[df["Name"] == selected_disease]
            
            # Visualization titles use translated templates but English stat names
            fig = px.choropleth(
                df,
                locations="Country",
                locationmode="country names",
                color=selected_stat,  # English column name
                title=t['visualizations']['map_title'].format(stat=selected_stat)  # English stat in translated template
            )
            st.plotly_chart(fig)
            
            st.markdown(f"### {t['visualizations']['table_title']}")
            st.table(df)
            
    except requests.exceptions.RequestException as e:
        st.error(t['data_fetch']['api_error'].format(error=e))
    except Exception as e:
        st.error(t['data_fetch']['general_error'].format(error=e))
if __name__ == "__main__":
    stats(None)