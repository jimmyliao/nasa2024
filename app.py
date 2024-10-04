import requests
import plotly.graph_objects as go

import folium
import pandas as pd
import streamlit as st
import google.generativeai as genai
from geopy.geocoders import Nominatim  
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from folium.plugins import DualMap  
import plotly.express as px
import json
import os
from streamlit_lottie import st_lottie
from frontend import my_component
import climate
import globalpop
climate_data = climate
global_population = globalpop

st.set_page_config(page_title="Climate Change Dashboard", layout="wide")

# Configure Google Generative AI
api_key = os.getenv("GENAI_API_KEY")
genai.configure(api_key=api_key)


# Load Lottie animations
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_temperature_meter = load_lottie_url("https://lottie.host/c2f23b2b-cc34-485a-b466-d0c0af815828/zPAxPvR17j.json")
lottie_earth = load_lottie_url("https://lottie.host/7332295c-98ac-4ba6-8ced-51cbf1ebd984/wUgtDvjY8F.json")

# Streamlit app configuration
st.title("🌍 Climate Dashboard")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["CO2 Flux Visualization", "Temperature Dashboard","Population","Summary Page"])

stories_data = {
    'Summary': None,
    'climate_story': None,
    'co2_story': None,
    'temperature_story': None,
    'population_story': None
}


def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'


if page == "CO2 Flux Visualization":
    # CO2 Flux Visualization Page
    st.write("Explore the effects of CO2 emissions using data from the U.S. Greenhouse Gas Center.")
    st.markdown("---")

    # STAC API URLs
    STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
    RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
    collection_name_flux = "eccodarwin-co2flux-monthgrid-v5"
    collection_name_oco2 = "oco2geos-co2-daygrid-v10r"

    # Fetch collections data
    collection_flux = requests.get(f"{STAC_API_URL}/collections/{collection_name_flux}").json()
    collection_oco2 = requests.get(f"{STAC_API_URL}/collections/{collection_name_oco2}").json()

    st.markdown("### Collection Summary")
    st.write(f"**Title:** {collection_flux['title']}")
    st.write(f"**Description:** {collection_flux['description']}")

    st.sidebar.header("Input Options")
    observation_dates = st.sidebar.text_input("Enter observation dates (comma-separated, e.g., 202212, 202104):")
    selected_region = st.sidebar.text_input("Enter a region (e.g., Los Angeles, CA): ")

    st.sidebar.markdown(
        "<div style='color: red; font-size: 12px;'>⚠️ Please do not change the selected region too quickly. "
        "Frequent changes may result in API errors due to request limits.</div>",
        unsafe_allow_html=True
    )

    # Function to get coordinates
    def get_coordinates(location):
        geolocator = Nominatim(user_agent="measurements", timeout=10)
        try:
            location = geolocator.geocode(location)
            if location:
                return (location.latitude, location.longitude)
            else:
                st.error("Location not found. Please try another region.")
                return None
        except GeocoderTimedOut:
            st.error("Geocoding service timed out. Please try again.")
            return None
        except GeocoderUnavailable:
            st.error("Geocoding service is currently unavailable. Please try again later.")
            return None

    # Function to fetch and display CO2 flux maps
    def fetch_and_display_flux_maps(observation_dates, region):
        location = get_coordinates(region)
        if location is None:
            return
        map_ = folium.Map(location=location, zoom_start=7)

        for obs_date in observation_dates:
            observation_id = f'eccodarwin-co2flux-monthgrid-v5-{obs_date}'
            tile = requests.get(
                f"{RASTER_API_URL}/collections/{collection_name_flux}/items/{observation_id}/tilejson.json?"
                f"&assets=co2&color_formula=gamma+r+1.05&colormap_name=magma&rescale=-0.0007,0.0007"
            ).json()
            folium.TileLayer(
                tiles=tile["tiles"][0],
                name=f'{obs_date} CO2 Flux',
                overlay=True,
                opacity=0.8,
                attr="Data Source: U.S. Greenhouse Gas Center"
            ).add_to(map_)
        folium.LayerControl(collapsed=False).add_to(map_)
        st.components.v1.html(map_.get_root().render(), height=600)

    # Fetch OCO-2 CO₂ data and create DualMap for comparison
    def fetch_and_display_oco2_comparison(region):
        location = get_coordinates(region)
        if location is None:
            return

        oco2_items = requests.get(f"{STAC_API_URL}/collections/{collection_name_oco2}/items?limit=2").json()["features"]
        rescale_values = {
            "min": oco2_items[0]["assets"]["xco2"]["raster:bands"][0]["histogram"]["min"],
            "max": oco2_items[0]["assets"]["xco2"]["raster:bands"][0]["histogram"]["max"]
        }

        oco2_1 = requests.get(
            f"{RASTER_API_URL}/collections/{oco2_items[0]['collection']}/items/{oco2_items[0]['id']}/tilejson.json?"
            f"&assets=xco2&color_formula=gamma+r+1.05&colormap_name=magma&rescale={rescale_values['min']},{rescale_values['max']}"
        ).json()

        oco2_2 = requests.get(
            f"{RASTER_API_URL}/collections/{oco2_items[1]['collection']}/items/{oco2_items[1]['id']}/tilejson.json?"
            f"&assets=xco2&color_formula=gamma+r+1.05&colormap_name=magma&rescale={rescale_values['min']},{rescale_values['max']}"
        ).json()

        dual_map = DualMap(location=location, zoom_start=6)

        folium.TileLayer(
            tiles=oco2_1["tiles"][0],
            name="CO2 Concentration (2020)",
            overlay=True,
            attr="OCO-2",
            opacity=0.6
        ).add_to(dual_map.m1)

        folium.TileLayer(
            tiles=oco2_2["tiles"][0],
            name="CO2 Concentration (2019)",
            overlay=True,
            attr="OCO-2",
            opacity=0.6
        ).add_to(dual_map.m2)

        folium.LayerControl(collapsed=False).add_to(dual_map)
        st.components.v1.html(dual_map.get_root().render(), height=600)

    # Display maps if user input is provided
    if observation_dates and selected_region:
        observation_dates_list = [date.strip() for date in observation_dates.split(',')]
        st.markdown("### CO₂ Flux Map")
        fetch_and_display_flux_maps(observation_dates_list, selected_region)
        st.markdown("### OCO-2 CO₂ Concentration Comparison")
        fetch_and_display_oco2_comparison(selected_region)

    def generate_storytelling_content(selected_region, greenhouse_gas_type, observation_dates):
        # Fetch items from the collection
        response = requests.get(f"{STAC_API_URL}/collections/{collection_name_flux}/items").json()

        # Sort items based on start datetime
        items_sorted = sorted(response['features'], key=lambda x: x['properties']['start_datetime'])

        # Filter items based on the selected observation dates
        selected_items = [item for item in items_sorted if item['id'] in [
            f'eccodarwin-co2flux-monthgrid-v5-{date}' for date in observation_dates]]

        # Create a data summary for the story
        data_summary = f"Selected Region: {selected_region}\nGreenhouse Gas Type: {greenhouse_gas_type}\n"
        data_summary += "Observation Data:\n"

        for item in selected_items:
            start_date = item['properties']['start_datetime']
            end_date = item['properties']['end_datetime']
            data_summary += (f"Item ID: {item['id']}, Start Date: {start_date}, End Date: {end_date}, "
                             f"CO2 Flux Description: {item['assets']['co2']['description']}\n")

        # Generate the storytelling content using the AI model
        response = genai.GenerativeModel('gemini-pro').generate_content(
            f"Generate a detailed climate change story based on the following data:\n"
            f"{data_summary}. Provide insights about how CO2 emissions are affecting the region of {selected_region}, "
            f"with a focus on {greenhouse_gas_type} emissions for the dates provided."
        )
        stories_data['co2_story'] = response.text
        return response.text

    greenhouse_gas_type = st.sidebar.selectbox("Select greenhouse gas type:", ["CO2", "CH4", "N2O"])

    if st.sidebar.button("Generate Climate Change Story"):
        if observation_dates and selected_region:
            story_content = generate_storytelling_content(selected_region, greenhouse_gas_type, observation_dates)
            st.markdown("### Climate Change Story")
            st.write(story_content)
        else:
            st.warning("Please enter a region and observation dates to generate a story.")

elif page == "Temperature Dashboard":
    st.markdown("---")

    # Load temperature data
    df = pd.read_csv("data/climate_change_indicators.csv")
    f = open('countries.geo.json')  
    world_json = json.load(f)

    # Data preparation
    year_list = [f"F{i}" for i in range(2002, 2022)]
    df_melt = pd.melt(df, id_vars=["Country"], value_vars=year_list)
    df_melt.rename(columns={"variable": "Year", "value": "Temperature_Change"}, inplace=True)
    df_melt['Year'] = df_melt['Year'].str.replace(r'F', '', regex=True).astype(int)
    df_melt['Temperature_Change'] = pd.to_numeric(df_melt['Temperature_Change'], errors='coerce')

    # Streamlit app layout
    colT1, colT2 = st.columns([1, 2])

    colG1, colG2, colG3, colG4 = st.columns(4)
    with colG2:
        st_lottie(lottie_earth, width=200, height=150)
    with colG4:
        st_lottie(lottie_temperature_meter, width=200, height=150)

    # Year selector
    st.markdown("<h3 style='text-align: center;'>Select Year</h3>", unsafe_allow_html=True)
    selected_year = st.slider("", min_value=int(df_melt['Year'].min()), max_value=int(df_melt['Year'].max()), value=int(df_melt['Year'].min()))

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

    # Load global temperatures for the selected year
    temperatures = pd.read_csv('data/GlobalLandTemperaturesByCountry.csv')
    temperatures['dt'] = pd.to_datetime(temperatures['dt'])
    temperatures['Year'] = temperatures['dt'].dt.year

    # Filter for the selected year and calculate average temperatures by country
    average_temperatures = temperatures[temperatures['Year'] == selected_year].groupby('Country')['AverageTemperature'].mean().reset_index()

    # Load country codes
    countryCodes = pd.read_csv('data/country_code.csv')
    countryCodes.rename(columns={'Country_name': 'Country'}, inplace=True)

    # Merge average temperatures with country codes
    merged_data = pd.merge(average_temperatures, countryCodes, how='outer', left_on='Country', right_on='Country')
    merged_data = merged_data.dropna(how='any', axis=0)

    # Plotly Choropleth map to visualize temperatures globally with black background
    tempFig = go.Figure(data=go.Choropleth(
        locations=merged_data['code_3digit'],
        z=merged_data['AverageTemperature'],
        text=merged_data['Country'],
        colorscale='YLORRD',
        autocolorscale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_ticksuffix='°C',
        colorbar_title='Average Temperature',
    ))

    # Set black background for the map
    st.markdown(f'#### This displays the average national temperature information for a specific year')
    tempFig.update_layout(
        title_text=f'Average Temperature around the world for {selected_year}',
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

    # Dynamic storytelling for Temperature Dashboard
    def generate_temperature_story(selected_year, max_temp_country, min_temp_country):
        story_prompt = (
            f"In {selected_year}, the country with the maximum temperature change was {max_temp_country}, "
            f"experiencing a significant increase of {max_temp['Temperature_Change']:.2f}°C. Conversely, {min_temp_country} saw the smallest change "
            f"of {min_temp['Temperature_Change']:.2f}°C. "
            f"As climate scientists observe rising temperatures globally, this data reflects not only the "
            f"average changes in temperature but also the real impacts on ecosystems, agriculture, and weather patterns. "
            f"Countries like {max_temp_country} are likely facing challenges due to heatwaves and changing rainfall patterns, "
            f"which could severely affect their agriculture and overall quality of life. Meanwhile, {min_temp_country} "
            f"might be struggling with different climate-related phenomena that require urgent attention. "
            f"This highlights the importance of understanding our climate data, as it tells a story that demands action."
            f"Generate an engaging story based on this temperature data and its connection to climate change."
        )

        response = genai.GenerativeModel('gemini-pro').generate_content(story_prompt)
        stories_data['temperature_story'] = response.text

        return response.text

        # Move the Generate Story button to the sidebar
    if st.sidebar.button("Generate Climate Change Story"):
        story_content = generate_temperature_story(selected_year, max_temp['Country'], min_temp['Country'])
        st.markdown("### Climate Change Story")
        st.write(story_content)

elif page == "Population":
    # Load population data
    df_reshaped = pd.read_csv('data/population.csv')
    df_reshaped.rename(columns={'Country Name': 'states', 'Country Code': 'states_code', 'Year': 'year', 'Value': 'population'}, inplace=True)

    # Filter data for years 2002 to 2021
    year_range = list(range(2002, 2022))
    df_reshaped = df_reshaped[df_reshaped['year'].isin(year_range)]

    # Sidebar for year selection and color theme
    with st.sidebar:
        year_list = sorted(df_reshaped.year.unique())
        selected_year = st.selectbox('Select a year', year_list)

        # Filter population data based on selected year
        df_selected_year = df_reshaped[df_reshaped.year == selected_year]
        df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

        color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

    # Display top countries based on selected year
    col = st.columns((1.5, 4.5, 2), gap='medium')

    with col[0]:
        st.markdown('#### Top Countries')
        if not df_selected_year_sorted.empty:
            first_country_name = df_selected_year_sorted.states.iloc[0]
            first_country_population = format_number(df_selected_year_sorted.population.iloc[0])
        else:
            first_country_name = '-'
            first_country_population = '-'

        st.metric(label=first_country_name, value=first_country_population)

    with col[1]:
        st.markdown('#### Total Population')
        choropleth = global_population.make_choropleth(df_selected_year, 'states', 'population', selected_color_theme)
        st.plotly_chart(choropleth, use_container_width=True)

    with col[2]:
        st.markdown('#### Population Data')
        st.dataframe(df_selected_year_sorted,
                     column_order=("states", "population"),
                     hide_index=True,
                     column_config={
                        "states": st.column_config.TextColumn("Countries"),
                        "population": st.column_config.ProgressColumn(
                            "Population",
                            format="%f",
                            min_value=0,
                            max_value=max(df_selected_year_sorted.population),
                        )}
                     )

    # Dynamic storytelling for Population Dashboard
    def generate_population_story(selected_year):
        filtered_data = df_reshaped[df_reshaped["year"] == selected_year]
        max_population = filtered_data.loc[filtered_data['population'].idxmax()]
        min_population = filtered_data.loc[filtered_data['population'].idxmin()]

        # Example of integrating climate change themes
        climate_change_impact = "As we look at the population dynamics, it's crucial to understand how climate change affects these numbers. For instance, in {year}, countries like {high_population_country} face challenges from rising temperatures and extreme weather, which could impact their growth rates. Conversely, countries like {low_population_country} might have different climate-related issues that affect their population stability."

        story = genai.GenerativeModel('gemini-pro').generate_content(
            f"In {selected_year}, the country with the highest population was "
            f"{max_population['states']} with a total of {max_population['population']} people.\n"
            f"On the contrary, {min_population['states']} had the lowest population of "
            f"{min_population['population']} people. "
            f"{climate_change_impact.format(year=selected_year, high_population_country=max_population['states'], low_population_country=min_population['states'])} "
            f"Generate an engaging story based on this population data and its connection to climate change."
        )
        stories_data['population_story'] = story.text

        return story.text

    # Include story generation in the Population Dashboard
    if st.sidebar.button("Generate Population Story"):
        if selected_year:
            story_content = generate_population_story(selected_year)
            st.markdown("### Population Story")
            st.write(story_content)
        else:
            st.warning("Please select a year to generate a story.")

elif page == "Summary Page":
    st.write("This will show the overall average values ​​related to global warming for all countries from 2002 to 2022.")

    launch_data, countries = climate_data.launchPage()
    clicked_country = my_component("leaf", launch_data)

    if clicked_country:
        st.markdown("Clicked country \"%s\" !" % clicked_country)

        # Get data for the clicked country
        country_data = climate_data.get_country_map(clicked_country)
        climate_data.get_scatter(clicked_country)
        if country_data:
            country_info = country_data[0]  # Assume only one country is returned
            country = country_info['Country']
            avg_temp_change = country_info['Avg Temp Change']
            avg_co2_emission = country_info['Avg Co2 Change']
            population = country_info['Population']

            # Display the data
            st.subheader("Climate Data for %s" % country)
            st.write("Average Temperature Change: %.3f" % avg_temp_change)
            st.write("Average CO2 Emission: %.3f" % avg_co2_emission)
            st.write("Population: %s" % population)

            prompt = (
                f"Over the decades, a wealth of data regarding climate change has been produced by scientists, governments, academic institutions, and private companies. "
                f"As climate research advances and the climate crisis escalates, the volume of available data continues to grow. "
                f"However, accessing and understanding this data are two distinct challenges. While scientific information is crucial for climate action decision-making, it is engaging narratives that inspire people to take action. "
                f"Carefully crafted stories based on credible scientific data are essential for making informed decisions regarding climate change.\n\n"

                f"Now, let’s focus on the specific situation in {country}. The data reveals:\n"
                f"- Average Temperature Change: {avg_temp_change}°C\n"
                f"- Average CO2 Emissions: {avg_co2_emission} million tons\n"
                f"- Population: {population}\n\n"

                f"In addition, consider these insights from relevant data:\n"
                f"- Climate Story: {stories_data['climate_story']}\n"
                f"- CO2 Flux Story: {stories_data['co2_story']}\n"
                f"- Temperature Story: {stories_data['temperature_story']}\n"
                f"- Population Story: {stories_data['population_story']}\n\n"

                f"Using this information, craft a compelling narrative about climate change that educates and engages the general public. "
                f"Your story should highlight the implications of the data, addressing the urgency of climate action while making it relatable and interesting. "
                f"Consider incorporating examples of how climate change impacts daily life and the future of the planet. "
                f"Utilize visualizations or compelling imagery where appropriate to enhance the narrative.\n\n"

                f"Focus on specific climate phenomena such as rising temperatures, sea-level rise, or increasing extreme weather events, and encourage your audience to see the importance of their role in addressing these challenges. "
                f"Your goal is to create a narrative that not only informs but also inspires action against climate change."
            )

            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)

            st.subheader("Comprehensive Climate Story")
            st.write(response.text)
