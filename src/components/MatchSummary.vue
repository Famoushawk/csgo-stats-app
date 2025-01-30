<template>
  <div class="w-full rounded-lg">

    <div class="text-2xl font-bold flex flex-col items-center gap-4 text-center text-white mb-8">
    <img src="../../public/img/Logo_Trophy.png" alt="blast_trophy" class="w-24 h-24 object-contain rounded-lg" />
    <h2 >NAVI GGBET vs. Team Vitality</h2>
    </div>

    <RoundHistory :rounds="matchData.round_history" />

    <div class="flex items-center justify-between items-center text-white mb-8">
      <div class="flex flex-col pl-8 pt-4 gap-4">
        <img src="../../public/img/navi_logopng.png" alt="navi_logo" class="w-24 h-24" />
        <span class="text-lg font-semibold">{{ matchData.teams.CT }}</span>
      </div>

      <div class="flex flex-col">
        <span class="text-4xl font-bold">{{ matchData.final_score }}</span>
      </div>

      <div class="flex flex-col pr-8 pt-4 gap-4">
        <img src="../../public/img/vitality-logo-yellow.png" alt="vitality_logo" class="w-24 h-24" />
        <span class="text-lg font-semibold">{{ matchData.teams.T }}</span>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import RoundHistory from './RoundHistory.vue';
import type { RoundHistoryData } from 'src/data/types';

interface Teams {
  CT: string;
  T: string;
}

interface MatchSummaryData {
  teams: Teams;
  final_score: string;
  round_history: RoundHistoryData[];
}

defineProps<{
  matchData: MatchSummaryData;
}>();
</script>