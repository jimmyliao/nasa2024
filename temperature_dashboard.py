import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import google.generativeai as genai
import requests
from streamlit_lottie import st_lottie

from progress import Progress


def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_temperature_meter = load_lottie_url("https://lottie.host/c2f23b2b-cc34-485a-b466-d0c0af815828/zPAxPvR17j.json")
lottie_earth = load_lottie_url("https://lottie.host/7332295c-98ac-4ba6-8ced-51cbf1ebd984/wUgtDvjY8F.json")


def generate_temperature_story(selected_year, max_temp, min_temp, average_temperatures):
    # 新的提示
    story_prompt = (
        f"In {selected_year}, the country with the maximum temperature change was {max_temp['Country']} "
        f"with a significant increase of {max_temp['Temperature_Change']:.2f}°C. "
        f"Conversely, {min_temp['Country']} experienced the smallest change of {min_temp['Temperature_Change']:.2f}°C. "
        f"This highlights the disparities in climate impact across regions. "
        f"Average temperature changes around the world reflect the pressing issue of global warming. "
        f"Countries are facing unique challenges due to these changes, influencing ecosystems and human activities. "
        f"The data for {selected_year} indicates a need for urgent action against climate change."
    )

    # 生成內容
    response = genai.GenerativeModel('gemini-pro').generate_content(story_prompt)
    st.session_state['temperature_story'] = response.text
    st.session_state.stories_data['temperature_story'] = response.text
    st.session_state.progress = Progress.TEMPERATURE_PAGE_AFTER_GEN_DATA
    
    st.session_state['temperature_data'] = {
        'year': selected_year,
        'max_temp_country': max_temp['Country'],
        'max_temp_change': max_temp['Temperature_Change'],
        'min_temp_country': min_temp['Country'],
        'min_temp_change': min_temp['Temperature_Change'],
    }
    
    return response.text

def temperature_dashboard():
    st.title("§3: About Temperature")

    df = pd.read_csv("data/climate_change_indicators.csv")
    f = open('countries.geo.json')
    world_json = json.load(f)

    # Data preparation
    year_list = [f"F{i}" for i in range(2002, 2022)]
    df_melt = pd.melt(df, id_vars=["Country", "ISO3"], value_vars=year_list)
    df_melt.rename(columns={"variable": "Year", "value": "Temperature_Change"}, inplace=True)
    df_melt['Year'] = df_melt['Year'].str.replace(r'F', '', regex=True).astype(int)
    df_melt['Temperature_Change'] = pd.to_numeric(df_melt['Temperature_Change'], errors='coerce')

    # Streamlit app layout
    colT1, colT2 = st.columns(2)

    with colT1:
        st_lottie(lottie_earth, width=200, height=150)

    with colT2:
        st_lottie(lottie_temperature_meter, width=200, height=150)

    # Year selector
    selected_year = st.session_state.selected_year

    # Filtered data
    filtered_df = df_melt[df_melt["Year"] == selected_year]

    # Indicators for max and min temperature change
    max_temp = filtered_df.loc[filtered_df['Temperature_Change'].idxmax()]
    min_temp = filtered_df.loc[filtered_df['Temperature_Change'].idxmin()]

    left_indicator, right_indicator = st.columns(2)
    with left_indicator:
        st.subheader(f"**Maximum Temperature Change ({max_temp['Country']} - {max_temp['Year']})**")
        st.subheader(f"{max_temp['Temperature_Change']:.2f}°C")
    with right_indicator:
        st.subheader(f"**Minimum Temperature Change ({min_temp['Country']} - {min_temp['Year']})**")
        st.subheader(f"{min_temp['Temperature_Change']:.2f}°C")

    st.markdown("---")

    # Load global temperature data from climate_change_indicators.csv for the selected year
    average_temperatures = df_melt[df_melt['Year'] == selected_year]

    # Plotly Choropleth map to visualize temperatures globally with black background
    st.markdown(f'#### This displays the average national temperature information for a specific year')
    tempFig = go.Figure(data=go.Choropleth(
        locations=average_temperatures['ISO3'],  # Use the ISO3 country code from the new dataset
        z=average_temperatures['Temperature_Change'],
        text=average_temperatures['Country'],
        colorscale='YLORRD',
        autocolorscale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_ticksuffix='°C',
        colorbar_title='Temperature Change (°C)',
    ))

    # Set black background for the map
    tempFig.update_layout(
        title_text=f'Average Temperature Change around the world for {selected_year}',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
            bgcolor='black'  # Set background color to black
        ),
        paper_bgcolor='black',  # Set the background color for the whole figure to black
        font=dict(color='white'),  # Set text color to white for better visibility
    )

    st.plotly_chart(tempFig, use_container_width=True)

    st.markdown("---")

    # Global Temperature Data synchronized with selected year
    df_temperature = pd.read_csv('data/global_temperature.csv')
    df_temperature.rename(columns={'Year': 'year'}, inplace=True)

    # Define the year range (2002-2021)
    year_range = range(2002, 2022)
    df_temperature = df_temperature[df_temperature['year'].isin(year_range)]

    # Filter global temperature data based on the selected year from the slider
    df_temp_selected_year = df_temperature[df_temperature.year == selected_year]

    if not df_temp_selected_year.empty:
        st.markdown(f'#### Global Temperature Anomalies for {selected_year}')

        # Melt temperature data for visualization
        df_temp_melted = df_temp_selected_year.melt(id_vars=['year'],
                                                    value_vars=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                                                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                                                    var_name='Month', value_name='Anomaly')

        # Create a line chart for temperature anomalies
        temp_chart = px.line(df_temp_melted, x='Month', y='Anomaly',
                             title=f'Monthly Global Temperature Anomalies for {selected_year}',
                             labels={'Anomaly': 'Temperature Anomaly (°C)'},
                             markers=True)
        st.plotly_chart(temp_chart, use_container_width=True)

    if st.columns(1)[0].button("Integrate the temperature information here...", use_container_width=True):
        story_content = generate_temperature_story(selected_year, max_temp, min_temp, average_temperatures)
        st.write(story_content)
    else:
        if st.session_state.stories_data['temperature_story']:
            st.write(st.session_state.stories_data['temperature_story'])
