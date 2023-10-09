import pandas as pd
from snowflake import connector

def fetch_data():
    #setting credentials
    import os
    os.environ["SNOWSQL_USR"] = 'pp_guillermo' #insert username
    os.environ["SNOWSQL_PWD"] = 'LionelMessi10' #insert password
    os.environ["SNOWSQL_ACC"] = 'sx14805.west-europe.azure'
    os.environ["SNOWSQL_WH"] = 'COMPUTE_WH'
    os.environ["SNOWSQL_DB"] = 'PYTHON_PROJECT'
    os.environ["SNOWSQL_SCH"] = 'PUBLIC'

    # Connect to Snowflake
    conn = connector.connect(
        user=os.getenv('SNOWSQL_USR'),
        password=os.getenv('SNOWSQL_PWD'),
        account=os.getenv('SNOWSQL_ACC'),
        warehouse=os.getenv('SNOWSQL_WH'),
        database=os.getenv('SNOWSQL_DB'),
        schema=os.getenv('SNOWSQL_SCH')
    )

    # Create a cursor object
    cur = conn.cursor()

    # Define all the setting queries
    queries = [
            'USE ROLE PYTHON_PROJECT;',
            'USE DATABASE PYTHON_PROJECT;',
            'USE SCHEMA PYTHON_PROJECT.PUBLIC;',
            'USE WAREHOUSE COMPUTE_WH;'
            ]

    # Adopt all correct settings
    results=[]
    for query in queries:
        cur.execute(query)
        result = cur.fetchall()
        results.append(result)

    # Print the results to make sure everything ran
    for row in results:
            print(row)

    # Get all data from helper_table
    query = '''SELECT * FROM helper_table'''
    cur.execute(query)
    results = cur.fetchall()

    # Make a dataframe
    helper_df = pd.DataFrame(results, columns=['team_name_tokens', 'team_name_matches', 'common_id'])

    # Get all data from team_hist
    query = '''SELECT * FROM team_hist'''
    cur.execute(query)
    results = cur.fetchall()

    # Make a dataframe
    team_hist_df = pd.DataFrame(results, columns=['team_name_matches', 'match_date', 'team_local_id', 'result', 'team_code'])

    # Get all data from fan_tokens
    query = '''SELECT * FROM fan_tokens'''
    cur.execute(query)
    results = cur.fetchall()

    # Make a dataframe
    fan_tokens_df = pd.DataFrame(results, columns=['id', 'team_name_tokens', 'token_name', 'slug', 'price_date', 'volume', 'price'])

    # Close connection
    cur.close()
    conn.close()

    # General cleaning:
    # Add common_id to both tables
    team_hist_df = team_hist_df.merge(helper_df, on='team_name_matches')
    fan_tokens_df = fan_tokens_df.merge(helper_df, on='team_name_tokens')

    # Change datatypes:
    team_hist_df['time'] = team_hist_df['match_date'].dt.time
    team_hist_df['date'] = team_hist_df['match_date'].dt.date

    fan_tokens_df['date'] = pd.to_datetime(fan_tokens_df['price_date']).dt.date    

    # Return dataframes
    return team_hist_df, fan_tokens_df