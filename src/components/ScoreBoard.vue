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
          <template v-for="player in naviPlayers" :key="player.name">
            <tr class="text-base text-white" :class="[isNaviCT ? 'bg-sky-400/50' : 'bg-rose-400/50']">
              <td class="text-left px-4 py-2 font-medium">{{ player.name }}</td>
              <td class="text-center">{{ player.kills }}</td>
              <td class="text-center">{{ player.deaths }}</td>
              <td class="text-center">{{ (player.kills / Math.max(player.deaths, 1)).toFixed(2) }}</td>
              <td class="text-center">{{ player.headshots }}</td>
              <td class="text-center">{{ player.headshotPercentage.toFixed(1) }}%</td>
              <td class="text-center">{{ player.weaponBreakdown }}</td>
            </tr>
          </template>

          <tr :class="[isVitalityCT ? 'bg-sky-800/50' : 'bg-rose-700/50']">
            <td colspan="7" class="px-4 py-2 text-base font-bold text-white text-left">
              Team Vitality ({{ isVitalityCT ? 'CT' : 'T' }})
            </td>
          </tr>
          <template v-for="player in vitalityPlayers" :key="player.name">
            <tr class="text-base text-white" :class="[isVitalityCT ? 'bg-sky-400/50' : 'bg-rose-400/50']">
              <td class="text-left px-4 py-2 font-medium">{{ player.name }}</td>
              <td class="text-center">{{ player.kills }}</td>
              <td class="text-center">{{ player.deaths }}</td>
              <td class="text-center">{{ (player.kills / Math.max(player.deaths, 1)).toFixed(2) }}</td>
              <td class="text-center">{{ player.headshots }}</td>
              <td class="text-center">{{ player.headshotPercentage.toFixed(1) }}%</td>
              <td class="text-center">{{ player.weaponBreakdown }}</td>
            </tr>
          </template>
        </tbody>
      </table>

      <div class="mt-2">
        <div class="flex items-center gap-4">
          <span class="text-base font-bold text-white">Round: {{ currentRound }}/{{ roundData?.length || 1 }}</span>
          <input
            type="range"
            v-model="currentRound"
            :min="1"
            :max="roundData?.length || 1"
            class="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            @change="handleRoundChange"
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watchEffect, toRefs } from 'vue';
import type {
  TransformedPlayerStats,
  PlayerRoundStats,
  MatchStats
} from '@/data/types';

const props = defineProps<{
  killData: MatchStats;
}>();

const { killData } = toRefs(props);

const NAVI_PLAYERS = ['s1mple', 'b1t', 'electronic', 'Boombl4', 'Perfecto'] as const;
const VITALITY_PLAYERS = ['ZywOo', 'apEX', 'misutaaa', 'Kyojin', 'shox '] as const;
const SIDE_SWITCH_ROUND = 16;

interface RoundSnapshot {
  roundNumber: number;
  playerStats: {
    [key: string]: PlayerRoundStats;
  };
}

const currentRound = ref(1);
const roundData = ref<RoundSnapshot[]>([]);
const allPlayerStats = ref<TransformedPlayerStats[]>([]);

const isVitalityCT = computed(() => currentRound.value < SIDE_SWITCH_ROUND);
const isNaviCT = computed(() => currentRound.value >= SIDE_SWITCH_ROUND);

const naviPlayers = computed(() => {
  return allPlayerStats.value
    .filter(player =>
      NAVI_PLAYERS.some(naviPlayer => naviPlayer === player.name)
    )
    .sort((a, b) =>
      NAVI_PLAYERS.indexOf(a.name as typeof NAVI_PLAYERS[number]) -
      NAVI_PLAYERS.indexOf(b.name as typeof NAVI_PLAYERS[number])
    );
});

const vitalityPlayers = computed(() => {
  return allPlayerStats.value
    .filter(player =>
      VITALITY_PLAYERS.some(vitalityPlayer => vitalityPlayer === player.name)
    )
    .sort((a, b) =>
      VITALITY_PLAYERS.indexOf(a.name as typeof VITALITY_PLAYERS[number]) -
      VITALITY_PLAYERS.indexOf(b.name as typeof VITALITY_PLAYERS[number])
    );
});

const transformPlayerStats = (): TransformedPlayerStats[] => {
  const stats: TransformedPlayerStats[] = [];

  const processPlayer = (name: string) => {
    let cumulativeStats = {
      kills: 0,
      deaths: 0,
      headshots: 0,
      weapons: {} as Record<string, number>
    };

    killData.value.kills.forEach(kill => {
      if (kill.round <= currentRound.value) {
        if (kill.killer.name === name) {
          cumulativeStats.kills++;
          if (kill.headshot) {
            cumulativeStats.headshots++;
          }
          cumulativeStats.weapons[kill.weapon] = (cumulativeStats.weapons[kill.weapon] || 0) + 1;
        }
        if (kill.victim.name === name) {
          cumulativeStats.deaths++;
        }
      }
    });

    const weaponBreakdown = Object.entries(cumulativeStats.weapons)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 1)
      .map(([weapon, count]) => `${weapon}: ${count}`)
      .join('') || '-';

    const headshotPercentage = cumulativeStats.kills > 0
      ? (cumulativeStats.headshots / cumulativeStats.kills) * 100
      : 0;

    stats.push({
      name,
      kills: cumulativeStats.kills,
      deaths: cumulativeStats.deaths,
      headshots: cumulativeStats.headshots,
      headshotPercentage,
      weaponBreakdown
    });
  };

  [...NAVI_PLAYERS, ...VITALITY_PLAYERS].forEach(processPlayer);
  return stats;
};

const handleRoundChange = (event?: Event) => {
  if (event && event.target instanceof HTMLInputElement) {
    currentRound.value = parseInt(event.target.value, 10);
  }

  allPlayerStats.value = transformPlayerStats();
};

watchEffect(() => {
  if (killData.value?.roundStats && Array.isArray(killData.value.roundStats)) {
    roundData.value = killData.value.roundStats;

    if (!currentRound.value) {
      currentRound.value = 1;
    }

    handleRoundChange();
  }
});
</script>