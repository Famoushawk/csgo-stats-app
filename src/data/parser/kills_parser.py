import re
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class EnhancedKillParser:
    def __init__(self):
        self.timestamp_pattern = r'^(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})'
        self.kill_pattern = r'"([^"]+)<\d+><STEAM_\d:\d:\d+><([^>]+)>" \[([-\d\s]+)\] killed "([^"]+)<\d+><STEAM_\d:\d:\d+><([^>]+)>" \[([-\d\s]+)\] with "([^"]+)"(\s*\(headshot\))?'
        self.match_start_pattern = r'World triggered "Match_Start"'
        self.round_start_pattern = r'World triggered "Round_Start"'
        self.round_end_pattern = r'World triggered "Round_End"'
        self.live_pattern = r'\[FACEIT\^\] LIVE!'

    def parse_timestamp(self, timestamp_str: str) -> datetime:
        return datetime.strptime(timestamp_str, '%m/%d/%Y - %H:%M:%S')

    def parse_position(self, pos_str: str) -> Dict[str, int]:
        x, y, z = map(int, pos_str.strip().split())
        return {"x": x, "y": y, "z": z}

    def initialize_player_stats(self) -> Dict:
        return {
            "total_kills": 0,
            "deaths": 0,
            "headshots": 0,
            "weapons": {},
            "headshot_percentage": 0,
            "team_kills": 0
        }

    def create_round_snapshot(self, player_stats: Dict) -> Dict:
        """Create a deep copy of player stats for the round snapshot."""
        snapshot = {}
        for player, stats in player_stats.items():
            snapshot[player] = {
                "total_kills": stats["total_kills"],
                "deaths": stats["deaths"],
                "headshots": stats["headshots"],
                "weapons": dict(stats["weapons"]),
                "headshot_percentage": stats["headshot_percentage"],
                "team_kills": stats["team_kills"]
            }
        return snapshot

    def parse_kills(self, log_content: str) -> Dict:
        lines = log_content.strip().split('\n')

        # Initialize tracking variables
        live_started = False
        match_started = False
        current_round = 0
        round_snapshots = []
        current_round_start_time = None

        kills_data = []
        player_stats = {}
        match_start_time = None
        live_start_time = None

        for line in lines:
            timestamp_match = re.match(self.timestamp_pattern, line)
            if not timestamp_match:
                continue

            timestamp = self.parse_timestamp(timestamp_match.group(1))
            content = line[timestamp_match.end():].strip(': ')

            # Check for LIVE! trigger
            if not live_started and re.search(self.live_pattern, content):
                live_started = True
                live_start_time = timestamp
                continue

            # Skip lines before LIVE! trigger
            if not live_started:
                continue

            # Check for round start
            if re.search(self.round_start_pattern, content):
                current_round += 1
                current_round_start_time = timestamp
                continue

            # Check for round end
            if re.search(self.round_end_pattern, content):
                # Create a snapshot of the current stats for this round
                round_snapshot = {
                    "round_number": current_round,
                    "start_time": current_round_start_time.strftime('%H:%M:%S'),
                    "end_time": timestamp.strftime('%H:%M:%S'),
                    "player_stats": self.create_round_snapshot(player_stats)
                }
                round_snapshots.append(round_snapshot)
                continue

            # Parse kill information
            kill_match = re.search(self.kill_pattern, content)
            if not kill_match:
                continue

            # Extract kill data
            killer_name = kill_match.group(1)
            killer_team = kill_match.group(2)
            killer_pos = self.parse_position(kill_match.group(3))
            victim_name = kill_match.group(4)
            victim_team = kill_match.group(5)
            victim_pos = self.parse_position(kill_match.group(6))
            weapon = kill_match.group(7)
            is_headshot = bool(kill_match.group(8))

            # Initialize stats for new players
            if killer_name not in player_stats:
                player_stats[killer_name] = self.initialize_player_stats()
            if victim_name not in player_stats:
                player_stats[victim_name] = self.initialize_player_stats()

            # Record kill data with round number
            kill_data = {
                "round": current_round,
                "timestamp": timestamp.strftime('%H:%M:%S'),
                "killer": {
                    "name": killer_name,
                    "team": killer_team,
                    "position": killer_pos
                },
                "victim": {
                    "name": victim_name,
                    "team": victim_team,
                    "position": victim_pos
                },
                "weapon": weapon,
                "headshot": is_headshot
            }
            kills_data.append(kill_data)

            # Update statistics
            self.update_player_stats(player_stats, killer_name, victim_name, weapon, is_headshot,
                                     killer_team == victim_team)

        # Calculate final statistics
        self.calculate_final_stats(player_stats)

        return {
            "live_start_time": live_start_time.strftime('%H:%M:%S') if live_start_time else None,
            "match_start_time": match_start_time.strftime('%H:%M:%S') if match_start_time else None,
            "total_kills": len(kills_data),
            "total_rounds": current_round,
            "player_stats": player_stats,
            "kills": kills_data,
            "round_stats": round_snapshots
        }

    def update_player_stats(self, player_stats: Dict, killer: str, victim: str, weapon: str, is_headshot: bool,
                            is_team_kill: bool):
        """Update player statistics after a kill."""
        # Update killer statistics
        player_stats[killer]["total_kills"] += 1
        if is_headshot:
            player_stats[killer]["headshots"] += 1
        if weapon not in player_stats[killer]["weapons"]:
            player_stats[killer]["weapons"][weapon] = 0
        player_stats[killer]["weapons"][weapon] += 1
        if is_team_kill:
            player_stats[killer]["team_kills"] += 1

        # Update victim statistics
        player_stats[victim]["deaths"] += 1

    def calculate_final_stats(self, player_stats: Dict):
        """Calculate final statistics for all players."""
        for player in player_stats:
            total_kills = player_stats[player]["total_kills"]
            headshots = player_stats[player]["headshots"]
            player_stats[player]["headshot_percentage"] = (
                round((headshots / total_kills) * 100, 2) if total_kills > 0 else 0
            )


def main():
    parser = EnhancedKillParser()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, '../NAVIvsVitaGF-Nuke.txt')
    output_path = os.path.join(script_dir, '../../../public/data/kill_stats.json')

    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            log_content = file.read()

        kill_data = parser.parse_kills(log_content)

        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(kill_data, file, indent=2)

        print(f"\nEnhanced Kill Analysis Summary:")
        print(f"Total Rounds: {kill_data['total_rounds']}")
        print(f"Total Kills: {kill_data['total_kills']}")
        print("\nRoundInformation-by-RoundInformation Statistics Available")

    except FileNotFoundError:
        print(f"Error: Could not find input file at {input_path}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()