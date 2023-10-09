#importing packages and libraries 
import requests
import pandas as pd

# Initial setup from the provided code
base_url = "https://api.fanmarketcap.com/api/v1/markets/"
days_value = "max"  # Available values are 7d, 30d, 60d, 90d

headers = {
    'X-API-KEY': '' #insert API key 
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