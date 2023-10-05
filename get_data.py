import pandas as pd
import requests
import os
import datetime
import time



def get_team_stats(team_ids_dict):
    '''Gets team stats from a dictionary containing team names as keys and corresponding ids as values. 
        The dictionary is a result of calling get_team_ids function.
        Might get interrupted, but will run until all the data is gathered.
        This function returns a dataframe with columns = [competitions, first, last, played, wins, draws, losses, name, team_ids]'''

    base_url = 'https://api.football-data.org'
    team_matches_endpoint = '/v4/teams/{id}/matches?limit={limit}&status=FINISHED'
    url = base_url + team_matches_endpoint

    headers = {'X-Auth-Token': 'e5be8e867150491590a74c42e7c265b4'}
    done=[]
    data=[]

    while True:
        try:
            # Your main code that may raise an error
            for name, id in team_ids_dict.items():
                if name not in done:
                    print(f'Getting {name} data')
                    r = requests.get(
                    url=url.format(
                        id=id, 
                        # dateto=str(datetime.date.today()), 
                        # datefrom=str(datetime.date.today() - datetime.timedelta(weeks=8)),
                        limit=20
                        ),
                    headers=headers
                ).json()
                    results = r['resultSet']
                    results['name'] = name
                    results['team_id'] = id
                    data.append(results)
                    done.append(name)
                pass
            # If your code runs successfully, break out of the loop
            break
        except Exception as KeyError:
            # Handle the error, you can log the error message or take appropriate actions
            print(f"An error occurred: {str(KeyError)}")
            
            print(r)
            time_to_wait = int(''.join(c for c in r['message'] if c.isdigit()))
            
            print(f'So far gotten data from: \n {done}')

            print(f'Waiting for {time_to_wait} seconds')

            # Wait for a minute before attempting again
            time.sleep(time_to_wait)

    return pd.DataFrame(data)
