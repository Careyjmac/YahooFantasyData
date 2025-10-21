import setup
from tabulate import tabulate

query = setup.get_ff_query()

week = 7
teams = query.get_league_teams()

def get_qb_points_for_team(team_player_stats):
    for player in team_player_stats:
        if player.selected_position_value == "QB":
            return player.player_points_value

output = list()
winner = ""
winner_total = float('inf')
winner_overall = 0
for team in teams:
    team_player_stats = query.get_team_roster_player_stats_by_week(team.team_id, week)
    team_stats = query.get_team_stats_by_week(team.team_id, week)
    team_qb_points = get_qb_points_for_team(team_player_stats)
    if team_qb_points < winner_total or (team_qb_points == winner_total and team_stats["team_points"].total > winner_overall):
        winner = team.name
        winner_total = team_qb_points
        winner_overall = team_stats["team_points"].total
    output.append([team.name.decode(), team_qb_points, team_stats["team_points"].total])

output.sort(key=lambda x: x[1], reverse=False)
print(f"\nCalculating winner for week {week}, QB Least Points...\n")
print(tabulate(output, headers=['Team Name','QB Points', 'Total(Tiebreaker)'], tablefmt='orgtbl'))
print(f"\nWinner!: {winner.decode()}")