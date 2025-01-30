<template>
  <div class="w-full rounded-lg">
    <div class="text-2xl font-bold flex flex-col items-center gap-4 text-center text-white mb-8">
      <img src="/img/Logo_Trophy.png" alt="blast_trophy" class="w-24 h-24 object-contain rounded-lg" />
      <h2>NAVI GGBET vs. Team Vitality</h2>
    </div>

    <RoundHistory :rounds="matchData.roundHistory" />

    <div class="flex items-center justify-center text-white mb-4 mt-8 gap-8">
      <div class="flex items-center gap-4">
        <div class="flex flex-col items-center gap-2 mr-28">
          <img src="/img/navi_logopng.png" alt="navi_logo" class="w-24 h-24" />
          <span class="text-lg font-semibold">{{ matchData.teams.CT }}</span>
        </div>
      </div>

      <span class="text-4xl font-bold">{{ matchData.finalScore }}</span>

      <div class="flex items-center gap-4">
        <div class="flex flex-col items-center gap-2 ml-28">
          <img src="/img/vitality-logo-yellow.png" alt="vitality_logo" class="w-24 h-24" />
          <span class="text-lg font-semibold">{{ matchData.teams.T }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import RoundHistory from './RoundHistory.vue';
import type { MatchSummaryData } from '@/data/types';

defineProps<{
  matchData: MatchSummaryData;
}>();
</script>