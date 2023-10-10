import credentials.credentials as c
import requests
import pandas as pd
from snowflake import connector
from raw_data_module import get_data_football

def upload_football_data_to_sf():

    conn = connector.connect(
        user=c.SNOWSQL_USR,
        password=c.SNOWSQL_PWD,
        account=c.SNOWSQL_ACC,
        warehouse=c.SNOWSQL_WH,
        database=c.SNOWSQL_DB,
        schema=c.SNOWSQL_SCH
    )

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

    team_hist_df = get_data_football.get_historical_data()

    #Define the upload query
    query = '''
    INSERT INTO TEAM_HIST (team_name, date, local_team_id, wins, team_code)
    VALUES (%(team_name)s, %(date)s, %(team_id)s, %(wins)s, %(team_code)s)
    '''
    params = team_hist_df.to_dict('records')

    # Assuming CHUNK_SIZE is the size you want each batch to be
    CHUNK_SIZE = 16000  # or any number less than 16,384

    for i in range(0, len(params), CHUNK_SIZE):
        chunk = params[i:i + CHUNK_SIZE]
        cur.executemany(query, chunk)

    # Fetch the results
    results = cur.fetchall()

    # Print the results
    for row in results:
            print(row)

    cur.close()
    conn.close()

def upload_tokens_data_to_snowflake():
    
    # Create connector with credentials to connect to snowflake:
    conn = connector.connect(
        user=c.SNOWSQL_USR,
        password=c.SNOWSQL_PWD,
        account=c.SNOWSQL_ACC,
        warehouse=c.SNOWSQL_WH,
        database=c.SNOWSQL_DB,
        schema=c.SNOWSQL_SCH
    )

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

    # Initial setup from the provided code
    base_url = "https://api.fanmarketcap.com/api/v1/markets/"
    days_value = "max"  # Available values are 7d, 30d, 60d, 90d

    headers = {
        'X-API-KEY': c.TOKENS_API_KEY #insert API key 
    }

    # List of slugs to fetch data for
    slugs = [
        "fc-barcelona-fan-token", "galatasaray-fan-token", "as-roma-fan-token", 
        "manchester-city-fan-token", "lazio-fan-token", "paris-saint-germain-fan-token", 
        "fc-porto-fan-token", "juventus-fan-token", "ac-milan-fan-token", "arsenal-fan-token", 
        "atletico-madrid-fan-token", "trabzonspor-fan-token", "inter-milan-fan-token", 
        "napoli-fan-token", "valencia-fan-token", "young-boys-fan-token", "legia-warsaw-fan-token", 
        "real-sociedad-fan-token", "as-monaco-fan-token", "sevilla-fc-fan-token", "fenerbahce-fan-token", 
        "besiktas-fan-token", "aston-villa-fan-token", "everton-fc-fan-token", "dinamo-zagreb-fan-token", 
        "leeds-united-fan-token", "bologna-fc-fan-token", "udinese-fan-token"
    ]

    # Dictionary to store data for each slug
    data_dict = {}

    # List to store individual dataframes
    df_list = []

    # Loop through each slug and make the API call
    for slug in slugs:
        endpoint_url = f"{base_url}{slug}/{days_value}/"
        response = requests.get(endpoint_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Convert the data to a dataframe
            df = pd.DataFrame(data)
        
            df_list.append(df)

            # Add a new column 'slug' to the dataframe
            df['slug'] = slug

            # Convert the date format
            df['date'] = pd.to_datetime(df['date'], unit='ms').dt.strftime('%Y-%m-%d')
            
            # Create the 'token_name' column
            df['token_name'] = df['slug'].str.replace('-', ' ')

            # Create the 'team_name' column
            df['team_name'] = df['token_name'].str.replace('fan token', '').str.strip()
            
        else:
            print(f"Error for slug {slug}: {response.status_code}: {response.text}")

        # Concatenate all the dataframes in the list into a single dataframe
        fan_tokens_df = pd.concat(df_list, ignore_index=True)

        # Remove the 'market_cap' column
        fan_tokens_df = fan_tokens_df.drop(columns=['market_cap'])

        # Reordering columns 
        fan_tokens_df = fan_tokens_df[['team_name', 'token_name', 'slug', 'date', 'volume', 'price']]


    #Define the query
    query = '''
    INSERT INTO fan_tokens (team_name, token_name, slug, date, volume, price)
    VALUES (%(team_name)s, %(token_name)s, %(slug)s, %(date)s, %(volume)s, %(price)s)
    '''
    params = fan_tokens_df.to_dict('records')

    # Assuming CHUNK_SIZE is the size you want each batch to be
    CHUNK_SIZE = 16000  # or any number less than 16,384

    for i in range(0, len(params), CHUNK_SIZE):
        chunk = params[i:i + CHUNK_SIZE]
        cur.executemany(query, chunk)

    # Fetch the results
    results = cur.fetchall()

    # Print the results
    for row in results:
            print(row)

    cur.close()
    conn.close()

def upload_helper_table():
     
     helper_table_data = [('ac milan', 'AC Milan', 1),
                    ('arsenal', 'Arsenal', 2),
                    ('as monaco', 'AS Monaco', 3),
                    ('as roma', 'AS Roma', 4),
                    ('aston villa', 'Aston Villa', 5),
                    ('atletico madrid', 'Atletico Madrid', 6),
                    ('bologna fc', 'Bologna FC', 7),
                    ('everton fc', 'Everton FC', 8),
                    ('fc barcelona', 'FC Barcelona', 9),
                    ('fc porto', 'FC Porto', 10),
                    ('inter milan', 'Inter Milan', 11),
                    ('juventus', 'Juventus', 12),
                    ('lazio', 'S.S. Lazio', 13),
                    ('leeds united', 'Leeds United', 14),
                    ('manchester city', 'Manchester City', 15),
                    ('napoli', 'Napoli', 16),
                    ('paris saint germain', 'Paris Saint-Germain', 17),
                    ('real sociedad', 'Real Sociedad', 18),
                    ('sevilla fc', 'Sevilla FC', 19),
                    ('udinese', 'Udinese Calcio', 20),
                    ('valencia', 'Valencia CF', 21)]
     
     
