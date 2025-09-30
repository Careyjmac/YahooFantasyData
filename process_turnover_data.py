import setup

query = setup.get_ff_query()

week = 4
matches = query.get_league_matchups_by_week(week)

game_info=query.get_current_game_info()
int_stat_ids = list()
fum_rec_stat_ids = list()
fourth_down_stops_stat_ids = list()
for stat in game_info.stat_categories.stats:
    if stat.name.__contains__("Interception"):
        int_stat_ids.append(stat.stat_id)
    elif stat.name.__contains__("Fumble Recovery"):
        fum_rec_stat_ids.append(stat.stat_id)
    elif stat.name.__contains__("4th Down Stops"):
        fourth_down_stops_stat_ids.append(stat.stat_id)

def get_turnovers_for_team(team_stats):
    team_int = 0
    team_fum_rec = 0
    team_fourth_down_stops = 0
    for player in team_stats:
        if player.selected_position_value == "DEF":
            for stat in player.player_stats.stats:
                if stat.stat_id in int_stat_ids:
                    team_int += stat.value
                if stat.stat_id in fum_rec_stat_ids:
                    team_fum_rec += stat.value
                if stat.stat_id in fourth_down_stops_stat_ids:
                    team_fourth_down_stops += stat.value
    return team_int, team_fum_rec, team_fourth_down_stops

print("Team Name,Interceptions,Fumble Recoveries,Fourth Down Stops")
for match in matches:
    team_1_stats = query.get_team_roster_player_stats_by_week(match.teams[0].team_id, week)
    team_1_int, team_1_fum_rec, team_1_fourth_down_stops = get_turnovers_for_team(team_1_stats)
    team_2_stats = query.get_team_roster_player_stats_by_week(match.teams[1].team_id, week)
    team_2_int, team_2_fum_rec, team_2_fourth_down_stops  = get_turnovers_for_team(team_2_stats)
    print(f"{str(match.teams[0].name)},{team_1_int},{team_1_fum_rec},{team_1_fourth_down_stops}")
    print(f"{str(match.teams[1].name)},{team_2_int},{team_2_fum_rec},{team_2_fourth_down_stops}")
