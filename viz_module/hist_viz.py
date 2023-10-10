import pandas as pd
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go

def matches_price_viz(team_hist_df,
                      fan_tokens_df,
                      team_name,
                      start_date='2020-06-25',
                      end_date='2023-10-01'):
    
    # Create team dataframe:
    # Filter by team name
    team_matches = team_hist_df[team_hist_df['team_name_matches'] == team_name]

    # Extract id
    id = team_matches.reset_index().loc[0, 'common_id']

    # Use id to get relevant token rows
    team_tokens = fan_tokens_df[fan_tokens_df['common_id'] == id]

    # Date filtering:
    team_tokens['date_f'] = pd.to_datetime(team_tokens['date'])
    team_df = team_matches.merge(team_tokens, on='date')
    team_df = team_df[(pd.to_datetime(start_date) < team_df['match_date']) & (team_df['match_date'] < pd.to_datetime(end_date))]
    team_tokens = team_tokens[(pd.to_datetime(start_date) < team_tokens['date_f']) & (team_tokens['date_f'] < pd.to_datetime(end_date))]

    # Create a color mapping and results mapping to differentiate wins, draws, and losses:

    color_mapping = {
        'W': 'green',
        'D': 'yellow',
        'L': 'red'
    }

    result_mapping = {
        'W':'Win',
        'D':'Draw',
        'L':'Loss'
    }

    # Create a Plotly Express scatter plot for team prices:
    fig = px.line(team_tokens, x='date', y='price', title=f"Matches and Price Visualization for {team_name}")
    fig.update_traces(hoverinfo='skip', hovertemplate=None)

    # Add scatter points for match results with pop-up text:
    for index, row in team_df.iterrows():
        result_color = color_mapping.get(row['result'], 'black')
        result_name = result_mapping.get(row['result'], '')
        fig.add_trace(go.Scatter(
            x=[row['date']],
            y=[row['price']],
            mode='markers',
            name=row['result'],
            text=[f"Result: {result_name}<br>Date: {row['date']}<br>Price: {row['price']}"],
            hoverinfo='text',
            marker=dict(size=5, color=result_color, symbol='x')
        ))

    # Customize the layout:
    fig.update_xaxes(title="Date")
    fig.update_yaxes(title="Price")
    fig.update_layout(showlegend=False)

    return fig

def matches_volume_viz(team_hist_df,
                       fan_tokens_df,
                      team_name,
                      start_date='2020-06-25',
                      end_date='2023-10-01'):
    
    # Create team dataframe:
    # Filter by team name
    team_matches = team_hist_df[team_hist_df['team_name_matches'] == team_name]

    # Extract id
    id = team_matches.reset_index().loc[0, 'common_id']

    # Use id to get relevant token rows
    team_tokens = fan_tokens_df[fan_tokens_df['common_id'] == id]

    # Date filtering and merging:
    team_tokens['date_f'] = pd.to_datetime(team_tokens['date'])
    team_df = team_matches.merge(team_tokens, on='date')
    team_df = team_df[(pd.to_datetime(start_date) < team_df['match_date']) & (team_df['match_date'] < pd.to_datetime(end_date))]
    team_tokens = team_tokens[(pd.to_datetime(start_date) < team_tokens['date_f']) & (team_tokens['date_f'] < pd.to_datetime(end_date))]

    # Create a color mapping and results mapping to differentiate wins, draws, and losses:

    color_mapping = {
        'W': 'green',
        'D': 'yellow',
        'L': 'red'
    }

    result_mapping = {
        'W':'Win',
        'D':'Draw',
        'L':'Loss'
    }

    # Create a Plotly Express scatter plot for team prices:
    fig = px.line(team_tokens, x='date', y='volume', title=f"Matches and Volume Visualization for {team_name}")
    fig.update_traces(hoverinfo='skip', hovertemplate=None)

    # Add scatter points for match results with pop-up text:
    for index, row in team_df.iterrows():
        result_color = color_mapping.get(row['result'], 'black')
        result_name = result_mapping.get(row['result'], '')
        fig.add_trace(go.Scatter(
            x=[row['date']],
            y=[row['volume']],
            mode='markers',
            name=row['result'],
            text=[f"Result: {result_name}<br>Date: {row['date']}<br>Volume: {row['volume']}"],
            hoverinfo='text',
            marker=dict(size=5, color=result_color, symbol='x')
        ))

    # Customize the layout:
    fig.update_xaxes(title="Date")
    fig.update_yaxes(title="Volume")
    fig.update_layout(showlegend=False)

    return fig

def performace_viz(team_hist_df,
                    teams,
                    start_date='2020-06-25',
                    end_date='2023-10-01'):
    
    # Filter by teams:
    team_df=team_hist_df[team_hist_df['team_name_matches'].isin(teams)]

    # Filter by date:
    team_df = team_df[(pd.to_datetime(start_date) < team_df['match_date']) & (team_df['match_date'] < pd.to_datetime(end_date))]

    # Create a dataframe quantifying performance:
    count_df = team_df.groupby(['team_name_matches', 'result']).agg({'result':'count'}).rename(columns={'result':'count'}).reset_index(level=[0,1])
    total_matches_df = count_df.groupby('team_name_matches').agg({'count':'sum'}).rename(columns={'count':'total'}).reset_index()
    performance_df = count_df.merge(total_matches_df, on='team_name_matches')

    # Create percentage format:
    performance_df['percentage'] = performance_df.apply(lambda row: round(row['count'] / row['total'] * 100, 2), axis=1)

    # Prettify for plotting:
    performance_df.sort_values(['percentage', 'result'], inplace=True)
    result_dict = {
        'W':'Wins',
        'D':'Draws',
        'L':'Losses'
    }
    performance_df['Match Outcome']=performance_df['result'].apply(lambda x: result_dict[x])

    # Create figure with bar:
    fig = px.bar(performance_df, 
             y='team_name_matches', 
             x='percentage', 
             color='Match Outcome', 
             labels={
                 'team_name_matches':'Teams',
                 'percentage':'Percentage'
             }, 
             title='Team Outcomes as Percentage of Total Matches',
             color_discrete_sequence=['#e4745c', '#f4dc34', '#c1dc44'])
    
    # Return figure for plotting:
    return fig