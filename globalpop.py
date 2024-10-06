import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

alt.themes.enable("dark")

st.markdown("""
<style>
[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}
[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}
[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}
[data-testid="stMetricLabel"] {
    display: flex;
    justify-content: center;
    align-items: center;
}
[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    transform: translateX(-50%);
}
[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    transform: translateX(-50%);
}
</style>
""", unsafe_allow_html=True)

# Load population data
df_reshaped = pd.read_csv('data/population.csv')
df_reshaped.rename(
    columns={'Country Name': 'states', 'Country Code': 'states_code', 'Year': 'year', 'Value': 'population'},
    inplace=True)

# Load global temperature data
df_temperature = pd.read_csv('data/global_temperature.csv')
df_temperature.rename(columns={'Year': 'year'}, inplace=True)

# Filter data for years 2002 to 2021
year_range = list(range(2002, 2022))
df_reshaped = df_reshaped[df_reshaped['year'].isin(year_range)]
df_temperature = df_temperature[df_temperature['year'].isin(year_range)]

def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
        y=alt.Y(f'{input_y}:O',
                axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        color=alt.Color(f'max({input_color}):Q',
                        legend=None,
                        scale=alt.Scale(scheme=input_color_theme)),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25),
    ).properties(width=900
                 ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )

    return heatmap

def make_choropleth(input_df, input_id, input_column, input_color_theme):
    # year_list = sorted(df_reshaped.year.unique())

    selected_year = st.session_state.selected_year

    # # Filter population data based on selected year
    # df_selected_year = df_reshaped[df_reshaped.year == selected_year]
    # df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)
    #
    # # Filter temperature data based on selected year
    # df_temp_selected_year = df_temperature[df_temperature.year == selected_year]
    #
    # color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    # selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

    # Filter population data based on selected year
    df_selected_year = df_reshaped[df_reshaped.year == selected_year]
    # df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="country names",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(df_selected_year.population)),
                               scope="world",
                               labels={'population': 'Population'}
                               )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth


def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'


# col = st.columns((1.5, 4.5, 2), gap='medium')
#
# with col[0]:
#     st.markdown('#### Top Countries')
#     if not df_selected_year_sorted.empty:
#         first_country_name = df_selected_year_sorted.states.iloc[0]
#         first_country_population = format_number(df_selected_year_sorted.population.iloc[0])
#     else:
#         first_country_name = '-'
#         first_country_population = '-'
#
#     st.metric(label=first_country_name, value=first_country_population)
#
# with col[1]:
#     st.markdown('#### Total Population')
#     choropleth = make_choropleth(df_selected_year, 'states', 'population', selected_color_theme)
#     st.plotly_chart(choropleth, use_container_width=True)
#
# with col[2]:
#     st.markdown('#### Population Data')
#     st.dataframe(df_selected_year_sorted,
#                  column_order=("states", "population"),
#                  hide_index=True,
#                  width=None,
#                  column_config={
#                      "states": st.column_config.TextColumn("Countries"),
#                      "population": st.column_config.ProgressColumn(
#                          "Population",
#                          format="%f",
#                          min_value=0,
#                          max_value=max(df_selected_year_sorted.population),
#                      )}
#                  )
#
# # Display Global Temperature Data
# if not df_temp_selected_year.empty:
#     st.markdown('#### Global Temperature Anomalies for ' + str(selected_year))
#
#     # Melt temperature data to long format for better visualization
#     df_temp_melted = df_temp_selected_year.melt(id_vars=['year'],
#                                                 value_vars=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
#                                                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
#                                                 var_name='Month', value_name='Anomaly')
#
#     # Create a line chart for temperature anomalies
#     temp_chart = px.line(df_temp_melted, x='Month', y='Anomaly',
#                          title='Monthly Global Temperature Anomalies',
#                          labels={'Anomaly': 'Temperature Anomaly (°C)'},
#                          markers=True)
#     temp_chart.update_layout(template='plotly_dark',
#                              plot_bgcolor='rgba(0, 0, 0, 0)',
#                              paper_bgcolor='rgba(0, 0, 0, 0)',
#                              margin=dict(l=0, r=0, t=0, b=0),
#                              height=400)
#     st.plotly_chart(temp_chart, use_container_width=True)
