<template>
  <div class="w-full">
    <h2 class="text-2xl font-bold mb-4 text-white">Scoreboard</h2>

    <div class="overflow-x-auto">
      <table class="min-w-full">
        <thead>
          <tr class="px-4 py-2 text-base font-semibold text-white">
            <th></th>
            <th class="text-center">Total Kills</th>
            <th class="text-center">Deaths</th>
            <th class="text-center">K/D Ratio</th>
            <th class="text-center">Headshots</th>
            <th class="text-center">HS %</th>
            <th class="text-center">Most Used Weapon</th>
          </tr>
        </thead>
        <tbody>
          <tr :class="[isNaviCT ? 'bg-sky-800/50' : 'bg-rose-700/50']">
            <td colspan="7" class="px-4 py-2 text-base font-bold text-white text-left">
              NAVI ({{ isNaviCT ? 'CT' : 'T' }})
            </td>
          </tr>
          <template v-for="player in getTeamPlayers(Team.Navi)" :key="player.name">
            <tr class="text-base text-white" :class="[isNaviCT ? 'bg-sky-400/50' : 'bg-rose-400/50']">
              <td class="text-left px-4 py-2 font-medium">{{ player.name }}</td>
              <td class="text-center">{{ player.kills }}</td>
              <td class="text-center">{{ player.deaths }}</td>
              <td class="text-center">{{ calculateKDRatio(player) }}</td>
              <td class="text-center">{{ player.headshots }}</td>
              <td class="text-center">{{ calculateHeadshotPercentage(player) }}%</td>
              <td class="text-center">{{ getPlayerMostUsedWeapon(player.name) }}</td>
            </tr>
          </template>

          <tr :class="[isVitalityCT ? 'bg-sky-800/50' : 'bg-rose-700/50']">
            <td colspan="7" class="px-4 py-2 text-base font-bold text-white text-left">
              Team Vitality ({{ isVitalityCT ? 'CT' : 'T' }})
            </td>
          </tr>
          <template v-for="player in getTeamPlayers(Team.Vitality)" :key="player.name">
            <tr class="text-base text-white" :class="[isVitalityCT ? 'bg-sky-400/50' : 'bg-rose-400/50']">
              <td class="text-left px-4 py-2 font-medium">{{ player.name }}</td>
              <td class="text-center">{{ player.kills }}</td>
              <td class="text-center">{{ player.deaths }}</td>
              <td class="text-center">{{ calculateKDRatio(player) }}</td>
              <td class="text-center">{{ player.headshots }}</td>
              <td class="text-center">{{ calculateHeadshotPercentage(player) }}%</td>
              <td class="text-center">{{ getPlayerMostUsedWeapon(player.name) }}</td>
            </tr>
          </template>
        </tbody>
      </table>

      <div class="mt-2">
        <div class="flex items-center gap-4">
          <span class="text-base font-bold text-white">
            RoundInformation: {{ currentRound }}/{{ roundNumber?.length || 1 }}
          </span>
          <input
            type="range"
            v-model="currentRound"
            :min="1"
            :max="roundNumber?.length || 1"
            class="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            @change="handleRoundChange"
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, watchEffect } from 'vue';
import type { MatchStats } from '@/data/types';
import { usePlayerStats } from '@/composables/usePlayerStats';
import { Team } from '@/data/teamsAndPlayers';

const SIDE_SWITCH_ROUND = 16;

const props = defineProps<{
  killData: MatchStats;
}>();

const {
  currentRound,
  roundNumber,
  allPlayerStats,
  calculateKDRatio,
  calculateHeadshotPercentage,
  getPlayerMostUsedWeapon,
  transformPlayerStats,
  getTeamPlayers
} = usePlayerStats(props.killData);

const isVitalityCT = computed(() => currentRound.value < SIDE_SWITCH_ROUND);
const isNaviCT = computed(() => currentRound.value >= SIDE_SWITCH_ROUND);

function handleRoundChange(event?: Event): void {
  if (event && event.target instanceof HTMLInputElement) {
    currentRound.value = parseInt(event.target.value, 10);
  }
  allPlayerStats.value = transformPlayerStats();
}

watchEffect(() => {
  if (props.killData.roundStats && Array.isArray(props.killData.roundStats)) {
    roundNumber.value = props.killData.roundStats.map(stat => stat.roundNumber);
    currentRound.value = currentRound.value || 1;
    handleRoundChange();
  }
});
</script>