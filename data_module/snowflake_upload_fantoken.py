# Importing connector
import snowflake.connector

#setting credentials
import os
os.environ["SNOWSQL_USR"] = '' #insert username
os.environ["SNOWSQL_PWD"] = '' #insert password
os.environ["SNOWSQL_ACC"] = 'yk87134.west-europe.azure'
os.environ["SNOWSQL_WH"] = 'COMPUTE_WH'
os.environ["SNOWSQL_DB"] = 'PYTHON_PROJECT'
os.environ["SNOWSQL_SCH"] = 'PUBLIC'

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.getenv('SNOWSQL_USR'),
    password=os.getenv('SNOWSQL_PWD'),
    account=os.getenv('SNOWSQL_ACC'),
    warehouse=os.getenv('SNOWSQL_WH'),
    database=os.getenv('SNOWSQL_DB'),
    schema=os.getenv('SNOWSQL_SCH')
)

# Create a cursor object
cur = conn.cursor()

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

# Close the cursor and connection
cur.close()
conn.close()
