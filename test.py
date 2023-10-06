# import data_module.get_data as get_data

# team_ids_dict=get_data.create_team_ids_dict()

# team_ids_dict_test={'FC Barcelona': '81',
#                     'Galatasaray': '610',
#                     'AS Roma': '100'}

# # team_stats_df=get_data.get_team_stats(team_ids_dict)

# # print(team_stats_df)

# team_hist_df=get_data.get_historical_data(team_ids_dict_test)

# print(team_hist_df.tail())

import snowflake.connector

# #setting credentials
# import os
# os.environ["SNOWSQL_USR"] = 'pp_guillermo' #insert username
# os.environ["SNOWSQL_PWD"] = 'LionelMessi10' #insert password
# os.environ["SNOWSQL_ACC"] = 'sx14805.west-europe.azure'
# os.environ["SNOWSQL_WH"] = 'COMPUTE_WH'
# os.environ["SNOWSQL_DB"] = 'PYTHON_PROJECT'
# os.environ["SNOWSQL_SCH"] = 'PUBLIC'