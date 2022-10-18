import  numpy as np
import streamlit as st
import pandas as pd
def mostruns(data):
    batsman = data.groupby('striker').sum().sort_values('runs_off_bat',ascending= False)
    batsman_run = batsman['runs_off_bat'].reset_index()

    return batsman_run

def fours(data):
    fours_df = data[data['runs_off_bat'] == 4]
    most_fours_batsman = fours_df.groupby('striker')
    most_fours_batsman = most_fours_batsman['runs_off_bat'].sum().sort_values(ascending=False).reset_index()
    most_fours_batsman['runs_off_bat'] = (most_fours_batsman['runs_off_bat'] / 4).astype('int')
    most_fours_batsman = most_fours_batsman.rename(columns={'runs_off_bat':"4s"})

    return  most_fours_batsman

def six(data):
    six_df = data[data['runs_off_bat'] == 6]
    most_six_batsman = six_df.groupby('striker')
    most_six_batsman = most_six_batsman['runs_off_bat'].sum().sort_values(ascending=False).reset_index()
    most_six_batsman['runs_off_bat'] = (most_six_batsman['runs_off_bat'] / 6).astype('int')
    most_six_batsman= most_six_batsman.rename(columns={'runs_off_bat':"6s"})

    return most_six_batsman

def fifties(data):
    new_df = data.groupby(['match_id', 'striker'])['runs_off_bat'].sum().reset_index()
    fifties = new_df[(new_df['runs_off_bat'] >= 50) & (new_df['runs_off_bat'] < 100)]
    fifties.drop(columns=['match_id'], inplace=True)
    fifties = fifties.groupby('striker').count().sort_values('runs_off_bat', ascending=False)
    fifties = fifties.reset_index()
    fifties = fifties.rename(columns={'runs_off_bat':"50s"})

    return fifties

def hundred(data):
    new_df = data.groupby(['match_id', 'striker'])['runs_off_bat'].sum().reset_index()
    hundreds = new_df[(new_df['runs_off_bat'] >= 100)]
    hundreds.drop(columns=['match_id'], inplace=True)
    hundreds = hundreds.groupby('striker').count().sort_values('runs_off_bat', ascending=False)
    hundreds = hundreds.reset_index()

    return hundreds

def dotballs(data):
    dots_df = data[data['runs_off_bat'] == 0]
    dots_df=dots_df['striker'].value_counts().reset_index()

    return dots_df

def ducks(data):
    new_df = data.groupby(['match_id', 'striker'])['runs_off_bat'].sum().reset_index()
    new_df = new_df[new_df['runs_off_bat'] == 0]
    new_df.drop(columns=['match_id'], inplace=True)
    ducks_df = new_df.groupby('striker').count().sort_values('runs_off_bat', ascending=False)
    ducks_df= ducks_df.reset_index()

    return ducks_df
def highest(data):
    new_df = data.groupby(['match_id', 'striker'])['runs_off_bat'].sum().reset_index()
    new_df = new_df.drop(columns=['match_id'])
    new_df = new_df.sort_values('runs_off_bat', ascending=False)
    new_df = new_df.rename(columns={'runs_off_bat':"highest"})

    return highest

def highest_strike(data,most_runs):
    ball_faced = data[data['wides'] == 0].groupby('striker').count().sort_values('runs_off_bat', ascending=False)[
        'runs_off_bat'].reset_index()
    player = most_runs
    player = player.merge(ball_faced, left_on='striker', right_on='striker')
    player = player[player['runs_off_bat_y'] > 200]
    player = player.reset_index()
    player['strikerate'] = (player['runs_off_bat_x'] / player['runs_off_bat_y']) * 100
    player = player.sort_values('strikerate', ascending=False)
    player = player.reset_index()
    player = player.rename(columns={'runs_off_bat_x': 'runs', 'runs_off_bat_y': 'balls'})
    player=player.drop(columns=['runs','balls','level_0','index'])


    return player
def highest_strike_other(data,most_runs):
    ball_faced = data[data['wides'] == 0].groupby('striker').count().sort_values('runs_off_bat', ascending=False)[
        'runs_off_bat'].reset_index()
    player = most_runs
    player = player.merge(ball_faced, left_on='striker', right_on='striker')
    player = player[player['runs_off_bat_y'] > 50]
    player = player.reset_index()
    player['strikerate'] = (player['runs_off_bat_x'] / player['runs_off_bat_y']) * 100
    player = player.sort_values('strikerate', ascending=False)
    player = player.reset_index()
    player = player.rename(columns={'runs_off_bat_x': 'runs', 'runs_off_bat_y': 'balls'})
    player=player.drop(columns=['runs','balls','level_0','index'])


    return player

def highest_avg(data,mostruns):
    temp = data
    temp['count'] = 1
    temp = temp.groupby("player_dismissed").sum().reset_index()
    temp = temp.sort_values('count', ascending=False)
    temp = temp[['player_dismissed', 'count']]
    player = mostruns
    player = player.merge(temp, left_on='striker', right_on='player_dismissed')
    player = player[player['runs_off_bat'] > 500]
    player['bat_avg'] = (player['runs_off_bat'] / player['count'])
    top_avg = player.sort_values('bat_avg', ascending=False).reset_index()
    top_avg = top_avg[['striker', 'bat_avg']]

    return top_avg

def highest_avg_o(data,mostruns):
    temp = data
    temp['count'] = 1
    temp = temp.groupby("player_dismissed").sum().reset_index()
    temp = temp.sort_values('count', ascending=False)
    temp = temp[['player_dismissed', 'count']]
    player = mostruns
    player = player.merge(temp, left_on='striker', right_on='player_dismissed')
    player['bat_avg'] = (player['runs_off_bat'] / player['count'])
    top_avg = player.sort_values('bat_avg', ascending=False).reset_index()
    top_avg = top_avg[['striker', 'bat_avg']]

    return top_avg

def most_matches(data):
    playing11= data
    playing11 = playing11.groupby('Players')['Match_ID'].count()
    playing11 = pd.DataFrame({'Player': playing11.index, 'Matches': playing11.values})
    playing11 = playing11.sort_values('Matches', ascending=False).reset_index()
    playing11 = playing11.drop('index', axis=1)

    return playing11

def Highest_scores(data):
    new_df = data.groupby(['match_id', 'striker'])['runs_off_bat'].sum().reset_index()
    new_df = new_df.sort_values('runs_off_bat', ascending=False)
    new_df = new_df.reset_index()
    new_df = new_df.drop(columns=['match_id', 'index'])

    return new_df

def most_wickets(data):
    l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
    data_bowler = data[data['wicket_type'].isin(l)]
    data_bowler['wicket'] = 1
    bowler = data_bowler.groupby('bowler').sum()
    bowler = bowler['wicket'].sort_values(ascending=False).reset_index()

    return bowler

def highest_wickets(data):
    l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
    data_bowler = data[data['wicket_type'].isin(l)]
    data_bowler['wicket'] = 1
    df = data_bowler.groupby(['match_id', 'bowler']).count().reset_index()
    df = df[['bowler', 'wicket']]
    highest_wickets = df.sort_values('wicket', ascending=False).reset_index()
    highest_wickets = highest_wickets.drop('index', axis=1)

    return highest_wickets

def five_wicket(data):
    l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
    data_bowler = data[data['wicket_type'].isin(l)]
    data_bowler['wicket'] = 1
    data_bowler
    df = data_bowler.groupby(['match_id', 'bowler']).count().reset_index()
    df = df[['bowler', 'wicket']]
    df = df[df['wicket'] >= 5]
    five_w = df.groupby('bowler')['wicket'].count()
    five_w = pd.DataFrame({'bowler': five_w.index, 'wicket': five_w.values})
    five_w = five_w.sort_values('wicket', ascending=False).reset_index()
    five_w = five_w.drop('index', axis=1)

    return five_w

def most_wides(data):
    dots_df = data[(data['runs_off_bat'] == 0) & (data['wides'] > 0)]
    most_wides = dots_df['bowler'].value_counts().reset_index()

    return most_wides

def most_dots(data):
    dots_df = data[(data['runs_off_bat'] == 0) & ((data['wides'] > 0) | (data['legbyes'] > 0))]
    most_extras = dots_df['bowler'].value_counts().reset_index()
    df = data[(data['runs_off_bat'] == 0)]
    df = df['bowler'].value_counts()
    dot_wide = pd.DataFrame({'bowler': df.index, 'dot_wide': df.values})
    dot_wide = dot_wide.merge(most_extras, left_on='bowler', right_on='index')
    dot_wide['dots'] = dot_wide['dot_wide'] - dot_wide['bowler_y']
    dot_wide = dot_wide.sort_values('dots', ascending=False)
    dot_wide = dot_wide.drop(columns=['bowler_x', 'dot_wide', 'bowler_y'])

    return dot_wide

def economic_bowler(data):
    byes = data[(data['extras'] > 0) & (data['byes'] > 0)]
    legbyes = data[(data['extras'] > 0) & (data['legbyes'] > 0)]

    byes_run = byes.groupby('bowler').sum().sort_values('extras', ascending=False)['extras']
    byes_run = pd.DataFrame({'bowler': byes_run.index, 'byes': byes_run.values})
    legbyes_run = legbyes.groupby('bowler').sum().sort_values('extras', ascending=False)['extras']
    legbyes_run = pd.DataFrame({'bowler': legbyes_run.index, 'legbyes': legbyes_run.values})
    wides = data[(data['extras'] > 0) & (data['wides'] > 0)]
    wides_run = wides.groupby('bowler').sum().sort_values('extras', ascending=False)['extras']
    wides_run = pd.DataFrame({'bowler': wides_run.index, 'wides': wides_run.values})
    noball = data[(data['extras'] > 0) & (data['noballs'] > 0)]
    noball_run = noball.groupby('bowler').sum().sort_values('extras', ascending=False)['extras']
    noball_run = pd.DataFrame({'bowler': noball_run.index, 'noball_run': noball_run.values})
    batrun = data[(data['runs_off_bat'] > 0)]
    batrun = batrun.groupby('bowler').sum().sort_values('runs_off_bat', ascending=False)['runs_off_bat']
    batrun = pd.DataFrame({'bowler': batrun.index, 'batrun': batrun.values})
    bowlers = wides_run.merge(byes_run, left_on='bowler', right_on='bowler', how='left')
    bowlers = bowlers.merge(legbyes_run, left_on='bowler', right_on='bowler', how='left')
    bowlers = bowlers.merge(noball_run, left_on='bowler', right_on='bowler', how='left')
    bowlers = bowlers.merge(batrun, left_on='bowler', right_on='bowler', how='right')
    bowlers = bowlers.fillna(0)
    bowlers['extras_runs'] = bowlers['wides'] + bowlers['byes'] + bowlers['legbyes'] + bowlers['noball_run']
    bowlers['total_runs'] = bowlers['batrun'] + bowlers['extras_runs']
    bowlers = bowlers.sort_values('total_runs', ascending=False).reset_index()
    bowlers = bowlers.drop('index', axis=1)
    balls = data[(data['wides'] == 0) & (data['penalty'] == 0) & (data['byes'] == 0)].groupby('bowler').count()[
        'match_id']
    overs = balls / 6
    overs = pd.DataFrame({'bowler': overs.index, 'overs': overs.values})
    bowlers = bowlers.merge(overs, left_on='bowler', right_on='bowler', how='right')
    bowlers = bowlers.fillna(0)
    bowlers_a = bowlers[bowlers['overs'] > 50]
    bowlers_a['economy'] = bowlers_a['total_runs'] / bowlers_a['overs']
    bowlers_a = bowlers_a.sort_values('economy')
    economic = bowlers_a[['bowler', 'economy']].reset_index()
    economic = economic.drop('index', axis=1).reset_index()

    #most overs
    overs = overs.sort_values('overs', ascending=False)
    overs["overs"] = overs["overs"].astype('int')
    overs = overs.reset_index()
    overs = overs.drop('index', axis=1)



    return economic,overs
def economic_bowler_o(data):
    byes = data[(data['extras'] > 0) & (data['byes'] > 0)]
    legbyes = data[(data['extras'] > 0) & (data['legbyes'] > 0)]

    byes_run = byes.groupby('bowler').sum().sort_values('extras', ascending=False)['extras']
    byes_run = pd.DataFrame({'bowler': byes_run.index, 'byes': byes_run.values})
    legbyes_run = legbyes.groupby('bowler').sum().sort_values('extras', ascending=False)['extras']
    legbyes_run = pd.DataFrame({'bowler': legbyes_run.index, 'legbyes': legbyes_run.values})
    wides = data[(data['extras'] > 0) & (data['wides'] > 0)]
    wides_run = wides.groupby('bowler').sum().sort_values('extras', ascending=False)['extras']
    wides_run = pd.DataFrame({'bowler': wides_run.index, 'wides': wides_run.values})
    noball = data[(data['extras'] > 0) & (data['noballs'] > 0)]
    noball_run = noball.groupby('bowler').sum().sort_values('extras', ascending=False)['extras']
    noball_run = pd.DataFrame({'bowler': noball_run.index, 'noball_run': noball_run.values})
    batrun = data[(data['runs_off_bat'] > 0)]
    batrun = batrun.groupby('bowler').sum().sort_values('runs_off_bat', ascending=False)['runs_off_bat']
    batrun = pd.DataFrame({'bowler': batrun.index, 'batrun': batrun.values})
    bowlers = wides_run.merge(byes_run, left_on='bowler', right_on='bowler', how='left')
    bowlers = bowlers.merge(legbyes_run, left_on='bowler', right_on='bowler', how='left')
    bowlers = bowlers.merge(noball_run, left_on='bowler', right_on='bowler', how='left')
    bowlers = bowlers.merge(batrun, left_on='bowler', right_on='bowler', how='right')
    bowlers = bowlers.fillna(0)
    bowlers['extras_runs'] = bowlers['wides'] + bowlers['byes'] + bowlers['legbyes'] + bowlers['noball_run']
    bowlers['total_runs'] = bowlers['batrun'] + bowlers['extras_runs']
    bowlers = bowlers.sort_values('total_runs', ascending=False).reset_index()
    bowlers = bowlers.drop('index', axis=1)
    balls = data[(data['wides'] == 0) & (data['penalty'] == 0) & (data['byes'] == 0)].groupby('bowler').count()[
        'match_id']
    overs = balls / 6
    overs = pd.DataFrame({'bowler': overs.index, 'overs': overs.values})
    bowlers = bowlers.merge(overs, left_on='bowler', right_on='bowler', how='right')
    bowlers = bowlers.fillna(0)
    bowlers_a = bowlers[bowlers['overs'] > 5]
    bowlers_a['economy'] = bowlers_a['total_runs'] / bowlers_a['overs']
    bowlers_a = bowlers_a.sort_values('economy')
    economic = bowlers_a[['bowler', 'economy']].reset_index()
    economic = economic.drop('index', axis=1).reset_index()

    #most overs
    overs = overs.sort_values('overs', ascending=False)
    overs["overs"] = overs["overs"].astype('int')
    overs = overs.reset_index()
    overs = overs.drop('index', axis=1)



    return economic,overs


def over_generator(data):
    for x in range(data.shape[0]):
        for i in range(20):
            if i < data['ball'][x] < i + 1:
                data['over'][x] = i + 1
    return data

def most_win_run_batsman(data,match):
    data = data.merge(match, left_on='match_id', right_on='match_id')
    data = data[data['batting_team'] == data['winner']]
    batsman = data.groupby('striker').sum().sort_values('runs_off_bat', ascending=False)
    batsman_run = batsman['runs_off_bat'].reset_index()

    return batsman_run

def empty_check(data):
    if data.empty:
        return 0
    else:
        return data

def runs_perseason(data,team):
    data['runs'] = data['runs_off_bat'] + data['extras']
    bat = data[data['batting_team'] == team]
    bat_r = bat.groupby(['season', 'innings']).sum().reset_index()
    bat_r['innings'] = bat_r['innings'].astype('string')

    return bat_r

def wickets_seasons(data,team):
    l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
    ball = data[data['bowling_team'] == team]
    data_b = ball[ball['wicket_type'].isin(l)]
    data_b['wicket'] = 1
    ball_b = data_b.groupby(['season', 'innings']).sum().reset_index()
    ball_b['innings'] = ball_b['innings'].astype('string')
    return ball_b

def total_match_per_season(data,match,team):
    data = data.merge(match,left_on='match_id',right_on='match_id')
    data = data[(data['batting_team'] == team) | (data['bowling_team'] == team)]
    t_s = data['season_x'].unique()
    total_m = [0] * t_s.shape[0]
    for x in range(t_s.shape[0]):
        total_m[x] = data[data['season_x'] == t_s[x]]['match_id'].unique().shape[0]

    total_m_w = [0] * t_s.shape[0]
    for x in range(t_s.shape[0]):
        total_m_w[x] = data[(data['season_x'] == t_s[x]) & (data['winner']==team)]['match_id'].unique().shape[0]


    return total_m,total_m_w,t_s

def team_highest_scorers(data,team):
    data['runs'] = data['runs_off_bat'] + data['extras']
    bat = data[data['batting_team'] == team]

    # inning1
    bat_r1 = bat[bat['innings'] == 1]
    bat_r1 = bat_r1.groupby(['striker']).sum()
    bat_r1 = bat_r1.sort_values('runs', ascending=False).reset_index()

    # inning1
    bat_r2 = bat[bat['innings'] == 2]
    bat_r2 = bat_r2.groupby(['striker']).sum()
    bat_r2 = bat_r2.sort_values('runs', ascending=False).reset_index()

    # overall
    bat_r = bat.groupby(['striker']).sum()
    bat_r = bat_r.sort_values('runs', ascending=False).reset_index()
    bat_r = bat_r.merge(bat_r1, left_on='striker', right_on='striker')
    bat_r = bat_r.merge(bat_r2, left_on='striker', right_on='striker')
    bat_r
    return bat_r

def team_highest_deathover_run_scorer(data,team):
    data['runs'] = data['runs_off_bat'] + data['extras']
    data_p = data[data['over'] >15 ]
    bat = data_p[data_p['batting_team'] == team]

    # inning1
    bat_r1 = bat[bat['innings'] == 1]
    bat_r1 = bat_r1.groupby(['striker']).sum()
    bat_r1 = bat_r1.sort_values('runs', ascending=False).reset_index()

    # inning1
    bat_r2 = bat[bat['innings'] == 2]
    bat_r2 = bat_r2.groupby(['striker']).sum()
    bat_r2 = bat_r2.sort_values('runs', ascending=False).reset_index()

    # overall
    bat_r = bat.groupby(['striker']).sum()
    bat_r = bat_r.sort_values('runs', ascending=False).reset_index()
    bat_r = bat_r.merge(bat_r1, left_on='striker', right_on='striker')
    bat_r = bat_r.merge(bat_r2, left_on='striker', right_on='striker')
    bat_r
    return bat_r

def team_highest_middleover_run_scorer(data,team):
    data['runs'] = data['runs_off_bat'] + data['extras']
    data_p = data[(data['over']<=15) & (data['over']>6)]
    bat = data_p[data_p['batting_team'] == team]

    # inning1
    bat_r1 = bat[bat['innings'] == 1]
    bat_r1 = bat_r1.groupby(['striker']).sum()
    bat_r1 = bat_r1.sort_values('runs', ascending=False).reset_index()

    # inning1
    bat_r2 = bat[bat['innings'] == 2]
    bat_r2 = bat_r2.groupby(['striker']).sum()
    bat_r2 = bat_r2.sort_values('runs', ascending=False).reset_index()

    # overall
    bat_r = bat.groupby(['striker']).sum()
    bat_r = bat_r.sort_values('runs', ascending=False).reset_index()
    bat_r = bat_r.merge(bat_r1, left_on='striker', right_on='striker')
    bat_r = bat_r.merge(bat_r2, left_on='striker', right_on='striker')
    bat_r
    return bat_r

def team_top_wicket_taker(data,team):
    # Top wicket takers
    l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
    ball = data[data['bowling_team'] == team]
    data_b = ball[ball['wicket_type'].isin(l)]
    data_b['wicket'] = 1
    # inning1
    ball_r1 = data_b[data_b['innings'] == 1]
    ball_r1 = ball_r1.groupby(['bowler']).sum()
    ball_r1 = ball_r1.sort_values('wicket', ascending=False).reset_index()

    # inning2
    ball_r2 = data_b[data_b['innings'] == 2]
    ball_r2 = ball_r2.groupby(['bowler']).sum()
    ball_r2 = ball_r2.sort_values('wicket', ascending=False).reset_index()

    # overall
    ball_r = data_b.groupby(['bowler']).sum()
    ball_r = ball_r.sort_values('wicket', ascending=False).reset_index()
    ball_r = ball_r.merge(ball_r1, left_on='bowler', right_on='bowler')
    ball_r = ball_r.merge(ball_r2, left_on='bowler', right_on='bowler')

    return ball_r

def team_top_wicket_taker_in_powerplay(data,team):
    # Top wicket takers
    l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
    data_bp = data[data['over'] < 7]
    ball = data_bp[data_bp['bowling_team'] == team]
    data_b = ball[ball['wicket_type'].isin(l)]
    data_b['wicket'] = 1
    # batting team data
    # inning1
    ball_r1 = data_b[data_b['innings'] == 1]
    ball_r1 = ball_r1.groupby(['bowler']).sum()
    ball_r1 = ball_r1.sort_values('wicket', ascending=False).reset_index()

    # inning2
    ball_r2 = data_b[data_b['innings'] == 2]
    ball_r2 = ball_r2.groupby(['bowler']).sum()
    ball_r2 = ball_r2.sort_values('wicket', ascending=False).reset_index()

    # overall
    ball_r = data_b.groupby(['bowler']).sum()
    ball_r = ball_r.sort_values('wicket', ascending=False).reset_index()
    ball_r = ball_r.merge(ball_r1, left_on='bowler', right_on='bowler')
    ball_r = ball_r.merge(ball_r2, left_on='bowler', right_on='bowler')

    return ball_r

def team_top_wicket_taker_in_Middleover(data,team):
    # Top wicket takers
    l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
    data_bp = data[(data['over']<=15) & (data['over']>6)]
    ball = data_bp[data_bp['bowling_team'] == team]
    data_b = ball[ball['wicket_type'].isin(l)]
    data_b['wicket'] = 1
    # batting team data
    # inning1
    ball_r1 = data_b[data_b['innings'] == 1]
    ball_r1 = ball_r1.groupby(['bowler']).sum()
    ball_r1 = ball_r1.sort_values('wicket', ascending=False).reset_index()

    # inning2
    ball_r2 = data_b[data_b['innings'] == 2]
    ball_r2 = ball_r2.groupby(['bowler']).sum()
    ball_r2 = ball_r2.sort_values('wicket', ascending=False).reset_index()

    # overall
    ball_r = data_b.groupby(['bowler']).sum()
    ball_r = ball_r.sort_values('wicket', ascending=False).reset_index()
    ball_r = ball_r.merge(ball_r1, left_on='bowler', right_on='bowler')
    ball_r = ball_r.merge(ball_r2, left_on='bowler', right_on='bowler')

    return ball_r

def team_top_wicket_taker_in_Death(data,team):
    # Top wicket takers
    l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
    data_bp = data[(data['over']<=15) & (data['over']>6)]
    ball = data_bp[data_bp['bowling_team'] == team]
    data_b = ball[ball['wicket_type'].isin(l)]
    data_b['wicket'] = 1
    # batting team data
    # inning1
    ball_r1 = data_b[data_b['innings'] == 1]
    ball_r1 = ball_r1.groupby(['bowler']).sum()
    ball_r1 = ball_r1.sort_values('wicket', ascending=False).reset_index()

    # inning2
    ball_r2 = data_b[data_b['innings'] == 2]
    ball_r2 = ball_r2.groupby(['bowler']).sum()
    ball_r2 = ball_r2.sort_values('wicket', ascending=False).reset_index()

    # overall
    ball_r = data_b.groupby(['bowler']).sum()
    ball_r = ball_r.sort_values('wicket', ascending=False).reset_index()
    ball_r = ball_r.merge(ball_r1, left_on='bowler', right_on='bowler')
    ball_r = ball_r.merge(ball_r2, left_on='bowler', right_on='bowler')

    return ball_r

def team_highest_avg_score_grounds(data,match,venue,team):
    data = data[data['bowling_team'] == team]
    data['runs'] = data['runs_off_bat'].fillna(0) + data['extras'].fillna(0)
    data = data.merge(match, left_on='match_id', right_on='match_id')
    G = data.groupby('venueID')['runs'].sum().reset_index()
    G = G.sort_values('runs').reset_index()
    G = G.drop('index', axis=1)
    G = G.merge(venue, left_on="venueID", right_on='id')
    M = data.drop_duplicates('match_id')
    M = M.groupby('venueID')['match_id'].count().reset_index()
    M = M.sort_values('match_id').reset_index()
    M = M.drop('index', axis=1)
    G = G.merge(M, left_on='venueID', right_on='venueID')
    G['stadium'] = G['venue'] + '(' + G['city'] + ')'
    G['Average'] = (G['runs'] / G['match_id']).astype('int')
    temp = G.sort_values('Average').reset_index()
    temp = temp.drop('index', axis=1)

    return temp,G
