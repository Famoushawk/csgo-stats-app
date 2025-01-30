export interface MatchData {
  team1Name: string;
  team2Name: string;
  team1Score: number;
  team2Score: number;
  team1Logo: string;
  team2Logo: string;
  mapName: string;
}

export interface KillData {
  totalKills: number;
  headshots: number;
  bodyShots: number;
  legShots: number;
  weaponKills: Record<string, number>;
}

export interface PlayerStats {
  name: string;
  kills: number;
  deaths: number;
  accuracy: number;
  headshotPercentage: number;
}

export interface PlayerData {
  players: PlayerStats[];
}

export interface Round {
  roundNumber: number;
  startTime: string;
  endTime: string;
  durationSeconds: number;
}

export interface RoundData {
  totalRounds: number;
  averageRoundDuration: number;
  shortestRound: number;
  longestRound: number;
  matchStartTime: string;
  totalMatchDuration: number;
  rounds: Round[];
}

export interface RoundHistoryData {
  round_number: number;
  winner_side: 'CT' | 'T';
  winner_team: string;
  score_after_round: string;
  win_condition: 'explosion' | 'defuse' | 'elimination';
}

export interface Teams {
  CT: string;
  T: string;
}

export interface MatchSummaryData {
  teams: Teams;
  final_score: string;
  round_history: RoundHistoryData[];
  map: string;
  winner: string;
  total_rounds: number;
}

