<template>
  <div class="flex flex-col gap-4">
    <!-- Existing round circles -->
    <div class="w-full flex flex-wrap gap-2 justify-center">
      <div
        v-for="round in rounds"
        :key="round.round_number"
        class="w-8 h-8 rounded-full flex items-center justify-center cursor-pointer"
        :class="round.winner_side === 'CT' ? 'bg-sky-400/50' : 'bg-rose-400/50'"
        :title="`Round ${round.round_number}: ${round.winner_team} wins (${round.score_after_round})`"
      >
        <span class="text-xs text-white text-sm font-bold">{{ round.round_number }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { RoundHistoryData } from 'src/data/types';



defineProps<{
  rounds: RoundHistoryData[];
}>();

</script>