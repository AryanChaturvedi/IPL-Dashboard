import streamlit as st
import pandas as pd
import altair as alt
import helper, play
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import plotly.graph_objects as go

# CSS to inject contained in a string
hide_table_row_index = """
                        <style>
                        thead tr th:first-child {display:none}
                        tbody th {display:none}
                        </style>
                        """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.write(
    """
                <style type="text/css" media="screen">
                div[role="listbox"] ul {
                    height:300px;
                }
                </style>
                """
    ,
    unsafe_allow_html=True,
)

data = pd.read_csv('deliveries.csv')
venue = pd.read_csv('venue.csv')
players = pd.read_csv('players_info_with_keys.csv')
match = pd.read_csv('match_details.csv')
playing11 = pd.read_csv('playing_11.csv')
data.drop_duplicates(inplace=True)
data[['extras', 'wides', 'noballs', 'byes', 'legbyes', 'penalty']] = data[
    ['extras', 'wides', 'noballs', 'byes', 'legbyes', 'penalty']].fillna(0).astype('int')

st.sidebar.title('IPL Analysis')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Overall Analysis', 'Season-Wise-Analysis', 'Player-wise-analysis', 'Team-wise-analysis')
)

if user_menu == 'Overall Analysis':
    st.sidebar.header("Overall Analysis")
    selected_type = st.sidebar.selectbox('Select Type', ['Batting', 'Bowling', 'Overall'])

    if selected_type == 'Batting':
        st.title('Overall Batting Statistics')

        batsman_runs = helper.mostruns(data)
        total_runs = batsman_runs['runs_off_bat'].sum()

        most_fours_batsman = helper.fours(data)
        total_fours = most_fours_batsman['4s'].sum()

        most_six_batsman = helper.six(data)
        total_six = most_six_batsman['6s'].sum()

        most_fifties_batsman = helper.fifties(data)
        total_fifties = most_fifties_batsman['50s'].sum()

        most_hundred_batsman = helper.hundred(data)
        total_hundred = most_hundred_batsman['runs_off_bat'].sum()

        most_dots_batsman = helper.dotballs(data)
        total_dots = most_dots_batsman['striker'].sum()

        most_duck_batsman = helper.ducks(data)
        total_ducks = most_duck_batsman['runs_off_bat'].sum()

        highest_score_batsman = helper.Highest_scores(data)
        highest_score = highest_score_batsman['runs_off_bat'][0]

        highest_runs_batsman = helper.highest(data)

        highest_strikerate = helper.highest_strike(data, batsman_runs)
        highest_avg = helper.highest_avg(data, batsman_runs)
        most_MOM = match['player_of_match'].value_counts().reset_index()
        most_matches = helper.most_matches(playing11)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total Runs')
            st.subheader(total_runs)
        with col2:
            st.header('Total 4s')
            st.subheader(total_fours)
        with col3:
            st.header('Total 6s')
            st.subheader(total_six)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total 50s')
            st.subheader(total_fifties)
        with col2:
            st.header('Total 100s')
            st.subheader(total_hundred)
        with col3:
            st.header('Highest Run(player)')
            st.subheader(highest_score)

        st.header('Top 10 List')

        top_list_batsman = ["Most Runs", 'Most 4s', 'Most 6s', 'Most 50s', 'Most 100s', 'Highest Batsman Score',
                            'Most Ducks', 'Highest Strikerate', 'Highest Average', 'Most Man of the Match',
                            'Most Dotball Played', 'Most Matches Played']
        top_list_selected = st.selectbox('Select Top 10 List', top_list_batsman)

        if top_list_selected == "Most Runs":
            data_selected = batsman_runs.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', 'runs_off_bat': 'y'})
        if top_list_selected == 'Most 4s':
            data_selected = most_fours_batsman.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', '4s': 'y'})
        if top_list_selected == 'Most 6s':
            data_selected = most_six_batsman.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', '6s': 'y'})
        if top_list_selected == 'Most 50s':
            data_selected = most_fifties_batsman.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', '50s': 'y'})
        if top_list_selected == 'Most 100s':
            data_selected = most_hundred_batsman.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', 'runs_off_bat': 'y'})
        if top_list_selected == 'Most Ducks':
            data_selected = most_duck_batsman.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', 'runs_off_bat': 'y'})
        if top_list_selected == 'Highest Strikerate':
            data_selected = highest_strikerate.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', 'strikerate': 'y'})
        if top_list_selected == 'Most Dotball Played':
            data_selected = most_dots_batsman.head(10)
            data_selected = data_selected.rename(columns={'index': 'Batsman', 'striker': 'y'})
        if top_list_selected == 'Highest Average':
            data_selected = highest_avg.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', 'bat_avg': 'y'})
        if top_list_selected == 'Most Man of the Match':
            data_selected = most_MOM.head(10)
            data_selected = data_selected.rename(columns={'index': 'Batsman', 'player_of_match': 'y'})
        if top_list_selected == 'Most Matches Played':
            data_selected = most_matches.head(10)
            data_selected = data_selected.rename(columns={'Player': 'Batsman', 'Matches': 'y'})
        if top_list_selected == 'Highest Batsman Score':
            data_selected = highest_score_batsman.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', 'runs_off_bat': 'y'})

        fig, ax = plt.subplots()
        col1, col2 = st.columns([1, 3])
        with col2:
            ax.bar(data_selected['Batsman'], data_selected['y'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col1:
            st.table(data_selected)

        # ------Runs per Overs--------

        data['runs'] = data['runs_off_bat'].fillna(0) + data['extras'].fillna(0) + data['wides'].fillna(0)
        run_per_over = data.groupby('over')['runs'].sum().reset_index()
        runs_per_over_inn1 = data[data['innings'] == 1].groupby('over')['runs'].sum().reset_index()
        runs_per_over_inn2 = data[data['innings'] == 2].groupby('over')['runs'].sum().reset_index()
        x = runs_per_over_inn1.merge(runs_per_over_inn2, left_on='over', right_on='over')
        x = run_per_over.merge(x, left_on='over', right_on='over')
        x.rename(columns={'runs_x': 'Inning_1', 'runs_y': 'Inning_2', 'runs': 'Total Run'}, inplace=True)
        fig = px.line(x, x='over', y=['Inning_1', 'Inning_2', 'Total Run'])
        # fig.update_layout(autosize=False, width=800, height=600)
        st.header('Runs Per Over(Overall Total)')
        st.plotly_chart(fig)
        st.caption('click on top right variables to filter graphs.')
        """
                * Teams scores more in first inning than second.
                * Sudden fall in runs scored in 6th and 7th overs is because of Powerplay end.
        """

        st.header('Effect of Toss Wins and First Bat/Field ')
        x_labels = ['Toss Winner', 'Toss Looser']
        fig = go.Figure(data=[
            go.Bar(name='Total Wins', x=x_labels, y=[483, 467]),
            go.Bar(name='First Bat Win', x=x_labels, y=[156, 195]),
            go.Bar(name='First Field Win', x=x_labels, y=[327, 272])
        ])
        fig.update_layout(barmode='group', width=800, height=600)
        st.plotly_chart(fig)
        st.caption('click on top right variables to filter graphs.')
        st.markdown(
            "- Toss winning team has won more matches than toss loosing team. Winning the toss gives extra edge on match win.")
        st.markdown("- Most of the toss winning teams who won the matches has opted to field first.")

        st.header('Best Finishers')
        st.markdown('- Most runs scored by batsman in death overs(16-20)')
        do = data[data['over'] > 15].groupby('striker').sum().sort_values('runs_off_bat', ascending=False)
        do = do['runs_off_bat'].reset_index()
        fig = go.Figure([go.Bar(x=do['striker'].head(10), y=do["runs_off_bat"].head(10))])
        st.plotly_chart(fig)



        st.header('Best batsman giving good start')
        st.markdown('- Most runs scored by batsman in Starting overs(0-10)')
        so = data[data['over'] < 11].groupby('striker').sum().sort_values('runs_off_bat', ascending=False)
        so = so['runs_off_bat'].reset_index()
        fig = go.Figure([go.Bar(x=so['striker'].head(10), y=so["runs_off_bat"].head(10))])
        st.plotly_chart(fig)

        st.header('Highest Deathover Strikerate')
        hs = helper.highest_strike(data[data['over'] > 15], do)
        fig = go.Figure([go.Bar(x=hs['striker'].head(10), y=hs["strikerate"].head(10))])
        st.plotly_chart(fig)

        eo = data[data['over'] < 6].groupby('striker').sum().sort_values('runs_off_bat', ascending=False)
        eo = eo['runs_off_bat'].reset_index()

        st.header('Highest 5overs vs 10overs Runs')
        x_labels = eo['striker'].head(10)
        temp = so[so['striker'].isin(eo['striker'])]
        percent = so[so['striker'].isin(eo['striker'])]
        percent["runs_off_bat"] = ((temp["runs_off_bat"] - eo["runs_off_bat"]) / eo["runs_off_bat"]) * 1000
        fig = go.Figure(data=[
            go.Bar(name='5-Over Run', x=x_labels, y=eo["runs_off_bat"].head(10)),
            go.Bar(name='10-Over Run', x=x_labels, y=temp["runs_off_bat"].head(10)),
            go.Bar(name='% Increase*10', x=x_labels, y=percent["runs_off_bat"].head(10))
        ])
        fig.update_layout(barmode='group', width=800, height=600)
        st.plotly_chart(fig)
        st.caption('click on top right variables to filter graphs.')
        st.markdown(
            '- Sikhar Dhawan has scored highest Runs in both 5 and 10 overs. It shows he is very good at wickets once he playes for more than5 overs')
        st.markdown(
            '- Q de Kock has highest % increase From 5-overs to 10-Overs runs followed by Virat Kohli. This shows that these players first save their wickets for initial overs then gradually increases their runrate.')

        # Most runs for winning cause

        w_runs = helper.most_win_run_batsman(data, match)
        fig = go.Figure([go.Bar(x=w_runs['striker'].head(10), y=w_runs["runs_off_bat"].head(10))])
        st.header('Most runs scored in winning cause')
        st.plotly_chart(fig)
        st.markdown(
            '- Thses are top batsman whose performance highly affects win-loss for their teams.')

    # ------------Bowling-----------------

    if selected_type == 'Bowling':
        st.title('Overall Bowling Statistics')

        most_wickets = helper.most_wickets(data)
        total_wickets = most_wickets['wicket'].sum()

        highest_wicket_bowler = helper.highest_wickets(data)
        highest_wicket = highest_wicket_bowler['wicket'][0]

        five_w_bowler = helper.five_wicket(data)
        total_5w = five_w_bowler['wicket'].sum()

        most_wides = helper.most_wides(data)
        total_wides = most_wides['bowler'].sum()

        most_dots = helper.most_dots(data)
        total_dots_balls = most_dots['dots'].sum()

        most_economic, most_overs = helper.economic_bowler(data)

        # ---------------Temp-------------
        most_duck_batsman = helper.ducks(data)
        total_ducks = most_duck_batsman['runs_off_bat'].sum()
        # ---------------Temp-------------

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total Wickets')
            st.subheader(total_wickets)
        with col2:
            st.header('Highest Wickets')
            st.subheader(highest_wicket)
        with col3:
            st.header('Total 5+ Wickets')
            st.subheader(total_5w)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total Wides')
            st.subheader(total_wides)
        with col2:
            st.header('Total Dots')
            st.subheader(total_dots_balls)
        with col3:
            st.header('Total Ducks')
            st.subheader(total_ducks)

        st.header('Top 10 List')

        top_list_bowler = ["Most Wickets", 'Most Economic Bowler', 'Highest Wickets', '5 or More Wicket Taker',
                           'Most Dot balls', 'Most No of Wide Balls', 'Highest no of Overs Bowled']
        top_list_selected = st.selectbox('Select Top 10 List', top_list_bowler)

        if top_list_selected == "Most Wickets":
            data_selected = most_wickets.head(10)
            data_selected = data_selected.rename(columns={'bowler': 'Bowler', 'wicket': 'y'})
        if top_list_selected == 'Highest Wickets':
            data_selected = highest_wicket_bowler.head(10)
            data_selected = data_selected.rename(columns={'bowler': 'Bowler', 'wicket': 'y'})
        if top_list_selected == '5 or More Wicket Taker':
            data_selected = five_w_bowler.head(10)
            data_selected = data_selected.rename(columns={'bowler': 'Bowler', 'wicket': 'y'})
        if top_list_selected == 'Most No of Wide Balls':
            data_selected = most_wides.head(10)
            data_selected = data_selected.rename(columns={'index': 'Bowler', 'bowler': 'y'})
        if top_list_selected == 'Most Dot balls':
            data_selected = most_dots.head(10)
            data_selected = data_selected.rename(columns={'index': 'Bowler', 'dots': 'y'})
        if top_list_selected == 'Most Economic Bowler':
            data_selected = most_economic.head(10)
            data_selected = data_selected.rename(columns={'bowler': 'Bowler', 'economy': 'y'})
        if top_list_selected == 'Highest no of Overs Bowled':
            data_selected = most_overs.head(10)
            data_selected = data_selected.rename(columns={'bowler': 'Bowler', 'overs': 'y'})

        fig, ax = plt.subplots()
        col1, col2 = st.columns([1, 3])
        with col2:
            ax.bar(data_selected['Bowler'], data_selected['y'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col1:
            st.table(data_selected)

        fall_of_wickets = data.groupby('over')['wicket_type'].count().reset_index()
        fall_of_wickets1 = data[data['innings'] == 1].groupby('over')['wicket_type'].count().reset_index()
        fall_of_wickets2 = data[data['innings'] == 2].groupby('over')['wicket_type'].count().reset_index()
        fall_of_wickets = fall_of_wickets.merge(fall_of_wickets1, left_on='over', right_on='over')
        fall_of_wickets = fall_of_wickets.merge(fall_of_wickets2, left_on='over', right_on='over')
        fall_of_wickets = fall_of_wickets.rename(
            columns={'wicket_type_x': 'Total', 'wicket_type_y': 'Inning_1', 'wicket_type': 'Inning_2'})
        fig = px.line(fall_of_wickets, x='over', y=['Inning_1', 'Inning_2', 'Total'])
        st.header('Fall of Wickets per overs')
        st.plotly_chart(fig)
        st.caption('click on top right variables to filter graphs.')
        st.markdown(
            '- Most teams looses their early wickets in 4-5th over, may be because of powerplay rush of making runs.')
        st.markdown(
            '- First batting team looses more wickets,with exponential fall at death overs.')
        st.markdown(
            '- Chasing teams most of the times saves their wickets because they do not want to loose their set batsman.')

        #total wickets
        l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
        data_bowler = data.merge(players, left_on='bowler', right_on='Name')
        data_bowler = data_bowler[data_bowler['wicket_type'].isin(l)]
        data_bowler['wicket'] = 1
        st.header('Total Wickets per Season')
        data_bowler = data_bowler.groupby('season').sum().reset_index()
        data_bowler = data_bowler.sort_values('wicket', ascending=False).reset_index()
        x = data_bowler['season']
        y = data_bowler['wicket']
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.plotly_chart(fig)
        # Wickets taken on Different Grounds
        st.header('Wickets taken on Different Grounds')
        l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
        data_bowler = data.merge(players, left_on='bowler', right_on='Name')
        data_bowler = data_bowler[data_bowler['wicket_type'].isin(l)]
        data_bowler['wicket'] = 1
        w_groundsd = data_bowler.merge(match, left_on='match_id', right_on='match_id')
        w_groundsd = w_groundsd.groupby('venueID').sum().sort_values('wicket', ascending=False).reset_index().head(
            10)
        w_groundsd = w_groundsd.merge(venue, left_on='venueID', right_on='id')
        venues = w_groundsd['venue']
        w_groundsd = w_groundsd[w_groundsd['venue'].isin(venues)]
        fig = go.Figure(data=[go.Bar(
            x=w_groundsd['venue'], y=w_groundsd['wicket'],
            text=y,
            textposition='auto',
        )])
        st.plotly_chart(fig)
        st.markdown('- Highest Number of matches is played on Wankhede Stadium.')


    if selected_type == 'Overall':
        st.title('Overall Statistics')
        players = players.drop_duplicates()
        total_players = players.shape[0]

        # total batsman
        pp = ['Top order Batter', 'Middle order Batter', 'Opening Batter']
        batsman = players[players['Playing Position'].isin(pp)]
        total_batsman = batsman.shape[0]

        # total bowlers
        bowlers = players[players['Playing Position'] == 'Bowler']
        total_bowler = bowlers.shape[0]

        # total allrounders
        pa = ['Allrounder', 'Bowling Allrounder', 'Batting Allrounder']
        allrounders = players[players['Playing Position'].isin(pa)]
        total_allrounders = allrounders.shape[0]

        # total wicketkeepr
        pw = ['Wicketkeeper', 'Wicketkeeper Batter']
        total_Wicketkeeper = players[players['Playing Position'].isin(pw)].shape[0]
        # total seasons
        total_seasons = match['season'].value_counts().shape[0]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total Players')
            st.subheader(total_players)
        with col2:
            st.header('Total Batsman')
            st.subheader(total_batsman)
        with col3:
            st.header('Total Bowlers')
            st.subheader(total_bowler)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total Allrounders')
            st.subheader(total_allrounders)
        with col2:
            st.header('Total Wicketkeeper')
            st.subheader(total_Wicketkeeper)
        with col3:
            st.header('Total Seasons')
            st.subheader(total_seasons)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total Matches')
            st.subheader(match.drop_duplicates().shape[0])
        with col2:
            st.header('Total Venue')
            st.subheader(venue.drop_duplicates().shape[0])

        data['runs'] = data['runs_off_bat'].fillna(0) + data['extras'].fillna(0)
        extras_runs = data[data['extras'] > 0]['runs'].sum()
        fours_runs = data[data['runs_off_bat'] == 4]['runs_off_bat'].sum()
        six_runs = data[data['runs_off_bat'] == 6]['runs_off_bat'].sum()
        three_runs = data[data['runs_off_bat'] == 3]['runs_off_bat'].sum()
        two_runs = data[data['runs_off_bat'] == 2]['runs_off_bat'].sum()
        singles_runs = data[data['runs_off_bat'] == 1]['runs'].sum()
        x = ['1s', '3s', '4s', '6s', "Extras", 'Boundary', 'Non Boundary']
        y = [singles_runs, three_runs, fours_runs, six_runs, extras_runs, six_runs + fours_runs,
             singles_runs + three_runs + extras_runs + two_runs]
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Types of Runs Scored')
        """
        * Most number of runs come from boundaries in IPL, as expected in a T20 format.
        * No of Singles are almost Half of total Boundary scores.
        """
        st.plotly_chart(fig)

        # dismissal types
        w = data.groupby('wicket_type').count()
        wicket_type = w.index
        wickets = w["match_id"].values
        x = wicket_type
        y = wickets
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Overall Dismissal Types')
        """
        * Highest dismissals come from catch.It shows the rush of making runs in IPL.
        * No of run-out is almost half the number of bowled. 
        """
        st.plotly_chart(fig)

        ## highest Overall total Scores on grounds
        data = pd.read_csv('deliveries.csv')
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
        x = G["city"].tail(10)
        y = G['runs'].tail(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Highest Overall total Scores on Grounds')
        """
        * Wankhede stadium has hosted highest number of matches hence Mumbai has highest runs in its bucket.
        """
        st.plotly_chart(fig)

        # Lowest Overall Score total on grounds
        x = G["city"].head(10)
        y = G['runs'].head(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Lowest Overall total Scores on Grounds')
        st.plotly_chart(fig)

        # Highest Number of matches played on grounds
        x = G["city"].tail(10)
        y = G['match_id'].tail(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Highest No of Matches Played on Grounds')
        st.plotly_chart(fig)

        # HIGHEST Average Match scoreing grounds
        G['Average'] = (G['runs'] / G['match_id']).astype('int')
        temp = G.sort_values('Average').reset_index()
        temp = temp.drop('index', axis=1)
        x = temp["city"].tail(10)
        y = temp['Average'].tail(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Grounds with Highest Average Match Score ')
        """
        * Higher the average match score shows that the ground is smaller and easy for making runs.
        * Double stack for Mumbai shows that Mumbai has two major grounds(Wankhede and DY Patil stadium).
        * Wankhede stadium is easiest for making runs.
        """
        st.plotly_chart(fig)

        # Lowest Average Match scoreing grounds
        x = temp["city"].head(10)
        y = temp['Average'].head(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Grounds with Lowest Average Match Score ')
        """
            * Lower number of average match score shows that the ground is Large and its hard to make runs there.
            * Ranchi stadium is toughest for making runs.
            """
        st.plotly_chart(fig)

        # Highest Number of matches played by a team
        team1 = match.groupby('team1')['match_id'].count().reset_index()
        team2 = match.groupby('team2')['match_id'].count().reset_index()
        team1 = team1.merge(team2, left_on='team1', right_on='team2')
        team1['total'] = team1['match_id_x'] + team1['match_id_y']
        team1 = team1.sort_values('total', ascending=False).reset_index()
        team1 = team1.drop(columns=['team2', 'index'])
        x = team1['team1'].head(10)
        y = team1['total'].head(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Highest Number of matches played by a team ')
        st.plotly_chart(fig)

        # Top winning teams
        win_team = match['winner'].value_counts().reset_index()
        x = win_team['index'].head(10)
        y = win_team['winner'].head(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Top Winning teams ')
        st.plotly_chart(fig)

        # Teams with Highest Win Percentage
        win_team = match['winner'].value_counts().reset_index()
        win_team = win_team.merge(team1, left_on='index', right_on='team1')
        win_team['percentage'] = ((win_team['winner'] / win_team['total']) * 100).astype('int')
        win_team = win_team.sort_values('percentage', ascending=False).reset_index()
        x = win_team['index'].head(10)
        y = win_team['percentage'].head(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Top Win Percentage teams ')
        st.markdown('- Most Succesfull IPL teams.')
        st.plotly_chart(fig)

        ###
if user_menu == 'Season-Wise-Analysis':
    st.sidebar.header("Season Wise Analysis")

    selected_type = st.sidebar.selectbox('Select Type', ['Batting', 'Bowling', 'Overall'])
    selected_year = st.sidebar.selectbox('Select Type',
                                         ['2022', '2021', '2020/21', '2019', '2018', '2017', '2016', '2015', '2014',
                                          '2013', '2012', '2011', '2009/10', '2009', '2007/08'])

    winners = pd.DataFrame({
        'Seasons': [2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008],
        'Winner': ['Gujarat Titans', 'Chennai Super Kings', 'Mumbai Indians', 'Mumbai Indians', 'Chennai Super Kings',
                   'Mumbai Indians', 'Sunrisers Hyderabad', 'Mumbai Indians', 'Kolkata Knight Riders', 'Mumbai Indians',
                   'Kolkata Knight Riders', 'Chennai Super Kings', 'Chennai Super Kings', 'Deccan Chargers',
                   'Rajasthan Royals']
    })
    st.header('Season wise Winning Teams')
    st.table(winners)

    data = data[data['season'] == selected_year]

    match = match[match['season'] == selected_year]
    if selected_type == 'Batting':
        st.title('Overall Batting Statistics')

        batsman_runs = helper.mostruns(data)
        total_runs = batsman_runs['runs_off_bat'].sum()

        most_fours_batsman = helper.fours(data)
        total_fours = most_fours_batsman['4s'].sum()

        most_six_batsman = helper.six(data)
        total_six = most_six_batsman['6s'].sum()

        most_fifties_batsman = helper.fifties(data)
        total_fifties = most_fifties_batsman['50s'].sum()

        most_hundred_batsman = helper.hundred(data)
        total_hundred = most_hundred_batsman['runs_off_bat'].sum()

        most_dots_batsman = helper.dotballs(data)
        total_dots = most_dots_batsman['striker'].sum()

        most_duck_batsman = helper.ducks(data)
        total_ducks = most_duck_batsman['runs_off_bat'].sum()

        highest_score_batsman = helper.Highest_scores(data)
        highest_score = highest_score_batsman['runs_off_bat'][0]

        highest_runs_batsman = helper.highest(data)

        highest_strikerate = helper.highest_strike(data, batsman_runs)
        highest_avg = helper.highest_avg(data, batsman_runs)
        most_MOM = match['player_of_match'].value_counts().reset_index()
        most_matches = helper.most_matches(playing11)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total Runs')
            st.subheader(total_runs)
        with col2:
            st.header('Total 4s')
            st.subheader(total_fours)
        with col3:
            st.header('Total 6s')
            st.subheader(total_six)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total 50s')
            st.subheader(total_fifties)
        with col2:
            st.header('Total 100s')
            st.subheader(total_hundred)
        with col3:
            st.header('Highest Run(player)')
            st.subheader(highest_score)

        st.header('Top 10 List')

        top_list_batsman = ["Most Runs", 'Most 4s', 'Most 6s', 'Most 50s', 'Most 100s', 'Highest Batsman Score',
                            'Most Ducks', 'Highest Strikerate', 'Highest Average', 'Most Man of the Match',
                            'Most Dotball Played', 'Most Matches Played']
        top_list_selected = st.selectbox('Select Top 10 List', top_list_batsman)

        if top_list_selected == "Most Runs":
            data_selected = batsman_runs.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', 'runs_off_bat': 'y'})
        if top_list_selected == 'Most 4s':
            data_selected = most_fours_batsman.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', '4s': 'y'})
        if top_list_selected == 'Most 6s':
            data_selected = most_six_batsman.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', '6s': 'y'})
        if top_list_selected == 'Most 50s':
            data_selected = most_fifties_batsman.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', '50s': 'y'})
        if top_list_selected == 'Most 100s':
            data_selected = most_hundred_batsman.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', 'runs_off_bat': 'y'})
        if top_list_selected == 'Most Ducks':
            data_selected = most_duck_batsman.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', 'runs_off_bat': 'y'})
        if top_list_selected == 'Highest Strikerate':
            data_selected = highest_strikerate.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', 'strikerate': 'y'})
        if top_list_selected == 'Most Dotball Played':
            data_selected = most_dots_batsman.head(10)
            data_selected = data_selected.rename(columns={'index': 'Batsman', 'striker': 'y'})
        if top_list_selected == 'Highest Average':
            data_selected = highest_avg.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', 'bat_avg': 'y'})
        if top_list_selected == 'Most Man of the Match':
            data_selected = most_MOM.head(10)
            data_selected = data_selected.rename(columns={'index': 'Batsman', 'player_of_match': 'y'})
        if top_list_selected == 'Most Matches Played':
            data_selected = most_matches.head(10)
            data_selected = data_selected.rename(columns={'Player': 'Batsman', 'Matches': 'y'})
        if top_list_selected == 'Highest Batsman Score':
            data_selected = highest_score_batsman.head(10)
            data_selected = data_selected.rename(columns={'striker': 'Batsman', 'runs_off_bat': 'y'})

        fig, ax = plt.subplots()
        col1, col2 = st.columns([1, 3])
        with col2:
            ax.bar(data_selected['Batsman'], data_selected['y'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col1:
            st.table(data_selected)

        # ------Runs per Overs--------

        data['runs'] = data['runs_off_bat'].fillna(0) + data['extras'].fillna(0) + data['wides'].fillna(0)
        run_per_over = data.groupby('over')['runs'].sum().reset_index()
        runs_per_over_inn1 = data[data['innings'] == 1].groupby('over')['runs'].sum().reset_index()
        runs_per_over_inn2 = data[data['innings'] == 2].groupby('over')['runs'].sum().reset_index()
        x = runs_per_over_inn1.merge(runs_per_over_inn2, left_on='over', right_on='over')
        x = run_per_over.merge(x, left_on='over', right_on='over')
        x.rename(columns={'runs_x': 'Inning_1', 'runs_y': 'Inning_2', 'runs': 'Total Run'}, inplace=True)
        fig = px.line(x, x='over', y=['Inning_1', 'Inning_2', 'Total Run'])
        fig.update_layout(autosize=False, width=800, height=600)
        st.header('Runs Per Over(Overall Total)')
        st.plotly_chart(fig)
        st.caption('click on top right variables to filter graphs.')
        st.markdown("- Teams scores more in first inning than second.")
        st.markdown('- Sudden fall in runs scored in 6th and 7th overs is because of Powerplay end.')

        st.header('Effect of Toss Wins and First Bat/Field ')
        x_labels = ['Toss Winner', 'Toss Looser']
        fig = go.Figure(data=[
            go.Bar(name='Total Wins', x=x_labels, y=[483, 467]),
            go.Bar(name='First Bat Win', x=x_labels, y=[156, 195]),
            go.Bar(name='First Field Win', x=x_labels, y=[327, 272])
        ])
        fig.update_layout(barmode='group', width=800, height=600)
        st.plotly_chart(fig)
        st.caption('click on top right variables to filter graphs.')
        st.markdown(
            "- Toss winning team has won more matches than toss loosing team. Winning the toss gives extra edge on match win.")
        st.markdown("- Most of the toss winning teams who won the matches has opted to field first.")

        st.header('Best Finishers')
        do = data[data['over'] > 15].groupby('striker').sum().sort_values('runs_off_bat', ascending=False)
        do = do['runs_off_bat'].reset_index()
        fig = go.Figure([go.Bar(x=do['striker'].head(10), y=do["runs_off_bat"].head(10))])
        st.plotly_chart(fig)
        st.markdown('- Most runs scored by batsman in death overs(16-20)')

        st.header('Best batsman giving good start')
        so = data[data['over'] < 11].groupby('striker').sum().sort_values('runs_off_bat', ascending=False)
        so = so['runs_off_bat'].reset_index()
        fig = go.Figure([go.Bar(x=so['striker'].head(10), y=so["runs_off_bat"].head(10))])
        st.plotly_chart(fig)
        st.markdown('- Most runs scored by batsman in Starting overs(0-10)')

        st.header('Highest Deathover Strikerate')
        hs = helper.highest_strike_other(data[data['over'] > 15], do)
        fig = go.Figure([go.Bar(x=hs['striker'].head(10), y=hs["strikerate"].head(10))])
        st.plotly_chart(fig)

        eo = data[data['over'] < 6].groupby('striker').sum().sort_values('runs_off_bat', ascending=False)
        eo = eo['runs_off_bat'].reset_index()

        st.header('Highest 5overs vs 10overs Runs')
        x_labels = eo['striker'].head(10)
        temp = so[so['striker'].isin(eo['striker'])]
        percent = so[so['striker'].isin(eo['striker'])]
        percent["runs_off_bat"] = ((temp["runs_off_bat"] - eo["runs_off_bat"]) / eo["runs_off_bat"]) * 1000
        fig = go.Figure(data=[
            go.Bar(name='5-Over Run', x=x_labels, y=eo["runs_off_bat"].head(10)),
            go.Bar(name='10-Over Run', x=x_labels, y=temp["runs_off_bat"].head(10)),
            go.Bar(name='% Increase*10', x=x_labels, y=percent["runs_off_bat"].head(10))
        ])
        fig.update_layout(barmode='group', width=800, height=600)
        st.plotly_chart(fig)
        st.caption('click on top right variables to filter graphs.')
        st.markdown(
            '- Highest 5-over to 10-over conversion shows that player is very good at wickets once he playes for more than 5 overs he can make it for 10 overs too.')
        st.markdown(
            '-  % increase From 5-overs to 10-Overs runs shows that these players first save their wickets for initial overs then gradually increases their runrate.')

        # Most runs for winning cause

        w_runs = helper.most_win_run_batsman(data, match)
        fig = go.Figure([go.Bar(x=w_runs['striker'].head(10), y=w_runs["runs_off_bat"].head(10))])
        st.header('Most runs scored in winning cause')
        st.plotly_chart(fig)
        st.markdown(
            '- Thses are top batsman whose performance highly affects win-loss for their teams.')

    # ------------Bowling-----------------

    if selected_type == 'Bowling':
        st.title('Overall Batting Statistics')

        most_wickets = helper.most_wickets(data)
        total_wickets = most_wickets['wicket'].sum()

        highest_wicket_bowler = helper.highest_wickets(data)
        highest_wicket = highest_wicket_bowler['wicket'][0]

        five_w_bowler = helper.five_wicket(data)
        total_5w = five_w_bowler['wicket'].sum()

        most_wides = helper.most_wides(data)
        total_wides = most_wides['bowler'].sum()

        most_dots = helper.most_dots(data)
        total_dots_balls = most_dots['dots'].sum()

        most_economic, most_overs = helper.economic_bowler(data)

        # ---------------Temp-------------
        most_duck_batsman = helper.ducks(data)
        total_ducks = most_duck_batsman['runs_off_bat'].sum()
        # ---------------Temp-------------

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total Wickets')
            st.subheader(total_wickets)
        with col2:
            st.header('Highest Wickets')
            st.subheader(highest_wicket)
        with col3:
            st.header('Total 5+ Wickets')
            st.subheader(total_5w)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total Wides')
            st.subheader(total_wides)
        with col2:
            st.header('Total Dots')
            st.subheader(total_dots_balls)
        with col3:
            st.header('Total Ducks')
            st.subheader(total_ducks)

        st.header('Top 10 List')

        top_list_bowler = ["Most Wickets", 'Most Economic Bowler', 'Highest Wickets', '5 or More Wicket Taker',
                           'Most Dot balls', 'Most No of Wide Balls', 'Highest no of Overs Bowled']
        top_list_selected = st.selectbox('Select Top 10 List', top_list_bowler)

        if top_list_selected == "Most Wickets":
            data_selected = most_wickets.head(10)
            data_selected = data_selected.rename(columns={'bowler': 'Bowler', 'wicket': 'y'})
        if top_list_selected == 'Highest Wickets':
            data_selected = highest_wicket_bowler.head(10)
            data_selected = data_selected.rename(columns={'bowler': 'Bowler', 'wicket': 'y'})
        if top_list_selected == '5 or More Wicket Taker':
            data_selected = five_w_bowler.head(10)
            data_selected = data_selected.rename(columns={'bowler': 'Bowler', 'wicket': 'y'})
        if top_list_selected == 'Most No of Wide Balls':
            data_selected = most_wides.head(10)
            data_selected = data_selected.rename(columns={'index': 'Bowler', 'bowler': 'y'})
        if top_list_selected == 'Most Dot balls':
            data_selected = most_dots.head(10)
            data_selected = data_selected.rename(columns={'index': 'Bowler', 'dots': 'y'})
        if top_list_selected == 'Most Economic Bowler':
            data_selected = most_economic.head(10)
            data_selected = data_selected.rename(columns={'bowler': 'Bowler', 'economy': 'y'})
        if top_list_selected == 'Highest no of Overs Bowled':
            data_selected = most_overs.head(10)
            data_selected = data_selected.rename(columns={'bowler': 'Bowler', 'overs': 'y'})

        fig, ax = plt.subplots()
        col1, col2 = st.columns([1, 3])
        with col2:
            ax.bar(data_selected['Bowler'], data_selected['y'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col1:
            st.table(data_selected)

        fall_of_wickets = data.groupby('over')['wicket_type'].count().reset_index()
        fall_of_wickets1 = data[data['innings'] == 1].groupby('over')['wicket_type'].count().reset_index()
        fall_of_wickets2 = data[data['innings'] == 2].groupby('over')['wicket_type'].count().reset_index()
        fall_of_wickets = fall_of_wickets.merge(fall_of_wickets1, left_on='over', right_on='over')
        fall_of_wickets = fall_of_wickets.merge(fall_of_wickets2, left_on='over', right_on='over')
        fall_of_wickets = fall_of_wickets.rename(
            columns={'wicket_type_x': 'Total', 'wicket_type_y': 'Inning_1', 'wicket_type': 'Inning_2'})
        fig = px.line(fall_of_wickets, x='over', y=['Inning_1', 'Inning_2', 'Total'])
        st.header('Fall of Wickets per overs')
        st.plotly_chart(fig)
        st.caption('click on top right variables to filter graphs.')
        st.markdown(
            '- Most teams looses their early wickets in 4-5th over, may be because of powerplay rush of making runs.')
        st.markdown(
            '- First batting team looses more wickets,with exponential fall at death overs.')
        st.markdown(
            '- Chasing teams most of the times saves their wickets because they do not want to loose their set batsman.')
        # total wickets
        l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
        data_bowler = data.merge(players, left_on='bowler', right_on='Name')
        data_bowler = data_bowler[data_bowler['wicket_type'].isin(l)]
        data_bowler['wicket'] = 1

        data_bowler = data_bowler.groupby('season').sum().reset_index()
        data_bowler = data_bowler.sort_values('wicket', ascending=False).reset_index()
        x = data_bowler['season']
        y = data_bowler['wicket']

        # Wickets taken on Different Grounds
        st.header('Wickets taken on Different Grounds')
        l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
        data_bowler = data.merge(players, left_on='bowler', right_on='Name')
        data_bowler = data_bowler[data_bowler['wicket_type'].isin(l)]
        data_bowler['wicket'] = 1
        w_groundsd = data_bowler.merge(match, left_on='match_id', right_on='match_id')
        w_groundsd = w_groundsd.groupby('venueID').sum().sort_values('wicket', ascending=False).reset_index().head(
            10)
        w_groundsd = w_groundsd.merge(venue, left_on='venueID', right_on='id')
        venues = w_groundsd['venue']
        w_groundsd = w_groundsd[w_groundsd['venue'].isin(venues)]
        fig = go.Figure(data=[go.Bar(
            x=w_groundsd['venue'], y=w_groundsd['wicket'],
            text=y,
            textposition='auto',
        )])
        st.plotly_chart(fig)


    if selected_type == 'Overall':
        st.title('Overall Statistics')

        players = players.drop_duplicates()
        total_players = players.shape[0]

        # total batsman
        pp = ['Top order Batter', 'Middle order Batter', 'Opening Batter']
        batsman = players[players['Playing Position'].isin(pp)]
        total_batsman = batsman.shape[0]

        # total bowlers
        bowlers = players[players['Playing Position'] == 'Bowler']
        total_bowler = bowlers.shape[0]

        # total allrounders
        pa = ['Allrounder', 'Bowling Allrounder', 'Batting Allrounder']
        allrounders = players[players['Playing Position'].isin(pa)]
        total_allrounders = allrounders.shape[0]

        # total wicketkeepr
        pw = ['Wicketkeeper', 'Wicketkeeper Batter']
        total_Wicketkeeper = players[players['Playing Position'].isin(pw)].shape[0]
        # total seasons
        total_seasons = match['season'].value_counts().shape[0]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total Players')
            st.subheader(total_players)
        with col2:
            st.header('Total Batsman')
            st.subheader(total_batsman)
        with col3:
            st.header('Total Bowlers')
            st.subheader(total_bowler)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total Allrounders')
            st.subheader(total_allrounders)
        with col2:
            st.header('Total Wicketkeeper')
            st.subheader(total_Wicketkeeper)
        with col3:
            st.header('Total Seasons')
            st.subheader(total_seasons)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Total Matches')
            st.subheader(match.drop_duplicates().shape[0])
        with col2:
            st.header('Total Venue')
            st.subheader(venue.drop_duplicates().shape[0])

        data['runs'] = data['runs_off_bat'].fillna(0) + data['extras'].fillna(0)
        extras_runs = data[data['extras'] > 0]['runs'].sum()
        fours_runs = data[data['runs_off_bat'] == 4]['runs_off_bat'].sum()
        six_runs = data[data['runs_off_bat'] == 6]['runs_off_bat'].sum()
        three_runs = data[data['runs_off_bat'] == 3]['runs_off_bat'].sum()
        two_runs = data[data['runs_off_bat'] == 2]['runs_off_bat'].sum()
        singles_runs = data[data['runs_off_bat'] == 1]['runs'].sum()
        x = ['1s', '3s', '4s', '6s', "Extras", 'Boundary', 'Non Boundary']
        y = [singles_runs, three_runs, fours_runs, six_runs, extras_runs, six_runs + fours_runs,
             singles_runs + three_runs + extras_runs + two_runs]
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Types of Runs Scored')
        """
               * Most number of runs come from boundaries in IPL, as expected in a T20 format.
               * No of Singles are almost Half of total Boundary scores.
               """
        st.plotly_chart(fig)

        # dismissal types
        w = data.groupby('wicket_type').count()
        wicket_type = w.index
        wickets = w["match_id"].values
        x = wicket_type
        y = wickets
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Overall Dismissal Types')
        """
        * Highest dismissals come from catch.It shows the rush of making runs in IPL.
        * No of run-out is almost half the number of bowled. 
        """
        st.plotly_chart(fig)

        ## highest Overall total Scores on grounds
        data = pd.read_csv('deliveries.csv')
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
        x = G["city"].tail(10)
        y = G['runs'].tail(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Highest Overall total Scores on Grounds')
        """
                * Stadium which has hosted highest number of matches has highest runs in its bucket.
                """
        st.plotly_chart(fig)

        # Lowest Overall Score total on grounds
        x = G["city"].head(10)
        y = G['runs'].head(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Lowest Overall total Scores on Grounds')
        st.plotly_chart(fig)

        # Highest Number of matches played on grounds
        x = G["city"].tail(10)
        y = G['match_id'].tail(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Highest No of Matches Played on Grounds')
        st.plotly_chart(fig)

        # HIGHEST Average Match scoreing grounds
        G['Average'] = (G['runs'] / G['match_id']).astype('int')
        temp = G.sort_values('Average').reset_index()
        temp = temp.drop('index', axis=1)
        x = temp["city"].tail(10)
        y = temp['Average'].tail(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Grounds with Highest Average Match Score ')
        st.plotly_chart(fig)

        # Lowest Average Match scoreing grounds
        x = temp["city"].head(10)
        y = temp['Average'].head(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Grounds with Lowest Average Match Score ')
        st.plotly_chart(fig)

        # Highest Number of matches played by a team
        team1 = match.groupby('team1')['match_id'].count().reset_index()
        team2 = match.groupby('team2')['match_id'].count().reset_index()
        team1 = team1.merge(team2, left_on='team1', right_on='team2')
        team1['total'] = team1['match_id_x'] + team1['match_id_y']
        team1 = team1.sort_values('total', ascending=False).reset_index()
        team1 = team1.drop(columns=['team2', 'index'])
        x = team1['team1'].head(10)
        y = team1['total'].head(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Highest Number of matches played by a team ')
        """
               * Higher the average match score shows that the ground is smaller and easy for making runs.
               * Stack for Mumbai shows that Mumbai has Multiple grounds(Wankhede,DY Patil stadium and MCA Stadium).
               """
        st.plotly_chart(fig)

        # Top winning teams
        win_team = match['winner'].value_counts().reset_index()
        x = win_team['index'].head(10)
        y = win_team['winner'].head(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Top Winning teams ')
        st.plotly_chart(fig)

        # Teams with Highest Win Percentage
        win_team = match['winner'].value_counts().reset_index()
        win_team = win_team.merge(team1, left_on='index', right_on='team1')
        win_team['percentage'] = ((win_team['winner'] / win_team['total']) * 100).astype('int')
        win_team = win_team.sort_values('percentage', ascending=False).reset_index()
        x = win_team['index'].head(10)
        y = win_team['percentage'].head(10)
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
        st.header('Top Win Percentage teams ')
        st.markdown('- Most Succesfull team of the season.')
        st.plotly_chart(fig)

    ###
if user_menu == 'Player-wise-analysis':
    st.title('Player-wise-analysis')
    players_full_name = players['Full Name']

    selected_player = st.selectbox('Select Player', players_full_name)
    player_name = players[players['Full Name'] == selected_player]['Name'].values[0]
    selected_type = st.selectbox('Select Type', ['Batting', 'Bowling'])

    if selected_type == 'Batting':
        data = data[data['striker'] == player_name]

        player_data = data.groupby('match_id').sum()
        matches_played = player_data.shape[0]
        st.title('Overall Batting Statistics')
        if matches_played < 5:
            st.header('Insufficient data: Player has Scored less than 50 Runs')
        else:
            batsman_runs = helper.mostruns(data)
            total_runs = batsman_runs['runs_off_bat'].sum()

            most_fours_batsman = helper.fours(data)
            total_fours = most_fours_batsman['4s'].sum()

            most_six_batsman = helper.six(data)
            total_six = most_six_batsman['6s'].sum()

            most_fifties_batsman = helper.fifties(data)
            total_fifties = most_fifties_batsman['50s'].sum()

            most_hundred_batsman = helper.hundred(data)
            total_hundred = most_hundred_batsman['runs_off_bat'].sum()

            most_dots_batsman = helper.dotballs(data)
            total_dots = most_dots_batsman['striker'].sum()

            most_duck_batsman = helper.ducks(data)
            total_ducks = most_duck_batsman['runs_off_bat'].sum()

            highest_score_batsman = helper.Highest_scores(data)
            highest_score = highest_score_batsman['runs_off_bat'][0]

            highest_runs_batsman = helper.highest(data)

            highest_strikerate = helper.highest_strike_other(data, batsman_runs)
            highest_avg = helper.highest_avg_o(data, batsman_runs)
            most_MOM = match['player_of_match'].value_counts().reset_index()
            most_matches = helper.most_matches(playing11)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.header('Total Runs')
                st.subheader(total_runs)
            with col2:
                st.header('Total 4s')
                st.subheader(total_fours)
            with col3:
                st.header('Total 6s')
                st.subheader(total_six)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.header('Total 50s')
                st.subheader(total_fifties)
            with col2:
                st.header('Total 100s')
                st.subheader(total_hundred)
            with col3:
                st.header('Highest Run')
                st.subheader(highest_score)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.header('Total Ducks')
                st.subheader(total_ducks)
            with col2:
                st.header('Strike Rate')
                st.subheader(highest_strikerate['strikerate'][0].astype('int'))
            with col3:
                st.header('Batting Average')
                st.subheader((highest_avg['bat_avg'][0]).astype('int'))

            # ------Runs per Overs--------

            data['runs'] = data['runs_off_bat'].fillna(0) + data['extras'].fillna(0) + data['wides'].fillna(0)
            run_per_over = data.groupby('over')['runs'].sum().reset_index()
            runs_per_over_inn1 = data[data['innings'] == 1].groupby('over')['runs'].sum().reset_index()
            runs_per_over_inn2 = data[data['innings'] == 2].groupby('over')['runs'].sum().reset_index()
            x = runs_per_over_inn1.merge(runs_per_over_inn2, left_on='over', right_on='over')
            x = run_per_over.merge(x, left_on='over', right_on='over')
            x.rename(columns={'runs_x': 'Inning_1', 'runs_y': 'Inning_2', 'runs': 'Total Run'}, inplace=True)
            fig = px.line(x, x='over', y=['Inning_1', 'Inning_2', 'Total Run'])
            fig.update_layout(autosize=False, width=800, height=600)
            st.header('Runs Per Over(Overall Total)')
            """
                    * Region of higher overall run graph gives an idea about Overs or number at which player generally comes to play.
                    * Higher graph shows that player has played and scored more in those overs.
                    """
            st.caption('click on top right variables to filter graphs.')
            st.plotly_chart(fig)



            ##Overwise Strikerate

            data[['extras', 'wides', 'noballs', 'byes', 'legbyes', 'penalty']] = data[
                ['extras', 'wides', 'noballs', 'byes', 'legbyes', 'penalty']].fillna(0).astype('int')
            data['count'] = 1
            ball_faced_dataO = data[(data['wides'] == 0)]
            ball_faced_dataO = ball_faced_dataO.groupby('over').sum().reset_index()
            ball_faced_dataO['strikerate'] = (
                        (ball_faced_dataO['runs_off_bat'] / ball_faced_dataO['count']) * 100).astype(
                'int')
            ball_faced_data1 = data[(data['wides'] == 0) & (data['innings'] == 1)]
            ball_faced_data1 = ball_faced_data1.groupby('over').sum().reset_index()
            ball_faced_data1['strikerate'] = (
                        (ball_faced_data1['runs_off_bat'] / ball_faced_data1['count']) * 100).astype(
                'int')
            ball_faced_data2 = data[(data['wides'] == 0) & (data['innings'] == 2)]
            ball_faced_data2 = ball_faced_data2.groupby('over').sum().reset_index()
            ball_faced_data2['strikerate'] = (
                        (ball_faced_data2['runs_off_bat'] / ball_faced_data2['count']) * 100).astype(
                'int')
            ball_faced_dataO = ball_faced_dataO.merge(ball_faced_data1, left_on='over', right_on='over')
            ball_faced_dataO = ball_faced_dataO.merge(ball_faced_data2, left_on='over', right_on='over')
            ball_faced_dataO = ball_faced_dataO.rename(
                columns={'strikerate_x': 'Overall', 'strikerate_y': 'Inning_1', 'strikerate': 'Inning_2'})
            fig = px.line(ball_faced_dataO, x='over', y=['Overall', 'Inning_1', 'Inning_2'])
            st.header('Overwise Strikerate')
            """
                            * Region of higher overall strikerate graph gives an idea about how agressive this player generally play in that over.
                            * Higher graph shows that player has played with highe strike-rate in those overs and scored more.
                            """
            st.caption('click on top right variables to filter graphs.')
            st.plotly_chart(fig)

            # Total Runs
            st.header('Total Runs')
            """
            * Higher peak shows golden time of this batsman.
            * This graph gives an idea of players consistency over different seasons.
             """
            highest_run_p = play.highest_runs(data, match, venue)
            s_runs = highest_run_p.groupby('Season').sum().reset_index().sort_values('Run', ascending=False)
            s_runs = s_runs.reset_index()
            s_runs = s_runs.drop('index', axis=1)
            x = s_runs['Season']
            y = s_runs['Run']
            fig = go.Figure(data=[go.Bar(
                x=x, y=y,
                text=y,
                textposition='auto',
            )])
            st.plotly_chart(fig)

            st.header('Highest Runs')
            st.write(highest_run_p.head(20))
            x = highest_run_p['Season'].head(10)
            y = highest_run_p['Run'].head(10)
            fig = go.Figure(data=[go.Bar(
                x=x, y=y,
                text=y,
                textposition='auto',
            )])
            st.header('Highest Runs')
            st.plotly_chart(fig)

            # Runs scored on Different Grounds
            runs_grounds = highest_run_p.groupby('venue').sum()
            runs_grounds = runs_grounds.sort_values('Run', ascending=False).reset_index().head(10)
            venues = runs_grounds['venue']
            highest_runs_g = highest_run_p[highest_run_p['venue'].isin(venues)]

            dfs = highest_runs_g.groupby('venue').sum()
            fig = px.bar(highest_runs_g, x="venue", y="Run", color="Season")

            fig.add_trace(go.Scatter(
                x=dfs.index,
                y=dfs['Run'],
                text=dfs['Run'],
                mode='text',
                textposition='top center',
                textfont=dict(
                    size=14,
                ),
                showlegend=False
            ))
            st.header('Highest Runs on different Grounds')
            """
            * Highest Peak shows home ground of this player,as most teams play most of their matches in homeground.
            * Apart from homeground,this graph tells about other favorite and toughest grond of this player.
             """
            st.caption('click on top right variables to filter graphs.')
            st.plotly_chart(fig)

            # higheststrike-rate against bolltype
            highest_run_agains_bolltype = play.highest_run_agains_bolltype(data, players)
            x = highest_run_agains_bolltype['Bowling Style']
            y = highest_run_agains_bolltype['boll_type_avg']
            fig = go.Figure(data=[go.Bar(
                x=x, y=y,
                text=y,
                textposition='auto',
            )])
            st.header('Highest Strike Rate Against Different bowling styles')
            """
            * Graph gives an idea about comfortable and trouble making bowling actions for this player. 
            """
            st.plotly_chart(fig)

            # most no of outs
            most_out_against = play.most_out_against(data, players)
            x = most_out_against['Bowling Style'].head(10)
            y = most_out_against['Out Percentage']
            fig = go.Figure(data=[go.Bar(
                x=x, y=y,
                text=y,
                textposition='auto',
            )])
            st.header('Highest Out percentage on different bowling action')
            """
            * Graph gives an idea about most strugling bowling action for this batsman.
            * Note that number of pacers are more than number of spinners. 
            """
            st.plotly_chart(fig)


    if selected_type == 'Bowling':
        data = data[data['bowler'] == player_name]
        st.title('Overall Bowling Statistics')

        player_data = data.groupby('match_id').sum()
        matches_played = player_data.shape[0]

        if matches_played < 5:
            st.header('Insufficient data: Player has Bowled in less than 5 Matches')
        else:

            most_wickets = helper.most_wickets(data)
            total_wickets = most_wickets['wicket'].sum()

            highest_wicket_bowler = helper.highest_wickets(data)
            highest_wicket = highest_wicket_bowler['wicket'][0]

            five_w_bowler = helper.five_wicket(data)
            total_5w = five_w_bowler['wicket'].sum()

            most_wides = helper.most_wides(data)
            total_wides = most_wides['bowler'].sum()

            most_dots = helper.most_dots(data)
            total_dots_balls = most_dots['dots'].sum()

            most_economic, most_overs = helper.economic_bowler_o(data)
            most_MOM = match['player_of_match'].value_counts().reset_index()
            most_matches = helper.most_matches(playing11)
            me = round(most_economic['economy'].values[0], 2)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.header('Total Wickets')
                st.subheader(total_wickets)
            with col2:
                st.header('Highest Wicket')
                st.subheader(highest_wicket)
            with col3:
                st.header('5-Wickets')
                st.subheader(total_5w)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.header('Total Wides')
                st.subheader(total_wides)
            with col2:
                st.header('Total Dotballs')
                st.subheader(total_dots_balls)
            with col3:
                st.header('Economy')
                st.subheader(me)

            col1, col2, col3 = st.columns(3)
            # with col1:
            #     st.header('Total Overs Bowled')
            #     st.subheader(most_overs['overs'][0].value[0])
            with col1:
                st.header('No of MOM')
                st.subheader(most_MOM['player_of_match'][0])
            # with col3:
            #     st.header('Batting Average')
            #     st.subheader((highest_avg['bat_avg'][0]).astype('int'))

            # ------wickets per Overs--------
            l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
            data_bowler = data.merge(players, left_on='bowler', right_on='Name')
            data_bowler = data_bowler[data_bowler['wicket_type'].isin(l)]
            data_bowler['wicket'] = 1
            total_outs = data_bowler.shape[0]

            data_bowlerO = data_bowler.groupby('over').sum().reset_index()
            data_bowler1 = data_bowler[data_bowler['innings'] == 1]
            data_bowler1 = data_bowler1.groupby('over').sum().reset_index()
            data_bowler2 = data_bowler[data_bowler['innings'] == 2]
            data_bowler2 = data_bowler2.groupby('over').sum().reset_index()
            data_bowlerO = data_bowlerO.merge(data_bowler1, left_on='over', right_on='over', how='left')
            data_bowlerO = data_bowlerO[['over', 'wicket_x', 'wicket_y']]
            data_bowlerO = data_bowlerO.merge(data_bowler2, left_on='over', right_on='over', how='left')
            data_bowlerO = data_bowlerO.fillna(0)
            data_bowlerO = data_bowlerO.rename(
                columns={'wicket_x': 'Overall', 'wicket_y': 'Inning_1', 'wicket': 'Inning_2'})
            fig = px.line(data_bowlerO, x='over', y=['Overall', 'Inning_1', 'Inning_2'])
            st.header('Wickets Per Over(Overall Total)')

            """
            * Higher peaks gives an idea about overs at which this bowler generally come for bowling.
            """
            st.caption('click on top right variables to filter graphs.')
            st.plotly_chart(fig)


            # Total Wicketss
            st.header('Total Wickets')
            data_bowler = data_bowler.groupby('season').sum().reset_index()
            data_bowler = data_bowler.sort_values('wicket', ascending=False).reset_index()
            x = data_bowler['season']
            y = data_bowler['wicket']
            fig = go.Figure(data=[go.Bar(
                x=x, y=y,
                text=y,
                textposition='auto',
            )])
            """
            * Most succesfull ipl season for this bowler.
            """
            st.plotly_chart(fig)

            # Wickets taken on Different Grounds
            st.header('Wickets taken on Different Grounds')
            l = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
            data_bowler = data.merge(players, left_on='bowler', right_on='Name')
            data_bowler = data_bowler[data_bowler['wicket_type'].isin(l)]
            data_bowler['wicket'] = 1
            w_groundsd = data_bowler.merge(match, left_on='match_id', right_on='match_id')
            w_groundsd = w_groundsd.groupby('venueID').sum().sort_values('wicket', ascending=False).reset_index().head(
                10)
            w_groundsd = w_groundsd.merge(venue, left_on='venueID', right_on='id')
            venues = w_groundsd['venue']
            w_groundsd = w_groundsd[w_groundsd['venue'].isin(venues)]
            fig = go.Figure(data=[go.Bar(
                x=w_groundsd['venue'], y=w_groundsd['wicket'],
                text=y,
                textposition='auto',
            )])
            """
            * Most of the wickets comes from home ground because most of the matches are played in home ground.
            * Other grounds at which this bowler takes wicket can be seen easily.
            """
            st.plotly_chart(fig)
if user_menu == 'Team-wise-analysis':
    st.title("Team-wise-analysis")

    teams = data['batting_team'].unique()
    selected_team = st.selectbox('Select Team', teams)
    winners = pd.DataFrame({
        'Seasons': [2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008],
        'Winner': ['Gujarat Titans', 'Chennai Super Kings', 'Mumbai Indians', 'Mumbai Indians', 'Chennai Super Kings',
                   'Mumbai Indians', 'Sunrisers Hyderabad', 'Mumbai Indians', 'Kolkata Knight Riders', 'Mumbai Indians',
                   'Kolkata Knight Riders', 'Chennai Super Kings', 'Chennai Super Kings', 'Deccan Chargers',
                   'Rajasthan Royals']
    })
    st.header('Season wise Winning Teams')
    st.table(winners)

    st.header('Season wise Overall Team runs')
    bat_r = helper.runs_perseason(data, selected_team)
    fig = px.bar(bat_r, x="season", y="runs", color="innings", title=selected_team + " Overall Runs per season")
    st.plotly_chart(fig)
    data_t = data[data['batting_team'] == selected_team]
    data_t['runs'] = data_t['runs_off_bat'].fillna(0) + data_t['extras'].fillna(0) + data['wides'].fillna(0)
    run_per_over = data_t.groupby('over')['runs'].sum().reset_index()
    runs_per_over_inn1 = data_t[data_t['innings'] == 1].groupby('over')['runs'].sum().reset_index()
    runs_per_over_inn2 = data_t[data_t['innings'] == 2].groupby('over')['runs'].sum().reset_index()
    x = runs_per_over_inn1.merge(runs_per_over_inn2, left_on='over', right_on='over')
    x = run_per_over.merge(x, left_on='over', right_on='over')
    x.rename(columns={'runs_x': 'Inning_1', 'runs_y': 'Inning_2', 'runs': 'Total Run'}, inplace=True)
    fig = px.line(x, x='over', y=['Inning_1', 'Inning_2', 'Total Run'])
    # fig.update_layout(autosize=False, width=800, height=600)
    st.header('Runs Per Over(Overall Total)')
    st.plotly_chart(fig)
    st.caption('click on top right variables to filter graphs.')
    st.markdown("- Teams scores more in first inning than second.")
    st.markdown('- Sudden fall in runs scored in 6th and 7th overs is because of Powerplay end.')

    fall_of_wickets = data_t.groupby('over')['wicket_type'].count().reset_index()
    fall_of_wickets1 = data_t[data['innings'] == 1].groupby('over')['wicket_type'].count().reset_index()
    fall_of_wickets2 = data_t[data_t['innings'] == 2].groupby('over')['wicket_type'].count().reset_index()
    fall_of_wickets = fall_of_wickets.merge(fall_of_wickets1, left_on='over', right_on='over')
    fall_of_wickets = fall_of_wickets.merge(fall_of_wickets2, left_on='over', right_on='over')
    fall_of_wickets = fall_of_wickets.rename(
        columns={'wicket_type_x': 'Total', 'wicket_type_y': 'Inning_1', 'wicket_type': 'Inning_2'})
    fig = px.line(fall_of_wickets, x='over', y=['Inning_1', 'Inning_2', 'Total'])
    st.header('Fall of Wickets per overs')
    st.plotly_chart(fig)


    st.header('No of matches Played vs Won')
    total_m, total_m_w, t_s = helper.total_match_per_season(data, match, selected_team)
    Seasons = t_s
    fig = go.Figure(data=[
        go.Bar(name='Total Matches', x=Seasons, y=total_m),
        go.Bar(name='Matches Won', x=Seasons, y=total_m_w)
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

    st.header('Highest Run Scorer for ' + selected_team)
    bat_r = helper.team_highest_scorers(data, selected_team)
    x_labels = bat_r['striker'].head(10)
    fig = go.Figure(data=[
        go.Bar(name='Total Runs', x=x_labels, y=bat_r['runs_x']),
        go.Bar(name='Inning_1 Runs', x=x_labels, y=bat_r['runs_y']),
        go.Bar(name='Inning_2 Runs', x=x_labels, y=bat_r['runs'])
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

    st.header('Highest Powerplay Run Scorer for ' + selected_team)
    bat_r = helper.team_highest_scorers(data, selected_team)
    x_labels = bat_r['striker'].head(10)
    fig = go.Figure(data=[
        go.Bar(name='Total Runs', x=x_labels, y=bat_r['runs_x']),
        go.Bar(name='Inning_1 Runs', x=x_labels, y=bat_r['runs_y']),
        go.Bar(name='Inning_2 Runs', x=x_labels, y=bat_r['runs'])
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

    st.header('Highest Death-over Run Scorer for ' + selected_team)
    bat_r = helper.team_highest_deathover_run_scorer(data, selected_team)
    x_labels = bat_r['striker'].head(10)
    fig = go.Figure(data=[
        go.Bar(name='Total Runs', x=x_labels, y=bat_r['runs_x']),
        go.Bar(name='Inning_1 Runs', x=x_labels, y=bat_r['runs_y']),
        go.Bar(name='Inning_2 Runs', x=x_labels, y=bat_r['runs'])
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

    st.header('Highest Middle over Run Scorer for ' + selected_team)
    bat_r = helper.team_highest_middleover_run_scorer(data, selected_team)
    x_labels = bat_r['striker'].head(10)
    fig = go.Figure(data=[
        go.Bar(name='Total Runs', x=x_labels, y=bat_r['runs_x']),
        go.Bar(name='Inning_1 Runs', x=x_labels, y=bat_r['runs_y']),
        go.Bar(name='Inning_2 Runs', x=x_labels, y=bat_r['runs'])
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

    st.header('Highest Wicket Taking Bowler for ' + selected_team)
    ball_r = helper.team_top_wicket_taker(data, selected_team)
    x_labels = ball_r['bowler'].head(10)
    fig = go.Figure(data=[
        go.Bar(name='Total Wickets', x=x_labels, y=ball_r['wicket_x']),
        go.Bar(name='Inning_1 Wickets', x=x_labels, y=ball_r['wicket_y']),
        go.Bar(name='Inning_2 Wickets', x=x_labels, y=ball_r['wicket'])
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

    st.header('Highest Powerplay Wicket Taking Bowler for ' + selected_team)
    ball_r = helper.team_top_wicket_taker_in_powerplay(data, selected_team)
    x_labels = ball_r['bowler'].head(10)
    fig = go.Figure(data=[
        go.Bar(name='Total Wickets', x=x_labels, y=ball_r['wicket_x']),
        go.Bar(name='Inning_1 Wickets', x=x_labels, y=ball_r['wicket_y']),
        go.Bar(name='Inning_2 Wickets', x=x_labels, y=ball_r['wicket'])
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

    st.header('Highest Middle Over Wicket Taking Bowler for ' + selected_team)
    ball_r = helper.team_top_wicket_taker_in_Middleover(data, selected_team)
    x_labels = ball_r['bowler'].head(10)
    fig = go.Figure(data=[
        go.Bar(name='Total Wickets', x=x_labels, y=ball_r['wicket_x']),
        go.Bar(name='Inning_1 Wickets', x=x_labels, y=ball_r['wicket_y']),
        go.Bar(name='Inning_2 Wickets', x=x_labels, y=ball_r['wicket'])
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

    st.header('Highest Death Over Wicket Taking Bowler for ' + selected_team)
    ball_r = helper.team_top_wicket_taker_in_Death(data, selected_team)
    x_labels = ball_r['bowler'].head(10)
    fig = go.Figure(data=[
        go.Bar(name='Total Wickets', x=x_labels, y=ball_r['wicket_x']),
        go.Bar(name='Inning_1 Wickets', x=x_labels, y=ball_r['wicket_y']),
        go.Bar(name='Inning_2 Wickets', x=x_labels, y=ball_r['wicket'])
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

    st.header('Highest Average Match Total on different Grounds for ' + selected_team)
    temp,G = helper.team_highest_avg_score_grounds(data,match,venue,selected_team)
    x = temp["stadium"].tail(10)
    y = temp['Average'].tail(10)
    fig = go.Figure(data=[go.Bar(
        x=x, y=y,
        text=y,
        textposition='auto',
    )])
    st.plotly_chart(fig)

    st.header('Lowest Average Match Total on different Grounds for ' + selected_team)
    x = temp["stadium"].head(10)
    y = temp['Average'].head(10)
    fig = go.Figure(data=[go.Bar(
        x=x, y=y,
        text=y,
        textposition='auto',
    )])
    st.plotly_chart(fig)

    # Highest Number of matches played on grounds
    x = G["city"].tail(10)
    y = G['match_id'].tail(10)
    fig = go.Figure(data=[go.Bar(
        x=x, y=y,
        text=y,
        textposition='auto',
    )])
    st.header('Highest No of Matches Played on Grounds')
    st.plotly_chart(fig)

st.sidebar.caption('''  
                        

                        
                        
                        * Developed By:
                          * Aryan Chaturvedi
                          * B.Tech, IIT Roorkee
                          * Email:  aryan_c@ch.iitr.ac.in
                    ''')
