export type TeamSide = 'CT' | 'T';

export interface MatchSummaryData {
  map: string;
  final_score: string;
  winner: string;
  teams: {
    CT: string;
    T: string;
  };
  total_rounds: number;
  round_history: Array<{
    round_number: number;
    winner_side: TeamSide;
    winner_team: string;
    score_after_round: string;
  }>;
}