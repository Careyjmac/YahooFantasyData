import setup
from tabulate import tabulate

query = setup.get_ff_query()

week = 4
teams = query.get_league_teams()

game_info=query.get_current_game_info()
int_stat_ids = list()
fum_rec_stat_ids = list()
for stat in game_info.stat_categories.stats:
    if "Interception" in stat.name:
        int_stat_ids.append(stat.stat_id)
    elif stat.name == "Fumble Recovery":
        fum_rec_stat_ids.append(stat.stat_id)

def get_turnovers_for_team(team_player_stats):
    team_int = 0
    team_fum_rec = 0
    for player in team_player_stats:
        if player.selected_position_value == "DEF":
            for stat in player.player_stats.stats:
                if stat.stat_id in int_stat_ids:
                    team_int += stat.value
                if stat.stat_id in fum_rec_stat_ids:
                    team_fum_rec += stat.value
    return team_int, team_fum_rec

output = list()
winner = ""
winner_total = 0
winner_overall = 0
for team in teams:
    team_player_stats = query.get_team_roster_player_stats_by_week(team.team_id, week)
    team_stats = query.get_team_stats_by_week(team.team_id, week)
    team_int, team_fum_rec = get_turnovers_for_team(team_player_stats)
    total = team_int + team_fum_rec
    if total > winner_total or (total == winner_total and team_stats["team_points"].total > winner_overall):
        winner = team.name
        winner_total = total
        winner_overall = team_stats["team_points"].total
    output.append([team.name.decode(), team_int, team_fum_rec, total])

print(tabulate(output, headers=['Team Name','Interceptions','Fumble Recoveries','Total Turnovers'], tablefmt='orgtbl'))
print(f"\nWinner!: {winner.decode()}")