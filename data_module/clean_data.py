def wins(r):
    if r['winner'] == 'DRAW':
        return 'D'
    if r['winner'] == 'HOME_TEAM':
        if r['home_team_code'] == 'BVB':
            return 'W'
        return 'L'
    if r['winner'] == 'AWAY_TEAM':
        if r['away_team_code'] == 'BVB':
            return 'W'
        return 'L'