import pandas as pd
import matplotlib.pyplot as plt
from snowflake import connector

#setting credentials
import os
os.environ["SNOWSQL_USR"] = 'darkonimbus' #insert username
os.environ["SNOWSQL_PWD"] = 'PWDsnowflakenimbus1!' #insert password
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

# Print the results
for row in results:
        print(row)

# Create a cursor object
cur = conn.cursor()

query = '''SELECT * FROM team_hist'''
cur.execute(query)
results = cur.fetchall()
results[:5]

# Close the cursor and connection
cur.close()
conn.close()
display(row)

team_hist_df = pd.DataFrame(results, columns=['team_name', 'match_date', 'team_local_id', 'result', 'team_code'])
team_hist_df

# Streamlit App
st.title('Team Results')

# Filter team_name
selected_team = st.selectbox('Select Team:', team_hist_df['team_name'].unique())

# Filter match_date
start_date = st.date_input("Start date", pd.to_datetime(team_hist_df['match_date'].min()))
end_date = st.date_input("End date", pd.to_datetime(team_hist_df['match_date'].max()))

filtered_df = team_hist_df[(team_hist_df['team_name'] == selected_team) & 
                 (pd.to_datetime(team_hist_df['match_date']) >= start_date) & 
                 (pd.to_datetime(team_hist_df['match_date']) <= end_date)]

# Count the results
result_count = filtered_df['result'].value_counts(normalize=True) * 100  # Get percentages

# Plot the chart
st.bar_chart(result_count, use_container_width=True)

if __name__ == "__main__":
    st.run()


    