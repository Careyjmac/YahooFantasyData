import setup

query = setup.get_ff_query()

def print_stats_for_player(query, player_key, player_name):
    player_stats_week_1 = query.get_player_stats_by_week(player_key, 1)
    player_stats_week_2 = query.get_player_stats_by_week(player_key, 2)
    week_1_ret_yards = 0
    week_2_ret_yards = 0
    for stat in player_stats_week_1.player_stats.stats:
        if stat.stat_id == 14 or stat.stat_id == 48:
            week_1_ret_yards += stat.value
    for stat in player_stats_week_2.player_stats.stats:
        if stat.stat_id == 14 or stat.stat_id == 48:
            week_2_ret_yards += stat.value
    print(
        f"{player_name},{week_1_ret_yards},{player_stats_week_1.player_points.total},{week_2_ret_yards},{player_stats_week_2.player_points.total}")

# game_info=query.get_current_game_info()
# return_yards_id=list()
# for stat in game_info.stat_categories.stats:
#     if stat.name == "Return Yards":
#         return_yards_id.append(stat.stat_id)

# start = 2845
# end = None
# players=query.get_league_players(end,start)

# for player in players:
#     print_stats_for_player(query, player.player_key, player.full_name)

week = 2
matches = query.get_league_matchups_by_week(week)

def get_return_yards_points_for_team(query, team_stats):
    team_ret_yards_points = 0
    team_ret_yards_bonus_points = 0
    for player in team_stats:
        if player.selected_position_value == "BN":
            continue
        for stat in player.player_stats.stats:
            if stat.stat_id == 14 or stat.stat_id == 48:
                team_ret_yards_points += stat.value / 10.0
                if player.display_position == "DEF":
                    continue
                if stat.value >= 60:
                    team_ret_yards_bonus_points += 3
                    team_ret_yards_points += 3
                if stat.value >= 80:
                    team_ret_yards_bonus_points += 5
                    team_ret_yards_points += 5
                if stat.value >= 99:
                    team_ret_yards_bonus_points += 10
                    team_ret_yards_points += 10
    return team_ret_yards_points, team_ret_yards_bonus_points

for match in matches:
    team_1_points = match.teams[0].team_points.total
    team_1_stats = query.get_team_roster_player_stats_by_week(match.teams[0].team_id, week)
    team_1_ret_yards_points, team_1_ret_yards_bonus_points = get_return_yards_points_for_team(query, team_1_stats)
    team_2_points = match.teams[1].team_points.total
    team_2_stats = query.get_team_roster_player_stats_by_week(match.teams[1].team_id, week)
    team_2_ret_yards_points, team_2_ret_yards_bonus_points  = get_return_yards_points_for_team(query, team_2_stats)
    if team_1_points > team_2_points:
        print(f"{str(match.teams[0].name)},{team_1_points},{team_1_ret_yards_points},{team_1_ret_yards_bonus_points},"
              f"{str(match.teams[1].name)},{team_2_points},{team_2_ret_yards_points},{team_2_ret_yards_bonus_points}")
    else:
        print(f"{str(match.teams[1].name)},{team_2_points},{team_2_ret_yards_points},{team_2_ret_yards_bonus_points},"
              f"{str(match.teams[0].name)},{team_1_points},{team_1_ret_yards_points},{team_1_ret_yards_bonus_points}")
