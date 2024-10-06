from asyncore import write

import streamlit as st
import google.generativeai as genai

from frontend import my_component
from progress import Progress
import time
import os

def landing():
    st.header("🌍 Climate Dashboard")

    st.write(
        "Welcome to the Climate Dashboard! This dashboard provides a comprehensive overview of global warming and its impact on the environment.")

    default_year = st.session_state.selected_year
    selected_year = st.slider("Select Year", 2002, 2021, default_year)
    if selected_year != default_year:
        #st.session_state.selected_year = selected_year
        st.session_state['selected_year'] = selected_year

    st.write(
        "This will show the overall average values ​​related to global warming for all countries from 2002 to 2022.")

    st.title("§1: The Climate Change")

    st.toast('Loading resources, please note the resource loading progress in the upper right corner.', icon='⚠️')
    time.sleep(.2)
    st.toast('Loading resources, please note the resource loading progress in the upper right corner.', icon='⚠️')

    with st.spinner('Loading..Information is being compiled...'):
        time.sleep(6)

    selected_country = my_component("leaf", st.session_state.launch_data)
    if selected_country:
        st.info("Clicked country \"%s\" !" % selected_country)
        
    else:
        st.warning("Click map to find story of area")

    country_info = next((x for x in st.session_state.launch_data if x["Country"] == selected_country), None)
    #st.session_state['selected_country'] = selected_country
    
    
    
    if country_info is None:
        if selected_country:
            st.error("Area no data, please try another area")
    else:
        country = country_info['Country']
        avg_temp_change = country_info['Avg Temp Change']
        avg_co2_emission = country_info['Avg Co2 Change']
        population = country_info['Population']

        # Display the data
        st.subheader("Climate Data for %s" % country)
        st.write("Average Temperature Change: %.3f" % avg_temp_change)
        st.write("Average CO2 Emission: %.3f" % avg_co2_emission)
        st.write("Population: %s" % population)
        st.markdown("---")
        
        with st.spinner('Loading..Information is being compiled...'):
            time.sleep(6)

        st.toast('LLM is sorting out the information...don’t rush it, it will throw an error if it’s not happy', icon='🥴')
        time.sleep(3)
        st.toast('LLM is sorting out the information...don’t rush it, it will throw an error if it’s not happy', icon='🥴')

        if st.session_state.selected_country != selected_country:
            st.session_state.progress = Progress.LANDING_PAGE_BEFORE_GEN_DATA
            st.session_state.selected_country = selected_country

            # Prepare prompt for LLM
            prompt = (
                f"Based on the provided data, please summarize the global warming situation focusing on the following aspects:\n"
                f"- Country: {country}\n"
                f"- Average Temperature Change: {avg_temp_change}°C\n"
                f"- Average CO2 Emissions: {avg_co2_emission} million tons\n"
                f"- Population: {population}\n\n"
                f"Create a concise narrative that addresses the impacts of climate change and the importance of taking action, using the information above."
            )

            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)

            # Save data to a text file without overwriting
            with open("climate_data_summary.txt", "a") as f:
                f.write(f"Country: {country}, Avg Temp Change: {avg_temp_change}, Avg CO2 Emission: {avg_co2_emission}, Population: {population}\n")
                f.write("This data represents historical average values related to global warming.\n\n")

            if response:
                st.session_state.progress = Progress.LANDING_PAGE_AFTER_GEN_DATA
                st.write(response.text)
        else:
            st.write(st.session_state.stories_data.get("comprehensive_climate_story", "No story available.")) 