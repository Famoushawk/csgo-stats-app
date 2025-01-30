// Player related types
export interface PlayerStatsBase {
  kills: number;
  deaths: number;
  headshots: number;
  headshotPercentage: number;
  weaponBreakdown: string;
  name: string;
}

interface Player {
  name: string;
  team: Team;
}

// Kill related types
export interface KillEvent {
  round: number;
  timestamp: string;
  killer: Player;
  victim: Player;
  weapon: string;
  headshot: boolean;
}

// RoundInformation related types
export type Team = 'CT' | 'T';
export type WinCondition = 'elimination' | 'defuse' | 'explosion' | 'time';

export interface RoundInformation {
  roundNumber: number;
  startTime: string;
  endTime: string;
  durationSeconds: number;
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
  roundHistory: RoundInformation[];
}

export interface RoundTimings {
  totalRounds: number;
  averageRoundDuration: number;
  shortestRound: number;
  longestRound: number;
  matchStartTime: string;
  totalMatchDuration: number;
  rounds: RoundInformation[];
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