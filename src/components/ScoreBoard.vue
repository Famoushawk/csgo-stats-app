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
            Round: {{ currentRound }}/{{ roundNumber?.length || 1 }}
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
import { ref, computed, watchEffect, toRefs } from 'vue';
import type {
  MatchStats,
  KillEvent,
    PlayerStatsBase
} from '@/data/types';

enum Team {
  Navi = 'NAVI',
  Vitality = 'Vitality'
}

type NaviPlayer = 's1mple' | 'b1t' | 'electronic' | 'Boombl4' | 'Perfecto';
type VitalityPlayer = 'ZywOo' | 'apEX' | 'misutaaa' | 'Kyojin' | 'shox ';
type PlayerName = NaviPlayer | VitalityPlayer;

const NAVI_PLAYERS: readonly NaviPlayer[] = ['s1mple', 'b1t', 'electronic', 'Boombl4', 'Perfecto'] as const;
const VITALITY_PLAYERS: readonly VitalityPlayer[] = ['ZywOo', 'apEX', 'misutaaa', 'Kyojin', 'shox '] as const;
const SIDE_SWITCH_ROUND = 16;

interface Props {
  killData: MatchStats;
}

const props = defineProps<Props>();
const { killData } = toRefs(props);

const currentRound = ref<number>(1);
const roundNumber = ref<number[]>([]);
const allPlayerStats = ref<PlayerStatsBase[]>([]);

const isVitalityCT = computed((): boolean => currentRound.value < SIDE_SWITCH_ROUND);
const isNaviCT = computed((): boolean => currentRound.value >= SIDE_SWITCH_ROUND);

function getTeamPlayers<T extends Team>(team: T): PlayerStatsBase[] {
  const naviPlayers: readonly NaviPlayer[] = NAVI_PLAYERS;
  const vitalityPlayers: readonly VitalityPlayer[] = VITALITY_PLAYERS;

  return allPlayerStats.value
    .filter(player => {
      if (team === Team.Navi) {
        return naviPlayers.includes(player.name as NaviPlayer);
      }
      return vitalityPlayers.includes(player.name as VitalityPlayer);
    })
    .sort((a, b) => {
      if (team === Team.Navi) {
        return naviPlayers.indexOf(a.name as NaviPlayer) - naviPlayers.indexOf(b.name as NaviPlayer);
      }
      return vitalityPlayers.indexOf(a.name as VitalityPlayer) - vitalityPlayers.indexOf(b.name as VitalityPlayer);
    });
}

function calculateKDRatio(player: PlayerStatsBase): string {

  if (!player) {
    return '0.00';
  }

  if (player.deaths === 0) {
    return player.kills === 0 ? '0.00' : player.kills.toFixed(2);
  }

  const ratio = Math.max(0, player.kills) / Math.max(1, player.deaths);

  return ratio.toFixed(2);
}

function calculateHeadshotPercentage(player: PlayerStatsBase): string {
  return (player.kills > 0 ? (player.headshots / player.kills) * 100 : 0).toFixed(1);
}

function getPlayerMostUsedWeapon(playerName: PlayerName): string {
  const kills = killData.value.kills.filter(
    (kill: KillEvent): kill is KillEvent & { killer: { name: PlayerName } } =>
    kill.round <= currentRound.value && kill.killer.name === playerName
  );

  const weaponCounts: Record<string, number> = {};
  kills.forEach(kill => {
    weaponCounts[kill.weapon] = (weaponCounts[kill.weapon] || 0) + 1;
  });

  const mostUsedWeapon = Object.entries(weaponCounts)
    .sort(([, a], [, b]) => b - a)[0];

  return mostUsedWeapon ? `${mostUsedWeapon[0]}: ${mostUsedWeapon[1]}` : '-';
}

function transformPlayerStats(): PlayerStatsBase[] {
  const stats: PlayerStatsBase[] = [];

  const processPlayer = (name: PlayerName) => {
    const cumulativeStats: {
      kills: number;
      deaths: number;
      headshots: number;
      weapons: Record<string, number>;
    } = {
      kills: 0,
      deaths: 0,
      headshots: 0,
      weapons: {}
    };

    killData.value.kills.forEach((kill: KillEvent) => {
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

    const headshotPercentage = cumulativeStats.kills > 0
      ? (cumulativeStats.headshots / cumulativeStats.kills) * 100
      : 0;

    stats.push({
      name,
      kills: cumulativeStats.kills,
      deaths: cumulativeStats.deaths,
      headshots: cumulativeStats.headshots,
      headshotPercentage,
      weaponBreakdown: getPlayerMostUsedWeapon(name)
    });
  };

  [...NAVI_PLAYERS, ...VITALITY_PLAYERS].forEach(processPlayer);
  return stats;
}

function handleRoundChange(event?: Event): void {
  if (event && event.target instanceof HTMLInputElement) {
    currentRound.value = parseInt(event.target.value, 10);
  }
  allPlayerStats.value = transformPlayerStats();
}

watchEffect(() => {
  if (killData.value?.roundStats && Array.isArray(killData.value.roundStats)) {
    roundNumber.value = killData.value.roundStats.map(stat => stat.roundNumber);
    if (!currentRound.value) {
      currentRound.value = 1;
    }
    handleRoundChange();
  }
});
</script>