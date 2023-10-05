import get_data

team_ids_dict=get_data.create_team_ids_dict()

# team_stats_df=get_data.get_team_stats(team_ids_dict)

# print(team_stats_df)

team_hist_df=get_data.get_historical_data(team_ids_dict)

print(team_hist_df)