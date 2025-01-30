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
            @input="handleRoundChange"
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue';
import type {
  TransformedPlayerStats,
  PlayerMatchStats,
  PlayerRoundStats,
    MatchStats
} from '@/data/types';

const props = defineProps<{
  killData: MatchStats | null;
}>();

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
const matchStats = ref<{[key: string]: PlayerMatchStats}>({});

const isVitalityCT = computed(() => currentRound.value < SIDE_SWITCH_ROUND);
const isNaviCT = computed(() => currentRound.value >= SIDE_SWITCH_ROUND);

const naviPlayers = computed(() =>
  allPlayerStats.value
    .filter(player => NAVI_PLAYERS.includes(player.name as typeof NAVI_PLAYERS[number]))
    .sort((a, b) => NAVI_PLAYERS.indexOf(a.name as typeof NAVI_PLAYERS[number]) -
                    NAVI_PLAYERS.indexOf(b.name as typeof NAVI_PLAYERS[number]))
);

const vitalityPlayers = computed(() =>
  allPlayerStats.value
    .filter(player => VITALITY_PLAYERS.includes(player.name as typeof VITALITY_PLAYERS[number]))
    .sort((a, b) => VITALITY_PLAYERS.indexOf(a.name as typeof VITALITY_PLAYERS[number]) -
                    VITALITY_PLAYERS.indexOf(b.name as typeof VITALITY_PLAYERS[number]))
);

const transformPlayerStats = (roundSnapshot: RoundSnapshot): TransformedPlayerStats[] => {
  const stats: TransformedPlayerStats[] = [];

  const processPlayer = (name: string) => {
    const roundStats = roundSnapshot.playerStats[name] || {
      kills: 0,
      deaths: 0,
      headshots: 0,
      headshotPercentage: 0,
      weapons: {}
    };

    stats.push({
      name,
      kills: roundStats.kills,
      deaths: roundStats.deaths,
      headshots: roundStats.headshots,
      headshotPercentage: roundStats.kills > 0 ? (roundStats.headshots / roundStats.kills * 100) : 0,
      weaponBreakdown: Object.entries(roundStats.weapons || {})
        .reduce((prev, curr) => prev[1] > curr[1] ? prev : curr, ['', 0])
        .filter(v => v !== 0)
        .join(': ') || '-'
    });
  };

  [...NAVI_PLAYERS, ...VITALITY_PLAYERS].forEach(processPlayer);

  return stats;
};

const handleRoundChange = () => {
  if (roundData.value && roundData.value.length > 0) {
    const selectedRoundData = roundData.value[currentRound.value - 1];
    if (selectedRoundData) {
      allPlayerStats.value = transformPlayerStats(selectedRoundData);
    }
  }
};

watchEffect(() => {
  if (props.killData?.roundStats) {
    roundData.value = props.killData.roundStats.map(round => ({
      roundNumber: round.roundNumber,
      playerStats: round.playerStats
    }));
    matchStats.value = props.killData.playerStats;
    handleRoundChange();
  }
});
</script>