import pandas as pd
import requests
import os
import datetime
import time

from raw_data_module.clean_data import wins

def create_team_ids_dict():
    '''This function creates a dictionary out of a specified string of team ids and names'''
    team_ids = '81,610,100,65,110,524,503,109,98,57,78,108,113,95,92,548,559,613,600,58,62,755,341,103,115'.split(',')
    teams_string = '''FC Barcelona
    Galatasaray
    AS Roma
    Manchester City
    S.S. Lazio
    Paris Saint-Germain
    FC Porto
    Juventus 
    AC Milan
    Arsenal
    Atletico Madrid 
    Inter Milan
    Napoli
    Valencia CF
    Real Sociedad
    AS Monaco 
    Sevilla FC
    Leeds United
    Bologna FC
    Udinese Calcio'''

    token_teams=[t.strip() for t in teams_string.split('\n')]

    return {k:v for k, v in zip(token_teams, team_ids)}


def get_team_stats(team_ids_dict, 
                   beginning_date = '2020-04-17', 
                   end_date = '',
                   limit=100):
    
    '''Gets team stats from a dictionary containing team names as keys and corresponding ids as values. 
        The dictionary is a result of calling get_team_ids function.
        Might get interrupted, but will run until all the data is gathered.
        This function returns a dataframe with columns = [competitions, first, last, played, wins, draws, losses, name, team_ids]'''

    if not end_date:
        end_date = str(datetime.datetime.strptime(beginning_date, '%Y-%m-%d') + datetime.timedelta(days=740)).split(' ')[0]

    print('Getting data from {beginning_date} to {end_date}'.format(beginning_date=beginning_date, end_date=end_date))

    base_url = 'https://api.football-data.org'
    team_matches_endpoint = '/v4/teams/{id}/matches?dateFrom={datefrom}&dateTo={dateto}&limit={limit}&status=FINISHED'

    headers = {'X-Auth-Token': 'e5be8e867150491590a74c42e7c265b4'}
    done=[]
    data=[]
    name_ = ''

    while True:
        try:
            # Your main code that may raise an error
            for name, id in team_ids_dict.items():
                if name not in done:
                    
                    name_=name
                    print(f'Getting {name_} data')

                    url = base_url + team_matches_endpoint.format(
                        id=id, 
                        datefrom=beginning_date, 
                        dateto=end_date,
                        limit=limit
                        )

                    r = requests.get(
                        url=url,
                        headers=headers
                    ).json()

                    results = r['resultSet']
                    results['name'] = name
                    results['team_id'] = id
                    
                    data.append(results)
                    done.append(name_)
                pass
            # If your code runs successfully, break out of the loop
            break
        except Exception as KeyError:
            # Handle the error, you can log the error message or take appropriate actions
            print(f"An error occurred: {str(KeyError)}")
            
            print(r)
            try:
                # Covert message to waiting time: 
                time_to_wait = int(''.join(c for c in r['message'] if c.isdigit()))
                
                print(f'So far gotten data from: \n {done}')
                print(f'Waiting for {time_to_wait} seconds')

                # Wait for before attempting again
                time.sleep(time_to_wait)

            except ValueError:
                print('No time specified, moving onto next team')
                done.append(name_)
            

    return pd.DataFrame(data)

def get_historical_data(team_ids_dict,
                        beginning_date = '2020-04-17',
                        end_date = '',
                        limit=1000):
        
        if not end_date:
            end_date = str(datetime.datetime.strptime(beginning_date, '%Y-%m-%d') + datetime.timedelta(days=740)).split(' ')[0]
        
        print('Getting data from {beginning_date} to {end_date}'.format(beginning_date=beginning_date, end_date=end_date))
    
        base_url = 'https://api.football-data.org'
        team_matches_endpoint = '/v4/teams/{id}/matches?dateFrom={datefrom}&dateTo={dateto}&limit={limit}&status=FINISHED'
        headers = {'X-Auth-Token': 'e5be8e867150491590a74c42e7c265b4'}

        done=[]
        name_ = ''

        total_df = pd.DataFrame()

        # The following code should loop through every team_id:
        
        while True:
            try:
                # Your main code that may raise an error
                for name, id in team_ids_dict.items():
                    if name not in done:

                        name_=name
                        print(f'Getting {name_} data')

                        url = base_url + team_matches_endpoint.format(
                                                id=id, 
                                                datefrom=beginning_date, 
                                                dateto=end_date,
                                                limit=limit
                                                )

                        r = requests.get(
                                url=url,
                                headers=headers
                                ).json()
                        
                        team_df = pd.DataFrame()
                        
                        date=[]
                        away_team = []
                        away_team_code = []
                        home_team=[]
                        home_team_code = []
                        winner=[]
                        team=[]
                        team_id=[]



                        for match in r['matches']:
                                winner.append(match['score']['winner'])
                                date.append(match['utcDate'])
                                away_team.append(match['awayTeam']['shortName'])
                                home_team.append(match['homeTeam']['shortName'])
                                away_team_code.append(match['awayTeam']['tla'])
                                home_team_code.append(match['homeTeam']['tla'])
                                team.append(name_)
                                team_id.append(id)

                        team_df['winner']=winner
                        team_df['date']=date
                        team_df['away_team']=away_team
                        team_df['away_team_code']=away_team_code
                        team_df['home_team']=home_team
                        team_df['home_team_code']=home_team_code
                        team_df['team_name']=team
                        team_df['team_id']=team_id

                        total_df = pd.concat([total_df,team_df])

                        done.append(name_)

                    pass
                # If your code runs successfully, break out of the loop
                break
            except Exception as KeyError:
                # Handle the error, you can log the error message or take appropriate actions
                print(f"An error occurred: {str(KeyError)}")
                
                print(r)
                try:
                    # Covert message to waiting time: 
                    time_to_wait = int(''.join(c for c in r['message'] if c.isdigit()))
                    
                    print(f'So far gotten data from: \n {done}')
                    print(f'Waiting for {time_to_wait} seconds')

                    # Wait for before attempting again
                    time.sleep(time_to_wait)

                except ValueError:
                    print('No time specified, moving onto next team')
                    del team_ids_dict[name_]

        # Helper cleaning function:
        total_df['wins']=total_df.apply(wins, axis=1)
        
        return total_df
