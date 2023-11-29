import pandas as pd
import itertools
from datetime import datetime, timedelta
import importlib.util
if importlib.util.find_spec("pulp") is None:
    raise ImportError("The 'pulp' library is not installed. Please install it to continue.")


def bin_packing_fair_seeding(teams, group_size):
    """
    Distribute teams into groups to minimize the average point difference between groups.
    
    This function sorts teams by their points and then assigns them to groups in a way that
    aims to balance the total points in each group. Teams are distributed alternatively to
    each group based on their ranking.

    Parameters:
    - teams (list of tuples): List where each tuple contains team information (name, points).
    - group_size (int): The number of teams in each group.

    Returns:
    - list: A list of groups, each group is a list of teams.
    """
    if len(teams) < group_size:
        return []

    teams.sort(key=lambda x: x[1], reverse=True)
    num_groups = len(teams) // group_size
    groups = [[] for _ in range(num_groups)]

    for i, team in enumerate(teams):
        index = i % num_groups if i // num_groups % 2 == 0 else num_groups - 1 - (i % num_groups)
        groups[index].append(team)

    return groups

def schedule_matches(groups, available_times, match_duration, num_courts):
    """
    Schedule matches for teams within each group, considering available times and courts.

    Ensures no player is double-booked and schedules matches according to the provided
    time slots and court availability.

    Parameters:
    - groups (list): List of groups, each group is a list of teams.
    - available_times (dict): Dictionary with available times for each day of matches.
    - match_duration (int): Duration of each match in minutes.
    - num_courts (int): Number of available courts.

    Returns:
    - list: A list of scheduled matches, each match includes time, match detail, and court.
    """
    matches = [match for group in groups for match in itertools.combinations([team for team, _ in group], 2)]
    all_players = set(player for group in groups for team, _ in group for player in team.split(' - '))

    time_slots = []
    for day, times in available_times.items():
        for start, end in times:
            current_time = start
            while current_time + timedelta(minutes=match_duration) <= end:
                for court in range(num_courts):
                    time_slots.append((current_time, court + 1))
                current_time += timedelta(minutes=match_duration)

    def is_player_free(player, time_slot, scheduled_matches):
        for scheduled_time, scheduled_match, _ in scheduled_matches:
            if scheduled_time == time_slot and player in scheduled_match.replace('Match_', '').replace('_', ' - '):
                return False
        return True

    scheduled_matches = []
    for time_slot, court in time_slots:
        for match in list(matches):
            players = match[0].split(' - ') + match[1].split(' - ')
            if all(is_player_free(player, time_slot, scheduled_matches) for player in players):
                scheduled_matches.append((time_slot, f'Match_{match[0]}_{match[1]}', f'Court {court}'))
                matches.remove(match)
                break

    return scheduled_matches

def schedule_to_dataframe(schedule):
    """
    Convert a schedule list to a pandas DataFrame.

    Parameters:
    - schedule (list): A list of tuples, each containing time, match, and court information.

    Returns:
    - DataFrame: A pandas DataFrame with columns for Date, Time, Team 1, Team 2, and Court.
    """
    
    # Prepare data for DataFrame
    data = []
    for entry in schedule:
        if len(entry) == 3:
            time, match_str, court = entry
            day = time.strftime('%Y-%m-%d')
            match_time = time.strftime('%H:%M')
            teams = match_str.replace('Match_', '').split('_')
            team1, team2 = teams[0], teams[1]

            row = {
                "Day": day,
                "Time": match_time,
                "Team 1": team1,
                "Team 2": team2,
                "Court": court
            }
            data.append(row)
        else:
            print(f"Invalid entry in schedule: {entry}")

    # Create DataFrame
    df = pd.DataFrame(data)
    return df

from datetime import datetime, timedelta
import itertools

def schedule_matches_v1(groups, available_times, match_duration, num_courts, max_consecutive=2):
    # Generate matches within each group
    matches = [match for group in groups for match in itertools.combinations([team for team, _ in group], 2)]

    # Initialize tracking for players
    all_players = {player: {'last_court': None, 'consecutive': 0} for group in groups for team, _ in group for player in team.split(' - ')}

    # Generate list of available time slots
    time_slots = []
    for day, times in available_times.items():
        for start, end in times:
            current_time = start
            while current_time + timedelta(minutes=match_duration) <= end:
                for court in range(num_courts):
                    time_slots.append((current_time, court + 1))
                current_time += timedelta(minutes=match_duration)

    def is_player_free(player, time_slot, scheduled_matches, court):
        player_info = all_players[player]
        # Check if player needs rest
        if player_info['consecutive'] >= max_consecutive:
            return False
        # Check if player has a match at this time slot
        for scheduled_time, scheduled_match, scheduled_court in scheduled_matches:
            if scheduled_time == time_slot and player in scheduled_match.replace('Match_', '').replace('_', ' - '):
                # Check for same court if consecutive match
                if player_info['consecutive'] > 0 and scheduled_court != court:
                    return False
                return False
        return True

    # Schedule the matches
    scheduled_matches = []
    for time_slot, court in time_slots:
        for match in list(matches):
            players = match[0].split(' - ') + match[1].split(' - ')
            if all(is_player_free(player, time_slot, scheduled_matches, court) for player in players):
                match_str = f'Match_{match[0]}_{match[1]}'
                scheduled_matches.append((time_slot, match_str, f'Court {court}'))
                matches.remove(match)
                # Update player info
                for player in players:
                    if all_players[player]['last_court'] == court:
                        all_players[player]['consecutive'] += 1
                    else:
                        all_players[player] = {'last_court': court, 'consecutive': 1}
                break
            # Reset consecutive count after a gap
            for player in players:
                if not is_player_free(player, time_slot, scheduled_matches, court):
                    all_players[player]['consecutive'] = 0

    return scheduled_matches



def schedule_matches_mip(groups, available_times, match_duration, num_courts):
    # Generate matches within each group
    matches = [match for group in groups for match in itertools.combinations([team for team, _ in group], 2)]
    match_indices = range(len(matches))

    # Extract individual players
    players = set(player for group in groups for team, _ in group for player in team.split(' - '))

    # Generate list of available time slots
    time_slots = []
    for day, times in available_times.items():
        for start, end in times:
            current_time = start
            while current_time + timedelta(minutes=match_duration) <= end:
                time_slots.append(current_time)
                current_time += timedelta(minutes=match_duration)
    time_slot_indices = range(len(time_slots))

    # Create a PuLP problem
    problem = pulp.LpProblem("Match_Scheduling_Minimize_Total_Time", pulp.LpMinimize)

    # Decision variables
    match_vars = pulp.LpVariable.dicts("match",
                                       ((match_idx, time_slot_idx, court) for match_idx in match_indices for time_slot_idx in time_slot_indices for court in range(num_courts)),
                                       0, 1, pulp.LpBinary)

    # Additional variables to handle consecutive match constraint
    consecutive_match_vars = pulp.LpVariable.dicts("consecutive_match",
                                                  ((player, time_slot_idx) for player in players for time_slot_idx in time_slot_indices),
                                                  0, 1, pulp.LpBinary)


    # Objective: Minimize the latest time slot used
    problem += pulp.lpSum([time_slot_idx * match_vars[match_idx, time_slot_idx, court] for match_idx in match_indices for time_slot_idx in time_slot_indices for court in range(num_courts)])

    # Constraint: Each match is scheduled exactly once
    for match_idx in match_indices:
        problem += pulp.lpSum([match_vars[match_idx, time_slot_idx, court] for time_slot_idx in time_slot_indices for court in range(num_courts)]) == 1

    # Constraint: No player plays more than once at the same time
    for time_slot_idx in time_slot_indices:
        for player in players:
            problem += pulp.lpSum([match_vars[match_idx, time_slot_idx, court] for match_idx in match_indices for court in range(num_courts) if player in ' - '.join(matches[match_idx])]) <= 1

    # Constraint: Only one match per court per time slot
    for time_slot_idx in time_slot_indices:
        for court in range(num_courts):
            problem += pulp.lpSum([match_vars[match_idx, time_slot_idx, court] for match_idx in match_indices]) <= 1

    # Constraints for consecutive matches
    for player in players:
        for time_slot_idx in time_slot_indices[:-1]:  # Consider up to the second last time slot for consecutive checks
            # Constraint for identifying consecutive matches
            problem += consecutive_match_vars[player, time_slot_idx] <= pulp.lpSum([match_vars[match_idx, time_slot_idx, court] + match_vars[match_idx, time_slot_idx + 1, court] for match_idx in match_indices for court in range(num_courts) if player in ' - '.join(matches[match_idx])])

            # Constraint to limit consecutive matches to 2, then a gap is needed
            if time_slot_idx < len(time_slots) - 2:  # Ensure the index + 2 is within range
                problem += pulp.lpSum([consecutive_match_vars[player, ts] for ts in range(time_slot_idx, time_slot_idx + 3)]) <= 2


                problem += pulp.lpSum([consecutive_match_vars[player, ts] for ts in range(time_slot_idx, min(time_slot_idx + 3, len(time_slots)))]) <= 2


    # Constraint for same court in consecutive matches
    for player in players:
        for time_slot_idx in time_slot_indices[:-1]:
            for court in range(num_courts):
                problem += (consecutive_match_vars[player, time_slot_idx] + pulp.lpSum([match_vars[match_idx, time_slot_idx, court] for match_idx in match_indices if player in ' - '.join(matches[match_idx])])) <= 1

    # Solve the problem
    problem.solve()

    # Extract the schedule
    scheduled_matches = []
    if problem.status == pulp.LpStatusOptimal:
        for match_idx in match_indices:
            for time_slot_idx in time_slot_indices:
                for court in range(num_courts):
                    if pulp.value(match_vars[match_idx, time_slot_idx, court]) == 1:
                        match_time = time_slots[time_slot_idx]
                        scheduled_matches.append((match_time, f'Match_{matches[match_idx][0]}_{matches[match_idx][1]}', f'Court {court + 1}'))
        return scheduled_matches
    else:
        print("No feasible solution found.")
        return None
