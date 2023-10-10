import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

from clean_data_module import get_data_from_sf
from viz_module import hist_viz

st.title('Welcome to ...!')

start_date_str = '2020-01-01'
end_date_str = '2023-12-31'

start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

start_date = st.date_input("Select a starting date:", start_date, min_value=start_date, max_value=end_date)
end_date = st.date_input("Select an ending date:", end_date, min_value=start_date, max_value=end_date)

teams = ['AC Milan', 'AS Roma', 'Arsenal', 'Aston Villa', 'Atletico Madrid',
        'Bologna FC', 'Everton FC', 'FC Barcelona', 'FC Porto',
        'Inter Milan', 'Leeds United', 'Manchester City', 'Napoli',
        'Paris Saint-Germain', 'Real Sociedad', 'S.S. Lazio', 'Sevilla FC',
        'Udinese Calcio', 'Valencia CF']

team_name = st.selectbox('Select your favourite team', teams)

if start_date and end_date and team_name:

    team_hist_df, fan_tokens_df = get_data_from_sf.fetch_data()

    fig = hist_viz.matches_price_viz(team_hist_df=team_hist_df, 
                                     fan_tokens_df=fan_tokens_df, 
                                     team_name=team_name, 
                                     start_date=start_date,
                                     end_date=end_date)
    st.plotly_chart(fig)

    fig = hist_viz.matches_volume_viz(team_hist_df=team_hist_df, 
                                     fan_tokens_df=fan_tokens_df, 
                                     team_name=team_name, 
                                     start_date=start_date,
                                     end_date=end_date)
    st.plotly_chart(fig)

teams = st.multiselect('Select your favourite team', teams)

if start_date and end_date and teams:
    team_hist_df, fan_tokens_df = get_data_from_sf.fetch_data()
    fig = hist_viz.performace_viz(team_hist_df=team_hist_df, 
                                     teams=teams, 
                                     start_date=start_date,
                                     end_date=end_date)
    st.plotly_chart(fig)

