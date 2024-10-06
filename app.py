import climate as climate_data
import streamlit as st

st.set_page_config(
    layout="wide",
    page_icon="🌎"
)

import google.generativeai as genai
import pyautogui

from population import population_dashboard
from progress import Progress, is_progress
from landing import landing
from landing import landing
from co2_flux_visualization import co2_flux_visualization
from temperature_dashboard import temperature_dashboard
from time import sleep
from streamlit.components.v1 import html

# Function to clear the climate data summary file
def clear_climate_data_summary():
    with open('climate_data_summary.txt', 'w') as f:
        # Write nothing to effectively clear the file
        f.write("")

# Detect if the page is refreshed or loaded for the first time
if "page_initialized" not in st.session_state:
    # This block only runs when the page is refreshed
    st.session_state.page_initialized = True
    clear_climate_data_summary()  # Clear the file on page refresh


if "progress" not in st.session_state:
    st.session_state.progress = Progress.UNKNOWN

if "selected_year" not in st.session_state:
    st.session_state.selected_year = 2021

if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

if "selected_greenhouse_gas_type" not in st.session_state:
    st.session_state.selected_greenhouse_gas_type = None

if "stories_data" not in st.session_state:
    st.session_state.stories_data = {
        'Summary': None,
        'climate_story': None,
        'co2_story': None,
        'temperature_story': None,
        'population_story': None
    }

if "launch_data" not in st.session_state or "countries" not in st.session_state or "country_data" not in st.session_state:
    with st.spinner("Loading launch data..."):
        st.session_state.launch_data, st.session_state.countries = climate_data.launchPage()
        st.session_state.country_data = climate_data.get_country_map(st.session_state.launch_data[0])

if "flux_maps" not in st.session_state:
    st.session_state.flux_maps = None

if "oco2_comparison" not in st.session_state:
    st.session_state.oco2_comparison = None

# Configure Google Generative AI
api_key = 'AIzaSyAD86BMs-X7nmvsQ0eh8hsuv_I1ai60-0c'  # Replace with your actual API key
genai.configure(api_key=api_key)

landing()

if is_progress(st, Progress.LANDING_PAGE_AFTER_GEN_DATA):
    if st.columns(1)[0].button("Next Story", use_container_width=True, key="to_co2"):
        st.session_state.progress = Progress.LANDING_PAGE_CLICKED_NEXT
        st.session_state.flux_maps = None
        st.session_state.oco2_comparison = None
        st.session_state.stories_data['co2_story'] = None

if is_progress(st, Progress.LANDING_PAGE_CLICKED_NEXT):
    st.markdown("---")
    co2_flux_visualization()

if is_progress(st, Progress.CO2_PAGE_AFTER_GEN_DATA):
    if st.columns(1)[0].button("Next Story", use_container_width=True, key="to_temperature"):
        st.session_state.progress = Progress.CO2_PAGE_CLICKED_NEXT
        st.session_state.stories_data['temperature_story'] = None

if is_progress(st, Progress.CO2_PAGE_CLICKED_NEXT):
    st.markdown("---")
    temperature_dashboard()

if is_progress(st, Progress.TEMPERATURE_PAGE_AFTER_GEN_DATA):
    if st.columns(1)[0].button("Next Story", use_container_width=True, key="to_population"):
        st.session_state.progress = Progress.TEMPERATURE_PAGE_CLICKED_NEXT

if is_progress(st, Progress.TEMPERATURE_PAGE_CLICKED_NEXT):
    st.markdown("---")
    population_dashboard()

if is_progress(st, Progress.POPULATION_PAGE_AFTER_GEN_DATA):
    if st.columns(1)[0].button("Try another story from scratch", use_container_width=True, key="the_end"):
        st.session_state.progress = Progress.UNKNOWN
        st.balloons()
        pyautogui.press('f5')