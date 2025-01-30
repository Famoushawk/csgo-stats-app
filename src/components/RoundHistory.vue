<template>
  <div class="flex flex-col gap-4">
    <div class="w-full flex flex-wrap gap-2 justify-center">
      <div
        v-for="round in rounds"
        :key="round.roundNumber"
        class="w-8 h-8 rounded-full flex items-center justify-center cursor-pointer"
        :class="round.winnerSide === 'CT' ? 'bg-sky-400/50' : 'bg-rose-400/50'"
        :title="`Round ${round.roundNumber}: ${round.winnerTeam} wins (${round.scoreAfterRound})`"
      >
        <span class="text-xs text-white text-sm font-bold">{{ round.roundNumber }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { RoundInformation } from '@/data/types';

defineProps<{
  rounds: RoundInformation[];
}>();
</script>