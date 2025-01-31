<template>
  <div class="flex flex-col gap-8 w-full max-w-7xl mx-auto p-8">
    <MatchSummary v-if="matchData" :match-data="matchData" />
    <ScoreBoard v-if="killData.roundStats.length > 0" :kill-data="killData"/>
    <RoundAnalysis :round-data="roundData" :match-data="matchData"
    />
  </div>
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue';
import MatchSummary from '@/components/MatchSummary.vue';
import ScoreBoard from '@/components/ScoreBoard.vue';
import RoundAnalysis from '@/components/RoundAnalysis.vue';
import type {MatchStats, MatchSummaryData, RoundTimings, WinCondition} from '@/data/types';
import type {KillJsonResponse, MatchJsonResponse, RoundJsonResponse} from "@/data/jsonTypes";

const matchData = ref<MatchSummaryData>({
  teams: {
    CT: 'NAVI GGBET',
    T: 'Team Vitality'
  },
  finalScore: '',
  map: 'de_nuke',
  roundHistory: [],
  winner: '',
  totalRounds: 0
});

const killData = ref<MatchStats>({
  liveStartTime: '',
  matchStartTime: null,
  totalKills: 0,
  totalRounds: 0,
  kills: [],
  roundStats: []
});
const roundData = ref<RoundTimings>({
  totalRounds: 0,
  averageRoundDuration: 0,
  shortestRound: 0,
  longestRound: 0,
  matchStartTime: '',
  totalMatchDuration: 0,
  rounds: []
});

onMounted(async () => {
  try {
    const [matchResponse, killResponse, roundResponse] = await Promise.all([
      fetch('/data/match_summary.json'),
      fetch('/data/kill_stats.json'),
      fetch('/data/round_timings.json')
    ]);

    const matchJson = await matchResponse.json() as MatchJsonResponse;
    const killJson = await killResponse.json() as KillJsonResponse;
    const roundJson = await roundResponse.json() as RoundJsonResponse;

    matchData.value = {
      teams: matchJson.teams,
      finalScore: matchJson.final_score,
      map: matchJson.map,
      roundHistory: matchJson.round_history.map((round) => ({
        roundNumber: round.round_number,
        winnerSide: round.winner_side,
        winnerTeam: round.winner_team,
        scoreAfterRound: round.score_after_round,
        winCondition: 'elimination' as WinCondition,
        startTime: '',
        endTime: '',
        durationSeconds: 0
      })),
      winner: matchJson.winner,
      totalRounds: matchJson.total_rounds
    };

    killData.value = {
      liveStartTime: killJson.live_start_time,
      matchStartTime: killJson.match_start_time,
      totalKills: killJson.total_kills,
      totalRounds: killJson.total_rounds,
      kills: killJson.kills,
      roundStats: killJson.round_stats.map(round => ({
        roundNumber: round.round_number
      }))
    };

    roundData.value = {
      totalRounds: roundJson.total_rounds,
      averageRoundDuration: roundJson.average_round_duration,
      shortestRound: roundJson.shortest_round,
      longestRound: roundJson.longest_round,
      matchStartTime: roundJson.match_start_time,
      totalMatchDuration: roundJson.total_match_duration,
      rounds: roundJson.rounds.map((round) => ({
        roundNumber: round.round_number,
        startTime: round.start_time,
        endTime: round.end_time,
        durationSeconds: round.duration_seconds,
        winnerSide: 'CT',
        winnerTeam: '',
        scoreAfterRound: '',
        winCondition: 'elimination' as WinCondition
      }))
    };

  } catch (error) {
    console.error('Error loading data:', error);
  }
});
</script>