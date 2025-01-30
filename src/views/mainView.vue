<template>
  <div class="flex flex-col gap-8 w-full max-w-7xl mx-auto p-8">

    <MatchSummary v-if="matchData" :match-data="matchData" />

    <PlayerStats :player-data="playerData" />

    <RoundAnalysis :round-data="roundData" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import MatchSummary from '@/components/MatchSummary.vue';
import PlayerStats from '@/components/PlayerStats.vue';
import RoundAnalysis from '@/components/RoundAnalysis.vue';
import type { MatchSummaryData } from '@/data/types';

export default defineComponent({
  name: 'MainView',
  components: {
    MatchSummary,
    PlayerStats,
    RoundAnalysis
  },
  setup() {
    const matchData = ref<MatchSummaryData>({
      teams: {
        CT: 'NAVI GGBET',
        T: 'Team Vitality'
      },
      final_score: '6:16',
      map: 'de_nuke',
      round_history: [],
      winner: '',
      total_rounds: 0
    });

    const killData = ref({});
    const playerData = ref({});
    const roundData = ref({
      averageRoundDuration: 0,
      totalRounds: 0,
      matchDuration: '0:00',
      rounds: []
    });

    onMounted(async () => {
      try {
        const [matchResponse, killResponse, playerResponse, roundResponse] = await Promise.all([
          fetch('/data/match_summary.json'),
          fetch('/data/kill_stats.json'),
          fetch('/data/player_accuracy_stats.json'),
          fetch('/data/round_timings.json')
        ]);

        const matchJson = await matchResponse.json();
        const killJson = await killResponse.json();
        const playerJson = await playerResponse.json();
        const roundJson = await roundResponse.json();

        // Transform data as needed
        matchData.value = {
          teams: matchJson.teams,
          final_score: matchJson.final_score,
          map: matchJson.map,
          round_history: matchJson.round_history || [],
          winner: matchJson.winner || '',
          total_rounds: matchJson.total_rounds || 0
        };

        console.log('Match data loaded:', matchData.value); // Debug log

        killData.value = killJson;
        playerData.value = playerJson;
        roundData.value = roundJson;
      } catch (error) {
        console.error('Error loading data:', error);
      }
    });

    return {
      matchData,
      killData,
      playerData,
      roundData
    };
  }
});
</script>