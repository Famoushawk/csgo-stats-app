<template>
  <div v-if="roundData" class="rounded-lg text-center text-white">
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
    <div class="h-96">
      <Bar v-if="roundChartData" :data="roundChartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { formatTime } from '@/utils/timeUtils';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface Round {
  start_time: string;
  end_time: string;
  duration_seconds: number;
  round_number: number;
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

const props = withDefaults(defineProps<{
  roundData?: RoundData;
}>(), {
  roundData: undefined
});

const formatDuration = (value: number | undefined): string => {
  if (typeof value === 'number') {
    return value.toFixed(1);
  }
  return '0.0';
};

const roundChartData = computed(() => {
  if (!props.roundData?.rounds) return null;

  return {
    labels: props.roundData.rounds.map(round => `Round ${round.round_number}`),
    datasets: [{
      label: 'Round Duration',
      data: props.roundData.rounds.map(round => round.duration_seconds),
      backgroundColor: '#4F46E5',
      borderColor: '#4338CA',
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
      display: true,
      position: 'top' as const,
      labels: {
        color: 'white'
      }
    },
    tooltip: {
      callbacks: {
        label: (context: any) => `Duration: ${context.raw} seconds`
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
</script>