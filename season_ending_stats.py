import setup
from tabulate import tabulate

query = setup.get_ff_query()
teams = query.get_league_teams()
numWeeks = 17

process_team_weekly_player = False
best_by_position_overall=dict()
best_by_position_by_team=dict()

process_team_weekly = False
best_and_worst_week_by_team=dict()

process_matchups = True
curr_most_lopsided_match = None
curr_closest_match = None

def process_team_weekly_player_stats(team_id, team_name, week, team_best_by_position, best_by_position_overall):
    team_player_stats = query.get_team_roster_player_stats_by_week(team_id, week)
    for player in team_player_stats:
        position = player.selected_position.position
        points_for_week = player.player_points.total
        if position not in best_by_position_overall or points_for_week > best_by_position_overall[position][4]:
            best_by_position_overall[position] = (position, week, player.name.full, team_name, points_for_week)
        if position not in team_best_by_position or points_for_week > team_best_by_position[position][3]:
            team_best_by_position[position] = (week, player.name.full, position, points_for_week)

def process_team_weekly_stats(team_id, team_name, week, best_and_worst_week_by_team):
    team_week_stats = query.get_team_stats_by_week(team_id, week)
    curr_week_points = team_week_stats['team_points'].total
    if team_name not in best_and_worst_week_by_team:
        best_and_worst_week_by_team[team_name] = (team_name, week, curr_week_points, week, curr_week_points)
    elif best_and_worst_week_by_team[team_name][2] < curr_week_points:
        best_and_worst_week_by_team[team_name] = (team_name, week, curr_week_points, best_and_worst_week_by_team[team_name][3], best_and_worst_week_by_team[team_name][4])
    elif curr_week_points > 0 and best_and_worst_week_by_team[team_name][4] > curr_week_points:
        best_and_worst_week_by_team[team_name] = (team_name, best_and_worst_week_by_team[team_name][1], best_and_worst_week_by_team[team_name][2], week, curr_week_points)

def process_matchups_stats(week):
    global curr_most_lopsided_match, curr_closest_match
    matchups_stats = query.get_league_matchups_by_week(week)
    for matchup in matchups_stats:
        team_1_points = matchup.teams[0].team_points.total
        team_2_points = matchup.teams[1].team_points.total
        diff = abs(team_1_points - team_2_points)
        if curr_most_lopsided_match is None or diff > curr_most_lopsided_match[5]:
            if team_1_points > team_2_points:
                curr_most_lopsided_match = (matchup.week, matchup.teams[0].name.decode(), team_1_points,
                                            matchup.teams[1].name.decode(), team_2_points, diff)
            else:
                curr_most_lopsided_match = (matchup.week, matchup.teams[1].name.decode(), team_2_points,
                                            matchup.teams[0].name.decode(), team_1_points, diff)
        if curr_closest_match is None or diff < curr_closest_match[5]:
            if team_1_points > team_2_points:
                curr_closest_match = (matchup.week, matchup.teams[0].name.decode(), team_1_points,
                                            matchup.teams[1].name.decode(), team_2_points, diff)
            else:
                curr_closest_match = (matchup.week, matchup.teams[1].name.decode(), team_2_points,
                                            matchup.teams[0].name.decode(), team_1_points, diff)

if process_team_weekly_player or process_team_weekly:
    for team in teams:
        team_id = team.team_id
        team_name = team.name.decode()
        team_best_by_position = dict()
        for week in range(1,numWeeks+1):
            if process_team_weekly_player:
                process_team_weekly_player_stats(team_id, team_name, week, team_best_by_position, best_by_position_overall)
            if process_team_weekly:
                process_team_weekly_stats(team_id, team_name, week, best_and_worst_week_by_team)
        best_by_position_by_team[team_name] = team_best_by_position

if process_team_weekly_player:
    print("Best overall performance for each position across entire season")
    print(tabulate(best_by_position_overall.values(), headers=['Position', 'Week', 'Player Name', 'Team Name', 'Points for Week'], tablefmt='orgtbl'))
    for team in teams:
        team_name = team.name.decode()
        print(f"\nBest performance for each position for team '{team_name}'")
        print(tabulate(best_by_position_by_team[team_name].values(), headers=['Week', 'Player Name', 'Position', 'Points for Week'], tablefmt='orgtbl'))

if process_team_weekly:
    print("Best and worst week for each team")
    print(tabulate(best_and_worst_week_by_team.values(), headers=['Team Name', 'Best Week', 'Best Points', 'Worst Week', 'Worst Points'], tablefmt='orgtbl'))

if process_matchups:
    for week in range(1,numWeeks+1):
        process_matchups_stats(week)
    print("Most lopsided matchup of the season")
    print(tabulate([curr_most_lopsided_match], headers=['Week', 'Winner', 'Winner Points', 'Loser', 'Loser Points', 'Differential'], tablefmt='orgtbl'))
    print("Closest matchup of the season")
    print(tabulate([curr_closest_match], headers=['Week', 'Winner', 'Winner Points', 'Loser', 'Loser Points', 'Differential'], tablefmt='orgtbl'))