<template>
  <div class="w-full">
    <h2 class="text-2xl font-bold mb-4 text-white">Scoreboard</h2>

    <!-- Player Stats Table -->
    <div class="overflow-x-auto">
      <table class="min-w-full">
        <thead>
          <tr class="px-6 py-3 text-base font-semibold text-white">
            <th>Player</th>
            <th>Total Kills</th>
            <th>Deaths</th>
            <th>K/D Ratio</th>
            <th>Headshots</th>
            <th>HS %</th>
            <th>Most Used Weapon</th>
          </tr>
        </thead>
        <tbody>
          <!-- NAVI Players -->
          <tr :class="[isNaviCT ? 'bg-sky-800/50' : 'bg-rose-700/50']">
            <td colspan="7" class="px-6 py-2 text-sm font-bold text-white">
              NAVI ({{ isNaviCT ? 'CT' : 'T' }})
            </td>
          </tr>
          <template v-for="player in naviPlayers" :key="player.name">
            <tr class="px-6 py-4 text-base text-white" :class="[isNaviCT ? 'bg-sky-400/50' : 'bg-rose-400/50']">
              <td class="px-6 py-4 text-base font-medium text-white">{{ player.name }}</td>
              <td>{{ player.kills }}</td>
              <td>{{ player.deaths }}</td>
              <td>{{ (player.kills / Math.max(player.deaths, 1)).toFixed(2) }}</td>
              <td>{{ player.headshots }}</td>
              <td>{{ player.headshotPercentage.toFixed(1) }}%</td>
              <td>{{ player.weaponBreakdown }}</td>
            </tr>
          </template>

          <!-- Vitality Players -->
          <tr :class="[isVitalityCT ? 'bg-sky-800/50' : 'bg-rose-700/50']">
            <td colspan="7" class="px-6 py-2 text-sm font-bold text-white">
              Team Vitality ({{ isVitalityCT ? 'CT' : 'T' }})
            </td>
          </tr>
          <template v-for="player in vitalityPlayers" :key="player.name">
            <tr class="px-6 py-4 text-base text-white" :class="[isVitalityCT ? 'bg-sky-400/50' : 'bg-rose-400/50']">
              <td class="px-6 py-4 text-base font-medium text-white">{{ player.name }}</td>
              <td>{{ player.kills }}</td>
              <td>{{ player.deaths }}</td>
              <td>{{ (player.kills / Math.max(player.deaths, 1)).toFixed(2) }}</td>
              <td>{{ player.headshots }}</td>
              <td>{{ player.headshotPercentage.toFixed(1) }}%</td>
              <td>{{ player.weaponBreakdown }}</td>
            </tr>
          </template>
        </tbody>
      </table>

    <div class="mt-2">
      <div class="flex items-center gap-4">
        <span class="text-base font-medium text-white">Round: {{ currentRound }}/{{ roundData?.length || 1 }}</span>
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

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';

interface WeaponStats {
  [key: string]: number;
}

interface PlayerStatsData {
  total_kills: number;
  deaths: number;
  headshots: number;
  headshot_percentage: number;
  weapons: WeaponStats;
}

interface RoundSnapshot {
  round_number: number;
  player_stats: {
    [key: string]: PlayerStatsData;
  };
}

interface TransformedPlayerStats {
  name: string;
  kills: number;
  deaths: number;
  headshots: number;
  headshotPercentage: number;
  weaponBreakdown: string;
}

const NAVI_PLAYERS = ['s1mple', 'b1t', 'electronic', 'Boombl4', 'Perfecto'];
const VITALITY_PLAYERS = ['ZywOo', 'apEX', 'misutaaa', 'Kyojin', 'shox '];
const SIDE_SWITCH_ROUND = 16;

export default defineComponent({
  name: 'PlayerStats',
  setup() {
    const currentRound = ref(1);
    const roundData = ref<RoundSnapshot[]>([]);
    const allPlayerStats = ref<TransformedPlayerStats[]>([]);

    // Compute team sides based on current round
    const isVitalityCT = computed(() => {
      return currentRound.value < SIDE_SWITCH_ROUND;
    });

    const isNaviCT = computed(() => {
      return currentRound.value >= SIDE_SWITCH_ROUND;
    });

    const naviPlayers = computed(() => {
      return allPlayerStats.value.filter(player => NAVI_PLAYERS.includes(player.name))
        .sort((a, b) => NAVI_PLAYERS.indexOf(a.name) - NAVI_PLAYERS.indexOf(b.name));
    });

    const vitalityPlayers = computed(() => {
      return allPlayerStats.value.filter(player => VITALITY_PLAYERS.includes(player.name))
        .sort((a, b) => VITALITY_PLAYERS.indexOf(a.name) - VITALITY_PLAYERS.indexOf(b.name));
    });

    const transformPlayerStats = (roundSnapshot: RoundSnapshot): TransformedPlayerStats[] => {
      const stats: TransformedPlayerStats[] = [];

      // Process all NAVI players
      NAVI_PLAYERS.forEach(name => {
        const playerStats = roundSnapshot.player_stats[name] || {
          total_kills: 0,
          deaths: 0,
          headshots: 0,
          headshot_percentage: 0,
          weapons: {}
        };

        stats.push({
          name,
          kills: playerStats.total_kills,
          deaths: playerStats.deaths,
          headshots: playerStats.headshots,
          headshotPercentage: playerStats.headshot_percentage,
          weaponBreakdown: Object.entries(playerStats.weapons || {})
            .reduce((prev, curr) => prev[1] > curr[1] ? prev : curr, ['', 0])
            .filter(v => v !== 0)
            .join(': ') || '-'
        });
      });

      // Process all Vitality players
      VITALITY_PLAYERS.forEach(name => {
        const playerStats = roundSnapshot.player_stats[name] || {
          total_kills: 0,
          deaths: 0,
          headshots: 0,
          headshot_percentage: 0,
          weapons: {}
        };

        stats.push({
          name,
          kills: playerStats.total_kills,
          deaths: playerStats.deaths,
          headshots: playerStats.headshots,
          headshotPercentage: playerStats.headshot_percentage,
          weaponBreakdown: Object.entries(playerStats.weapons || {})
            .reduce((prev, curr) => prev[1] > curr[1] ? prev : curr, ['', 0])
            .filter(v => v !== 0)
            .join(': ') || '-'
        });
      });

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

    onMounted(async () => {
      try {
        const response = await fetch('/data/kill_stats.json');
        const data = await response.json();

        if (data.round_stats) {
          roundData.value = data.round_stats;
          handleRoundChange(); // Initialize with first round stats
        }
      } catch (error) {
        console.error('Error loading player stats:', error);
      }
    });

    return {
      currentRound,
      roundData,
      naviPlayers,
      vitalityPlayers,
      handleRoundChange,
      isVitalityCT,
      isNaviCT
    };
  }
});
</script>