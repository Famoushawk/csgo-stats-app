<template>
  <div v-if="roundData" class="rounded-lg text-center text-white mt-8">
    <h2 class="text-2xl font-bold mb-4">RoundInformation Analysis</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div>
        <h3 class="text-lg font-semibold">Average RoundInformation Duration</h3>
        <p class="text-3xl">{{ formatDuration(roundData.averageRoundDuration) }}s</p>
      </div>
      <div>
        <h3 class="text-lg font-semibold">Total Rounds</h3>
        <p class="text-3xl">{{ roundData.totalRounds }}</p>
      </div>
      <div>
        <h3 class="text-lg font-semibold">Match Duration</h3>
        <p class="text-3xl">{{ formatTime(roundData.totalMatchDuration) }}</p>
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
      <Bar
        v-if="roundChartData"
        :data="roundChartData"
        :options="chartOptions"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { formatTime } from '@/utils/timeUtils';
import { createRoundDurationChartData, createRoundDurationChartOptions } from '@/utils/chartUtils';
import type { RoundTimings, MatchSummaryData } from '@/data/types';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const props = withDefaults(defineProps<{
  roundData?: RoundTimings;
  matchData?: MatchSummaryData;
}>(), {
  roundData: undefined,
});

const formatDuration = (value: number | undefined): string => {
  if (typeof value === 'number') {
    return value.toFixed(1);
  }
  return '0.0';
};

const roundChartData = computed(() => {
  if (!props.roundData?.rounds) return null;
  // Convert undefined to null for type compatibility
  return createRoundDurationChartData(props.roundData.rounds, props.matchData ?? null);
});

const chartOptions = computed(() => {
  if (!props.roundData?.rounds) return {};
  return createRoundDurationChartOptions(props.roundData.rounds, props.matchData ?? null);
});
</script>