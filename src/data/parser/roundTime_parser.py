import re
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class RoundTimingParser:
    def __init__(self):
        self.timestamp_pattern = r'^(\d{2}/\d{2}/\d{2}\d{2} - \d{2}:\d{2}:\d{2})'

    def parse_timestamp(self, timestamp_str: str) -> datetime:
        """Convert timestamp string to datetime object."""
        return datetime.strptime(timestamp_str, '%m/%d/%Y - %H:%M:%S')

    def calculate_duration(self, start: datetime, end: datetime) -> int:
        """Calculate duration in seconds between two timestamps."""
        duration = (end - start).total_seconds()
        return int(duration)

    def parse_round_timings(self, log_content: str) -> Dict:
        lines = log_content.strip().split('\n')

        # Initialize tracking variables
        match_started = False
        rounds_data = []
        match_start_time = None
        round_start_time = None
        actual_rounds = []  # Store all rounds to reindex later

        for line in lines:
            timestamp_match = re.match(self.timestamp_pattern, line)
            if not timestamp_match:
                continue

            timestamp = self.parse_timestamp(timestamp_match.group(1))
            content = line[timestamp_match.end():].strip(': ')

            # Detect match start
            if 'World triggered "Match_Start" on "de_nuke"' in content:
                match_started = True
                match_start_time = timestamp
                continue

            # Only process events after match has started
            if not match_started:
                continue

            # Detect round start
            if 'World triggered "Round_Start"' in content:
                round_start_time = timestamp

            # Detect round end
            elif ('World triggered "Round_End"' in content or 'World triggered "Game_Over"' in content) and round_start_time:
                duration = self.calculate_duration(round_start_time, timestamp)
                actual_rounds.append({
                    "start_time": round_start_time.strftime('%H:%M:%S'),
                    "end_time": timestamp.strftime('%H:%M:%S'),
                    "duration_seconds": duration
                })
                round_start_time = None

        # Reindex rounds from 1 to match total rounds
        rounds_data = []
        for i, round_data in enumerate(actual_rounds, 1):
            round_data["round_number"] = i
            rounds_data.append(round_data)

        # Calculate statistics
        if rounds_data:
            durations = [r["duration_seconds"] for r in rounds_data]
            avg_duration = sum(durations) / len(durations)

            stats = {
                "total_rounds": len(rounds_data),
                "average_round_duration": round(avg_duration, 2),
                "shortest_round": min(durations),
                "longest_round": max(durations),
                "match_start_time": match_start_time.strftime('%H:%M:%S') if match_start_time else None,
                "total_match_duration": self.calculate_duration(
                    match_start_time,
                    self.parse_timestamp(timestamp_match.group(1))
                ) if match_start_time else None,
                "rounds": rounds_data
            }
        else:
            stats = {
                "total_rounds": 0,
                "average_round_duration": 0,
                "shortest_round": 0,
                "longest_round": 0,
                "match_start_time": None,
                "total_match_duration": 0,
                "rounds": []
            }

        return stats


def main():
    parser = RoundTimingParser()

    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct paths relative to the script location
    input_path = os.path.join(script_dir, '../NAVIvsVitaGF-Nuke.txt')
    output_path = os.path.join(script_dir, '../../../public/data/round_timings.json')

    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as file:
            log_content = file.read()

        # Parse the log
        timing_data = parser.parse_round_timings(log_content)

        # Write to JSON file
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(timing_data, file, indent=2)

        # Print summary
        print("\nRound Timing Analysis:")
        print(f"Match Start Time: {timing_data['match_start_time']}")
        print(f"Total Match Duration: {timing_data['total_match_duration']} seconds")
        print(f"Total Rounds: {timing_data['total_rounds']}")
        print(f"Average Round Duration: {timing_data['average_round_duration']} seconds")
        print(f"Shortest Round: {timing_data['shortest_round']} seconds")
        print(f"Longest Round: {timing_data['longest_round']} seconds")

        print("\nRound Details:")
        for round_data in timing_data['rounds']:
            print(f"Round {round_data['round_number']}: "
                  f"{round_data['duration_seconds']} seconds "
                  f"({round_data['start_time']} - {round_data['end_time']})")

    except FileNotFoundError:
        print(f"Error: Could not find input file at {input_path}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()