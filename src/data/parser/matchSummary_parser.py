import re
import json
import os
from typing import Dict, Optional


class MatchStatusParser:
    def __init__(self):
        self.timestamp_pattern = r'^(\d{2}/\d{2}/\d{2}\d{2} - \d{2}:\d{2}:\d{2}):'

    def determine_round_winner(self, content: str) -> Optional[str]:
        """Determine round winner based on SFUI notices or bomb events"""
        if '"SFUI_Notice_CTs_Win"' in content or '"SFUI_Notice_Bomb_Defused"' in content:
            return "CT"
        elif '"SFUI_Notice_Terrorists_Win"' in content or '"SFUI_Notice_Target_Bombed"' in content:
            return "T"
        return None

    def parse_match_status(self, log_content: str) -> Dict:
        lines = log_content.strip().split('\n')

        # Initialize match status
        match_status = {
            "current_round": 0,
            "score": {"CT": 0, "T": 0},
            "teams": {"CT": "", "T": ""},
            "rounds": [],
            "map": "",
            "round_history": []
        }

        current_round_data = {
            "round_number": 1,
            "winner": None,
            "end_reason": None
        }

        for line in lines:
            timestamp_match = re.match(self.timestamp_pattern, line)
            if not timestamp_match:
                continue

            timestamp = timestamp_match.group(1)
            content = line[timestamp_match.end():].strip()

            # Check for round winner first
            round_winner = self.determine_round_winner(content)
            if round_winner:
                current_round_data["winner"] = round_winner
                continue

            # Parse team scores
            team_score_match = re.match(r'Team "(CT|TERRORIST)" scored "(\d+)" with "(\d+)" players', content)
            if team_score_match:
                team, score, players = team_score_match.groups()
                match_status["score"]["CT" if team == "CT" else "T"] = int(score)
                continue

            # Parse team names
            team_playing_match = re.match(r'MatchStatus: Team playing "(CT|TERRORIST)": (.+)', content)
            if team_playing_match:
                team, name = team_playing_match.groups()
                match_status["teams"]["CT" if team == "CT" else "T"] = name
                continue

            # Parse match status line
            status_match = re.match(r'MatchStatus: Score: (\d+):(\d+) on map "([^"]+)" RoundsPlayed: (-?\d+)', content)
            if status_match:
                ct_score, t_score, map_name, rounds_played = status_match.groups()
                match_status["score"]["CT"] = int(ct_score)
                match_status["score"]["T"] = int(t_score)
                match_status["map"] = map_name
                match_status["current_round"] = max(1, int(rounds_played))
                continue

            # Parse round end
            if 'World triggered "Round_End"' in content:
                if current_round_data["winner"]:
                    winning_team = match_status["teams"][current_round_data["winner"]]
                    round_summary = {
                        "round_number": match_status["current_round"],
                        "winner_side": current_round_data["winner"],
                        "winner_team": winning_team,
                        "score_after_round": f"{match_status['score']['CT']}:{match_status['score']['T']}"
                    }
                    match_status["round_history"].append(round_summary)

                # Reset for next round
                current_round_data = {
                    "round_number": match_status["current_round"] + 1,
                    "winner": None,
                    "end_reason": None
                }
                continue

        # Format final output
        match_summary = {
            "map": match_status["map"],
            "final_score": f"{match_status['score']['CT']}:{match_status['score']['T']}",
            "winner": match_status["teams"]["CT"] if match_status["score"]["CT"] > match_status["score"]["T"] else
            match_status["teams"]["T"],
            "teams": {
                "CT": match_status["teams"]["CT"],
                "T": match_status["teams"]["T"]
            },
            "total_rounds": match_status["current_round"],
            "round_history": match_status["round_history"]
        }

        return match_summary


def main():
    parser = MatchStatusParser()

    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct paths relative to the script location
    input_path = os.path.join(script_dir, '..', 'NAVIvsVitaGF-Nuke.txt')

    # Navigate up to project root then into public/data
    output_path = os.path.join(script_dir, '..', '..', '..', 'public', 'data', 'match_summary.json')

    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as file:
            log_content = file.read()

        # Parse the log
        match_summary = parser.parse_match_status(log_content)

        # Write to JSON file
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(match_summary, file, indent=2)

        print("\nMatch Summary:")
        print(f"Map: {match_summary['map']}")
        print(f"Final Score: {match_summary['final_score']}")
        print(f"Winner: {match_summary['winner']}")
        print(f"\nTeams:")
        print(f"CT: {match_summary['teams']['CT']}")
        print(f"T: {match_summary['teams']['T']}")
        print(f"\nTotal Rounds: {match_summary['total_rounds']}")

        print("\nRound History:")
        for round_data in match_summary['round_history']:
            print(f"Round {round_data['round_number']}: "
                  f"{round_data['winner_team']} wins "
                  f"(Score: {round_data['score_after_round']})")

    except FileNotFoundError:
        print(f"Error: Could not find input file at {input_path}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()