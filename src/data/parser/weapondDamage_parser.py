import re
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict


class WeaponDamageParser:
    def __init__(self):
        self.timestamp_pattern = r'^(\d{2}/\d{2}/\d{2}\d{2} - \d{2}:\d{2}:\d{2})'
        self.damage_pattern = r'"(.+?)<(\d+)>.+?" \[.+?\] attacked "(.+?)<(\d+)>.+?" \[.+?\] with "([^"]+)" \(damage "(\d+)"\).+?\(hitgroup "([^"]+)"\)'

    def parse_timestamp(self, timestamp_str: str) -> datetime:
        """Convert timestamp string to datetime object."""
        return datetime.strptime(timestamp_str, '%m/%d/%Y - %H:%M:%S')

    def parse_damage_events(self, log_content: str) -> Dict:
        lines = log_content.strip().split('\n')

        # Initialize tracking variables
        match_started = False
        weapon_stats = defaultdict(lambda: {
            "total_damage": 0,
            "hits": 0,
            "hitgroups": defaultdict(int),
            "max_damage": 0,
            "min_damage": float('inf'),
            "avg_damage": 0,
            "damage_by_hitgroup": defaultdict(list)
        })

        damage_events = []

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

            # Only process damage after match has started
            if not match_started:
                continue

            # Parse damage information
            damage_match = re.search(self.damage_pattern, content)
            if not damage_match:
                continue

            attacker = damage_match.group(1)
            victim = damage_match.group(3)
            weapon = damage_match.group(5)
            damage = int(damage_match.group(6))
            hitgroup = damage_match.group(7)

            # Record damage event
            event = {
                "timestamp": timestamp.strftime('%H:%M:%S'),
                "attacker": attacker,
                "victim": victim,
                "weapon": weapon,
                "damage": damage,
                "hitgroup": hitgroup
            }
            damage_events.append(event)

            # Update weapon statistics
            weapon_stats[weapon]["total_damage"] += damage
            weapon_stats[weapon]["hits"] += 1
            weapon_stats[weapon]["hitgroups"][hitgroup] += 1
            weapon_stats[weapon]["max_damage"] = max(weapon_stats[weapon]["max_damage"], damage)
            weapon_stats[weapon]["min_damage"] = min(weapon_stats[weapon]["min_damage"], damage)
            weapon_stats[weapon]["damage_by_hitgroup"][hitgroup].append(damage)

        # Calculate averages and format stats
        formatted_stats = {}
        for weapon, stats in weapon_stats.items():
            avg_damage = stats["total_damage"] / stats["hits"] if stats["hits"] > 0 else 0

            # Calculate average damage per hitgroup
            hitgroup_averages = {}
            for hitgroup, damages in stats["damage_by_hitgroup"].items():
                hitgroup_averages[hitgroup] = sum(damages) / len(damages)

            formatted_stats[weapon] = {
                "total_damage": stats["total_damage"],
                "total_hits": stats["hits"],
                "max_damage": stats["max_damage"],
                "min_damage": stats["min_damage"] if stats["min_damage"] != float('inf') else 0,
                "average_damage": round(avg_damage, 2),
                "hitgroup_distribution": dict(stats["hitgroups"]),
                "average_damage_by_hitgroup": {k: round(v, 2) for k, v in hitgroup_averages.items()}
            }

        return {
            "weapon_stats": formatted_stats,
            "damage_events": damage_events
        }


def main():
    parser = WeaponDamageParser()

    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct paths relative to the script location
    input_path = os.path.join(script_dir, '../NAVIvsVitaGF-Nuke.txt')
    output_path = os.path.join(script_dir, '../../../public/data/weapon_damage_stats.json')

    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as file:
            log_content = file.read()

        # Parse the log
        damage_data = parser.parse_damage_events(log_content)

        # Write to JSON file
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(damage_data, file, indent=2)

        # Print summary
        print("\nWeapon Damage Analysis:")
        for weapon, stats in damage_data["weapon_stats"].items():
            print(f"\n{weapon}:")
            print(f"  Total Hits: {stats['total_hits']}")
            print(f"  Total Damage: {stats['total_damage']}")
            print(f"  Average Damage: {stats['average_damage']}")
            print(f"  Damage Range: {stats['min_damage']} - {stats['max_damage']}")
            print("\n  Average Damage by Hitgroup:")
            for hitgroup, avg in stats['average_damage_by_hitgroup'].items():
                print(f"    {hitgroup}: {avg}")
            print("\n  Hitgroup Distribution:")
            for hitgroup, count in stats['hitgroup_distribution'].items():
                print(f"    {hitgroup}: {count}")

    except FileNotFoundError:
        print(f"Error: Could not find input file at {input_path}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()