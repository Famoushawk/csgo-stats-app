// Player related types
export interface WeaponStats {
  [weaponName: string]: number;
}

export interface PlayerStatsBase {
  kills: number;
  deaths: number;
  headshots: number;
  headshotPercentage: number;
  weaponBreakdown: string;
  name: string;
}

// Kill related types
export interface KillEvent {
  round: number;
  timestamp: string;
  killer: {
    name: string;
    team: Team;
  };
  victim: {
    name: string;
    team: Team;
  };
  weapon: string;
  headshot: boolean;
}

// Round related types
export type Team = 'CT' | 'T';
export type WinCondition = 'elimination' | 'defuse' | 'explosion' | 'time';

export interface Round {
  roundNumber: number;
  startTime: string;
  endTime: string;
  durationSeconds: number;
}

export interface RoundWinner {
  roundNumber: number;
  winnerSide: Team;
  winnerTeam: string;
  scoreAfterRound: string;
  winCondition: WinCondition;
}

// Match related types
export interface Teams {
  CT: string;
  T: string;
}

export interface MatchSummaryData {
  map: string;
  finalScore: string;
  winner: string;
  teams: Teams;
  totalRounds: number;
  roundHistory: RoundWinner[];
}

export interface RoundTimings {
  totalRounds: number;
  averageRoundDuration: number;
  shortestRound: number;
  longestRound: number;
  matchStartTime: string;
  totalMatchDuration: number;
  rounds: Round[];
}

// Match statistics
export interface MatchStats {
  liveStartTime: string;
  matchStartTime: string | null;
  totalKills: number;
  totalRounds: number;
  kills: KillEvent[];
  roundStats: {
    roundNumber: number;
  }[];
}