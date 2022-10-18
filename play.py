import  numpy as np
import streamlit as st
import pandas as pd

def highest_runs(data,match,venue):
    temp = data.groupby('match_id').sum().sort_values('runs_off_bat', ascending=False).reset_index()
    most_runs = temp[['match_id', 'runs_off_bat']]
    most_runs = most_runs.merge(match, left_on='match_id', right_on='match_id')

    most_runs = most_runs.merge(data, left_on='match_id', right_on=['match_id'])
    most_runs = most_runs.drop_duplicates(subset=['match_id'])
    most_runs['wicket_type'].fillna('Not Out', inplace=True)
    most_runs = most_runs.merge(venue, left_on='venueID', right_on='id')
    highest_runs = most_runs
    highest_runs = highest_runs.rename(
        columns={'runs_off_bat_x': 'Run', 'batting_team': 'Batting Team', 'bowling_team': 'Bowling Team',
                 'winner_y': 'Winner', 'winner_type_y': 'Win Type', 'season_x': 'Season',
                 'wicket_type': 'Dismissal Type', 'bowler': 'Dismissed By'})
    temp = highest_runs.drop(columns=['venueID', 'win_by', 'id'])
    highest_runs = highest_runs.drop(
        columns=['match_id', 'venueID', 'win_by', 'id', 'balls_per_over', 'team1', 'team2', 'gender'
            , 'date', 'event', 'match_number', 'toss_winner', 'toss_decision', 'player_of_match', 'winner',
                 'winner', 'winner_type', 'outcome', 'eliminator', 'method', 'date1', 'date2', 'Unnamed: 0', 'season_y'
            , 'innings', 'ball', 'striker', 'non_striker', 'runs_off_bat_y', 'extras', 'wides', 'noballs', 'byes',
                 'legbyes', 'penalty', 'player_dismissed','other_player_dismissed', 'other_wicket_type', 'striker_id', 'non_striker_id',
                 'bowler_id', 'over'])
    for x in range(highest_runs.shape[0]):
        if highest_runs['Dismissal Type'][x] == 'Not Out':
            highest_runs['Dismissed By'][x] = 'None'

    highest_runs = highest_runs.sort_values('Run', ascending=False).reset_index()
    highest_runs = highest_runs.drop('index', axis=1)

    return highest_runs

def highest_run_agains_bolltype(data,players):
    most_favboll = data.merge(players, left_on='bowler', right_on='Name')
    most_favboll['count'] = 1
    most_favboll = most_favboll.groupby('Bowling Style').sum().reset_index()
    most_favboll['boll_type_avg'] = ((most_favboll['runs_off_bat'] / most_favboll['count']) * 100).astype('int')
    most_favboll = most_favboll.sort_values('boll_type_avg', ascending=False).reset_index()

    return most_favboll

def most_out_against(data,players):
    l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
    data_bowler = data.merge(players, left_on='bowler', right_on='Name')
    data_bowler = data_bowler[data_bowler['wicket_type'].isin(l)]
    data_bowler['wicket'] = 1
    total_outs = data_bowler.shape[0]
    bowler = data_bowler.groupby('Bowling Style').sum()
    bowler = bowler.sort_values('wicket', ascending=False).reset_index()
    bowler['Out Percentage'] = ((bowler['wicket'] / total_outs) * 100).astype('int')

    return bowler