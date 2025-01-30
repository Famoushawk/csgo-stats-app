import type { Round, RoundWithWinner, MatchSummaryData } from '@/data/types';
import type { ChartOptions, ChartData } from 'chart.js';

interface RoundDurationChartData extends ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    backgroundColor: string[];
    borderColor: string[];
    borderWidth: number;
    borderRadius: number;
  }[];
}

// Color constants
const COLORS = {
  CT: {
    background: 'rgba(56, 189, 248, 0.5)',
    border: 'rgb(56, 189, 248)'
  },
  T: {
    background: 'rgba(251, 113, 133, 0.5)',
    border: 'rgb(251, 113, 133)'
  }
} as const;

export const createRoundDurationChartData = (
  rounds: Round[],
  matchData: MatchSummaryData | null
): RoundDurationChartData | null => {
  if (!rounds || !matchData) return null;

  const roundsWithWinners: RoundWithWinner[] = rounds.map(round => {
    const matchRound = matchData.roundHistory.find(
      r => r.roundNumber === round.roundNumber
    );
    return {
      ...round,
      winnerSide: matchRound?.winnerSide
    };
  });

  return {
    labels: roundsWithWinners.map(round => `Round ${round.roundNumber}`),
    datasets: [{
      label: 'Round Duration',
      data: roundsWithWinners.map(round => round.durationSeconds),
      backgroundColor: roundsWithWinners.map(round =>
        round.winnerSide === 'CT' ? COLORS.CT.background : COLORS.T.background
      ),
      borderColor: roundsWithWinners.map(round =>
        round.winnerSide === 'CT' ? COLORS.CT.border : COLORS.T.border
      ),
      borderWidth: 1,
      borderRadius: 4
    }]
  };
};

export const createRoundDurationChartOptions = (
  rounds: Round[],
  matchData: MatchSummaryData | null
): ChartOptions => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: (context: any) => {
          const roundIndex = context.dataIndex;
          const round = rounds[roundIndex];
          const winner = matchData?.roundHistory.find(
            r => r.roundNumber === round?.roundNumber
          );
          return [
            `Duration: ${context.raw} seconds`,
            `Winner: ${winner?.winnerTeam || 'Unknown'}`
          ];
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(255, 255, 255, 0.1)'
      },
      ticks: {
        color: 'white'
      },
      title: {
        display: true,
        text: 'Duration (seconds)',
        color: 'white'
      }
    },
    x: {
      grid: {
        color: 'rgba(255, 255, 255, 0.1)'
      },
      ticks: {
        color: 'white',
        maxRotation: 45,
        minRotation: 45
      }
    }
  }
});