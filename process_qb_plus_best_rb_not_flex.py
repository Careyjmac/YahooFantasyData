import setup
from tabulate import tabulate

query = setup.get_ff_query()

week = 6
teams = query.get_league_teams()

def get_points_for_team(team_stats):
    qb_points = 0
    rb_points = 0
    for player in team_stats:
        if player.selected_position_value == "QB":
            qb_points = player.player_points_value
        if player.selected_position_value == "RB":
            if player.player_points_value > rb_points:
                rb_points = player.player_points_value
    return qb_points, rb_points

output = list()
winner = ""
winner_total = 0
winner_overall = 0
for team in teams:
    team_stats = query.get_team_roster_player_stats_by_week(team.team_id, week)
    team_qb_points, team_rb_points = get_points_for_team(team_stats)
    total = team_qb_points + team_rb_points
    if total > winner_total or (total == winner_total and team.team_points > winner_overall):
        winner = team.name
        winner_total = total
        winner_overall = team.team_points
    output.append([team.name.decode(), team_qb_points, team_rb_points, total])

print(tabulate(output, headers=['Team Name','QB Points','Best RB Points','Total'], tablefmt='orgtbl'))
print(f"\nWinner!: {winner.decode()}")