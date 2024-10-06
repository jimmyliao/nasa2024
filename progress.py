import streamlit
from enum import Enum

class Progress(Enum):
    UNKNOWN = 0
    LANDING_PAGE_BEFORE_GEN_DATA = 3
    LANDING_PAGE_AFTER_GEN_DATA = 6
    LANDING_PAGE_CLICKED_NEXT = 10
    CO2_PAGE_BEFORE_GEN_DATA = 13
    CO2_PAGE_AFTER_GEN_DATA = 16
    CO2_PAGE_CLICKED_NEXT = 20
    TEMPERATURE_PAGE_BEFORE_GEN_DATA = 23
    TEMPERATURE_PAGE_AFTER_GEN_DATA = 26
    TEMPERATURE_PAGE_CLICKED_NEXT = 30
    POPULATION_PAGE_BEFORE_GEN_DATA = 33
    POPULATION_PAGE_AFTER_GEN_DATA = 36
    POPULATION_PAGE_CLICKED_NEXT = 40

def is_progress(st: streamlit, progress: Progress):
    return st.session_state.progress.value >= progress.value