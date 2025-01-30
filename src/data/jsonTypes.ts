import {KillEvent, Teams} from "@/data/types";

export interface MatchJsonResponse {
  teams: Teams;
  final_score: string;
  map: string;
  round_history: {
    round_number: number;
    winner_side: 'CT' | 'T';
    winner_team: string;
    score_after_round: string;
  }[];
  winner: string;
  total_rounds: number;
}

export interface KillJsonResponse {
  live_start_time: string;
  match_start_time: string | null;
  total_kills: number;
  total_rounds: number;
  player_stats: {
    [key: string]: {
      total_kills: number;
      deaths: number;
      headshots: number;
      headshot_percentage: number;
      team_kills?: number;
    };
  };
  kills: KillEvent[];
  round_stats: {
    round_number: number;
  }[];
}

export interface RoundJsonResponse {
  total_rounds: number;
  average_round_duration: number;
  shortest_round: number;
  longest_round: number;
  match_start_time: string;
  total_match_duration: number;
  rounds: {
    round_number: number;
    start_time: string;
    end_time: string;
    duration_seconds: number;
  }[];
}