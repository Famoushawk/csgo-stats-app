<template>
  <div v-if="roundData" class="rounded-lg text-center text-white mt-8">
    <h2 class="text-2xl font-bold mb-4">Round Analysis</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div>
        <h3 class="text-lg font-semibold">Average Round Duration</h3>
        <p class="text-3xl">{{ formatDuration(roundData.average_round_duration) }}s</p>
      </div>
      <div>
        <h3 class="text-lg font-semibold">Total Rounds</h3>
        <p class="text-3xl">{{ roundData.total_rounds }}</p>
      </div>
      <div>
        <h3 class="text-lg font-semibold">Match Duration</h3>
        <p class="text-3xl">{{ formatTime(roundData.total_match_duration) }}</p>
      </div>
    </div>

    <!-- Legend -->
    <div class="flex justify-end gap-4 mb-4">
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 bg-sky-400/50 rounded"></div>
        <span class="text-sm">CT Win</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 bg-rose-400/50 rounded"></div>
        <span class="text-sm">T Win</span>
      </div>
    </div>

    <div class="h-96">
      <Bar v-if="roundChartData" :data="roundChartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { formatTime } from '@/utils/timeUtils';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface Round {
  start_time: string;
  end_time: string;
  duration_seconds: number;
  round_number: number;
  winner_side?: 'CT' | 'T';
}

interface RoundData {
  total_rounds: number;
  average_round_duration: number;
  shortest_round: number;
  longest_round: number;
  match_start_time: string;
  total_match_duration: number;
  rounds: Round[];
}

interface RoundHistory {
  round_number: number;
  winner_side: 'CT' | 'T';
  winner_team: string;
  score_after_round: string;
}

interface MatchData {
  round_history: RoundHistory[];
}

const props = withDefaults(defineProps<{
  roundData?: RoundData;
}>(), {
  roundData: undefined
});

const matchData = ref<MatchData | null>(null);

const formatDuration = (value: number | undefined): string => {
  if (typeof value === 'number') {
    return value.toFixed(1);
  }
  return '0.0';
};

const roundChartData = computed(() => {
  if (!props.roundData?.rounds || !matchData.value) return null;

  const roundsWithWinners = props.roundData.rounds.map(round => {
    const matchRound = matchData.value?.round_history.find(
      r => r.round_number === round.round_number
    );
    return {
      ...round,
      winner_side: matchRound?.winner_side
    };
  });

  return {
    labels: roundsWithWinners.map(round => `Round ${round.round_number}`),
    datasets: [{
      label: 'Round Duration',
      data: roundsWithWinners.map(round => round.duration_seconds),
      backgroundColor: roundsWithWinners.map(round =>
        round.winner_side === 'CT' ? 'rgba(56, 189, 248, 0.5)' : 'rgba(251, 113, 133, 0.5)'
      ),
      borderColor: roundsWithWinners.map(round =>
        round.winner_side === 'CT' ? 'rgb(56, 189, 248)' : 'rgb(251, 113, 133)'
      ),
      borderWidth: 1,
      borderRadius: 4
    }]
  };
});

const chartOptions = {
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
          const round = props.roundData?.rounds[roundIndex];
          const winner = matchData.value?.round_history.find(
            r => r.round_number === round?.round_number
          );
          return [
            `Duration: ${context.raw} seconds`,
            `Winner: ${winner?.winner_team || 'Unknown'}`
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
};

onMounted(async () => {
  try {
    const response = await fetch('/data/match_summary.json');
    const data = await response.json();
    matchData.value = data;
  } catch (error) {
    console.error('Error loading match data:', error);
  }
});
</script>