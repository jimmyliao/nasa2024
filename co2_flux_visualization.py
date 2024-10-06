from geopy import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from folium.plugins import DualMap
import folium
import requests
import streamlit as st
import google.generativeai as genai
import plotly.express as px
from progress import Progress
import pandas as pd
import time

# STAC API URLs
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
collection_name_flux = "eccodarwin-co2flux-monthgrid-v5"
collection_name_oco2 = "oco2geos-co2-daygrid-v10r"

#annual => year , Code  => country
def co2_flux_visualization():
    st.title("§2: CO2 emissions")

    # CO2 Flux Visualization Page
    st.write("Explore the effects of CO2 emissions using data from the U.S. Greenhouse Gas Center.")

    def get_data():
        df_w = pd.read_csv('data/co2_total_world.csv')
        df_w = df_w.drop(columns=['Unnamed: 0'])
        df_total = pd.read_csv('data/co2_total.csv')
        df_total = df_total.drop(columns=['Unnamed: 0'])
        countries = df_total['Entity'].unique()
        return df_w, df_total, countries

    df_w, df_total, countries = get_data()

    # Check if 'year' is already in session state, otherwise set a default
    if 'year' not in st.session_state:
        st.session_state['year'] = 2021
    
    colh1, colh2 = st.columns((4, 2))
    colh1.markdown("## Global CO2 Emissions")
    colh2.markdown("")

    col1, col2 = st.columns((8, 4))
    
    footer = st.container()

    col = 'Annual CO₂ emissions'
    max_value = df_total[col].max()
    min_value = df_total[col].min()

    # Use the year set in landing.py
    #selected_year = st.session_state['year']
    selected_year = st.session_state.get('selected_year', 2021)
    
    #countries = st.session_state['selected_country']
    with st.spinner('Loading..Information is being compiled...'):
        time.sleep(3)
    
    st.toast('LLM is sorting out the information...don’t rush it, it will throw an error if it’s not happy', icon='🥴')
    time.sleep(3)
    st.toast('LLM is sorting out the information...don’t rush it, it will throw an error if it’s not happy', icon='🥴')

    
    # Removed the slider for year selection
    st.markdown(f"### Selected Year: {selected_year}")
    with st.spinner('Loading..Information is being compiled...'):
        time.sleep(5)
    
    # Scatter Geo plot
    with col1:
        fig1 = px.scatter_geo(df_total[df_total['Year'] == selected_year],
                            locations="Code",
                            color=col,
                            size=col,
                            hover_name="Entity",
                            range_color=(min_value, max_value),
                            scope='world',
                            projection='equirectangular',
                            title='World CO2 Emissions',
                            template='plotly_dark',
                            color_continuous_scale=px.colors.sequential.Reds
                            )
        fig1.update_layout(margin={'r': 0, 't': 0, 'b': 0, 'l': 0})

        fig2 = px.choropleth(df_total[df_total['Year'] == selected_year],
                            locations="Code",
                            color=col,
                            hover_name="Entity",
                            range_color=(min_value, max_value),
                            scope='world',
                            projection='equirectangular',
                            title='World CO2 Emissions',
                            template='plotly_dark',
                            color_continuous_scale=px.colors.sequential.Reds
                            )
        fig2.update_layout(margin={'r': 0, 't': 0, 'b': 0, 'l': 0})

        map_type = st.radio("Choose the map style", ["Scatter", "Choropleth"], horizontal=True)
        fig = fig1 if map_type == 'Scatter' else fig2

        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        c = st.multiselect('Add a country:', countries, default=['United States', 'Taiwan'])
        #c = st.session_state.get('selected_country', 'United States')
        tab1, tab2 = col2.tabs(["Graph", "Table"])

        with tab1:
            fig = px.line(df_total[df_total['Entity'].isin(c)], x='Year', y='Annual CO₂ emissions', color='Entity')
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            table = df_total[df_total['Year'] == selected_year]  # Use the selected year
            st.dataframe(table[table['Entity'].isin(c)], use_container_width=True)

    emissions = df_w[df_w['Year'] == selected_year]['Annual CO₂ emissions']
    colh2.metric(label=f"__Total emissions for {selected_year}__", value=emissions)
        
    selected_countries = ', '.join(c)
    
    co2_data = df_total[(df_total['Entity'].isin(c)) & (df_total['Year'] == selected_year)][['Entity', 'Annual CO₂ emissions']]
    st.session_state['co2_data'] = co2_data.to_dict(orient='records')
    data_summary = ""
    for index, row in co2_data.iterrows():
        data_summary += f"{row['Entity']}: {row['Annual CO₂ emissions']} metric tons of CO₂ emissions. "
    
    
    
    st.markdown("### Integrate some information obtained from co2....")
    
    
    if st.session_state.stories_data.get('co2_story'):
        st.write(st.session_state.stories_data['co2_story'])
    else:    
        # Construct the prompt for the LLM
        prompt = (f"In {selected_year}, the countries {selected_countries} had the following CO2 emission data: {data_summary}. "
                f"Using this data, summarize the global warming impact caused by CO2 emissions. "
                f"Explain why it's essential to reduce emissions globally and what strategies could be effective to combat this issue."
                )
        
        response = genai.GenerativeModel('gemini-pro').generate_content(prompt)
        st.session_state.stories_data['co2_story'] = response.text
        
        st.session_state.progress = Progress.CO2_PAGE_AFTER_GEN_DATA
        st.write(response.text)

        # Save the selected year, selected countries, and data summary to a file without overwriting
        with open("climate_data_summary.txt", "a") as f:
            f.write(f"Year: {selected_year}, Countries: {selected_countries},max_value={max_value},min_value={min_value}\n")
            f.write("This data represents the global CO2 emissions for the year related to climate change.\n\n")

