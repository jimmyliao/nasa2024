import pandas as pd
import streamlit as st
import globalpop as global_population
import google.generativeai as genai
from progress import Progress
from streamlit_modal import Modal
import streamlit.components.v1 as components

def population_dashboard():
    # Load population data
    df_reshaped = pd.read_csv('data/population.csv')
    df_reshaped.rename(
        columns={'Country Name': 'states', 'Country Code': 'states_code', 'Year': 'year', 'Value': 'population'},
        inplace=True
    )

    # Filter data for years 2002 to 2021
    year_range = list(range(2002, 2022))
    df_reshaped = df_reshaped[df_reshaped['year'].isin(year_range)]

    # Sidebar for year selection and color theme
    year_list = sorted(df_reshaped.year.unique())
    selected_year = st.session_state.get('selected_year', year_list[0])  # Default to first year

    # Filter population data based on selected year
    df_selected_year = df_reshaped[df_reshaped.year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.columns(1)[0].selectbox('Select a color theme', color_theme_list, key="select_color_theme")

    # Display top countries based on selected year
    col = st.columns((1.5, 4.5, 2), gap='medium')

    with col[0]:
        st.markdown('#### Top Countries')
        if not df_selected_year_sorted.empty:
            first_country_name = df_selected_year_sorted.states.iloc[0]
            first_country_population = global_population.format_number(df_selected_year_sorted.population.iloc[0])
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

    def final(selected_year):
        # Retrieve temperature, CO2, and population data
        filtered_data = df_reshaped[df_reshaped["year"] == selected_year]
        temperature_data = st.session_state.get('temperature_data', {})
        co2_data = st.session_state.get('co2_data', [])
        population_data = st.session_state.get('population_story', [])

        if temperature_data and co2_data and population_data:
            # Concise story prompt focusing on narrative
            
            story_prompt = (
                f"Please use these data {temperature_data}, {co2_data}, {population_data} data to generate a well-founded story based on the data. "
                f"You also need to achieve the effect of educating the public and may also have interesting laughter. While being well-founded, it can also make viewers "
                f"find the story interesting and want to continue reading, and it can educate people who read it to pay attention to the issue of global warming."
            )

            # Use LLM to generate the story
            response = genai.GenerativeModel('gemini-pro').generate_content(story_prompt)

            return response.text
        else:
            return "No sufficient data available for generating the summary."






    
    # Generate the population story
    def generate_population_story(selected_year):
        filtered_data = df_reshaped[df_reshaped["year"] == selected_year]
        max_population = filtered_data.loc[filtered_data['population'].idxmax()]
        min_population = filtered_data.loc[filtered_data['population'].idxmin()]

        # Integrate climate change themes into the population story
        climate_change_impact = (
            "As we look at the population dynamics, it's crucial to understand how climate change affects these numbers. "
            "For instance, in {year}, countries like {high_population_country} face challenges from rising temperatures "
            "and extreme weather, which could impact their growth rates. Conversely, countries like {low_population_country} "
            "might have different climate-related issues that affect their population stability."
        )

        story = genai.GenerativeModel('gemini-pro').generate_content(
            f"In {selected_year}, the country with the highest population was {max_population['states']} "
            f"with {max_population['population']} people. On the contrary, {min_population['states']} had the lowest population "
            f"of {min_population['population']} people. "
            f"{climate_change_impact.format(year=selected_year, high_population_country=max_population['states'], low_population_country=min_population['states'])}"
        )

        # Store the population story in session state
        st.session_state.stories_data['population_story'] = story.text
        st.session_state['population_story'] = {
            "max_population": max_population,
            "min_population": min_population
        }
        st.session_state.progress = Progress.POPULATION_PAGE_AFTER_GEN_DATA
        
        # Save climate data summary to file
        climate_data_summary = (
            f"{selected_year}, {max_population['states']}, {max_population['population']}, "
            f"{min_population['states']}, {min_population['population']}, {choropleth}\n"
        )
        with open('climate_data_summary.txt', 'a') as f:
            f.write(climate_data_summary)

        return story.text

    # Include story generation in the Population Dashboard
    if st.columns(1)[0].button("Generate Population Story", use_container_width=True):
        if selected_year:
            story_content = generate_population_story(selected_year)
            st.markdown("### Population Information")
            st.write(story_content)
            # You can also set temperature and CO2 data here if needed.
            
        else:
            st.warning("Please select a year to generate a story.")
        
        st.markdown("-----")
        st.markdown("### Final Story Summary")      
        final_summary = final(selected_year)    
        st.write(final_summary)
    else:
        if st.session_state.stories_data.get('population_story'):
            st.markdown("### Population Information")
            st.write(st.session_state.stories_data['population_story'])
 

