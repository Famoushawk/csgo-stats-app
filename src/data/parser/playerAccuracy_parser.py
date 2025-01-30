import re
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict


class PlayerAccuracyParser:
    def __init__(self):
        self.timestamp_pattern = r'^(\d{2}/\d{2}/\d{2}\d{2} - \d{2}:\d{2}:\d{2})'
        self.damage_pattern = r'"(.+?)<(\d+)>.+?" \[.+?\] attacked "(.+?)<(\d+)>.+?" \[.+?\] with "([^"]+)" \(damage "(\d+)"\).+?\(hitgroup "([^"]+)"\)'
        self.kill_pattern = r'"(.+?)<(\d+)>.+?\] killed "(.+?)<(\d+)>.+?\] with "([^"]+)"(\s*\(headshot\))?'

    def parse_timestamp(self, timestamp_str: str) -> datetime:
        """Convert timestamp string to datetime object."""
        return datetime.strptime(timestamp_str, '%m/%d/%Y - %H:%M:%S')

    def create_weapon_stats_template(self):
        """Create a template for weapon statistics."""
        return {
            "hits": 0,
            "kills": 0,
            "headshot_kills": 0,
            "total_damage": 0,
            "hitgroups": defaultdict(int),
            "damage_by_hitgroup": defaultdict(list),
            "accuracy_stats": {
                "hits_by_hitgroup": defaultdict(int),
                "avg_damage_by_hitgroup": defaultdict(float)
            }
        }

    def parse_player_accuracy(self, log_content: str) -> Dict:
        lines = log_content.strip().split('\n')

        # Initialize tracking variables
        match_started = False
        player_stats = defaultdict(lambda: defaultdict(self.create_weapon_stats_template))
        accuracy_events = []

        for line in lines:
            # Extract timestamp
            timestamp_match = re.match(self.timestamp_pattern, line)
            if not timestamp_match:
                continue

            timestamp = self.parse_timestamp(timestamp_match.group(1))
            content = line[timestamp_match.end():].strip(': ')

            # Detect match start
            if 'World triggered "Match_Start"' in content:
                match_started = True
                continue

            # Only process events after match has started
            if not match_started:
                continue

            # Parse damage events
            damage_match = re.search(self.damage_pattern, content)
            if damage_match:
                attacker = damage_match.group(1)
                weapon = damage_match.group(5)
                damage = int(damage_match.group(6))
                hitgroup = damage_match.group(7)

                # Update player weapon stats
                player_stats[attacker][weapon]["hits"] += 1
                player_stats[attacker][weapon]["total_damage"] += damage
                player_stats[attacker][weapon]["hitgroups"][hitgroup] += 1
                player_stats[attacker][weapon]["damage_by_hitgroup"][hitgroup].append(damage)

                # Record event
                event = {
                    "timestamp": timestamp.strftime('%H:%M:%S'),
                    "type": "damage",
                    "player": attacker,
                    "weapon": weapon,
                    "damage": damage,
                    "hitgroup": hitgroup
                }
                accuracy_events.append(event)
                continue

            # Parse kill events
            kill_match = re.search(self.kill_pattern, content)
            if kill_match:
                killer = kill_match.group(1)
                weapon = kill_match.group(5)
                is_headshot = bool(kill_match.group(6))

                # Update kill stats
                player_stats[killer][weapon]["kills"] += 1
                if is_headshot:
                    player_stats[killer][weapon]["headshot_kills"] += 1

                # Record event
                event = {
                    "timestamp": timestamp.strftime('%H:%M:%S'),
                    "type": "kill",
                    "player": killer,
                    "weapon": weapon,
                    "headshot": is_headshot
                }
                accuracy_events.append(event)

        # Calculate final statistics
        formatted_stats = {}
        for player, weapons in player_stats.items():
            formatted_stats[player] = {}
            for weapon, stats in weapons.items():
                # Calculate averages for each hitgroup
                hitgroup_averages = {}
                for hitgroup, damages in stats["damage_by_hitgroup"].items():
                    hitgroup_averages[hitgroup] = sum(damages) / len(damages)

                # Calculate headshot percentage
                hs_percentage = (stats["headshot_kills"] / stats["kills"] * 100) if stats["kills"] > 0 else 0

                formatted_stats[player][weapon] = {
                    "total_hits": stats["hits"],
                    "total_kills": stats["kills"],
                    "headshot_kills": stats["headshot_kills"],
                    "headshot_percentage": round(hs_percentage, 2),
                    "total_damage": stats["total_damage"],
                    "average_damage": round(stats["total_damage"] / stats["hits"], 2) if stats["hits"] > 0 else 0,
                    "hitgroup_distribution": dict(stats["hitgroups"]),
                    "hitgroup_percentages": {
                        hitgroup: round(count / stats["hits"] * 100, 2)
                        for hitgroup, count in stats["hitgroups"].items()
                    } if stats["hits"] > 0 else {},
                    "average_damage_by_hitgroup": {
                        k: round(v, 2) for k, v in hitgroup_averages.items()
                    }
                }

        return {
            "player_stats": formatted_stats,
            "events": accuracy_events
        }


def main():
    parser = PlayerAccuracyParser()

    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct paths relative to the script location
    input_path = os.path.join(script_dir, '../NAVIvsVitaGF-Nuke.txt')
    output_path = os.path.join(script_dir, '../../../public/data/player_accuracy_stats.json')

    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as file:
            log_content = file.read()

        # Parse the log
        accuracy_data = parser.parse_player_accuracy(log_content)

        # Write to JSON file
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(accuracy_data, file, indent=2)

        # Print summary
        print("\nPlayer Accuracy Analysis:")
        for player, weapons in accuracy_data["player_stats"].items():
            print(f"\nPlayer: {player}")
            for weapon, stats in weapons.items():
                print(f"\n  {weapon}:")
                print(f"    Total Hits: {stats['total_hits']}")
                print(f"    Total Kills: {stats['total_kills']}")
                print(f"    Headshot Kills: {stats['headshot_kills']} ({stats['headshot_percentage']}%)")
                print(f"    Average Damage: {stats['average_damage']}")
                print("\n    Hitgroup Distribution:")
                for hitgroup, percentage in stats['hitgroup_percentages'].items():
                    hits = stats['hitgroup_distribution'][hitgroup]
                    print(f"      {hitgroup}: {hits} hits ({percentage}%)")
                print("\n    Average Damage by Hitgroup:")
                for hitgroup, avg_damage in stats['average_damage_by_hitgroup'].items():
                    print(f"      {hitgroup}: {avg_damage}")

    except FileNotFoundError:
        print(f"Error: Could not find input file at {input_path}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()