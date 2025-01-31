import { ref } from 'vue';
import type { PlayerStatsBase, KillEvent, MatchStats } from '@/data/types';
import {NAVI_PLAYERS, VITALITY_PLAYERS, PlayerName, NaviPlayer, VitalityPlayer, Team} from '@/data/teamsAndPlayers';

export function usePlayerStats(killData: MatchStats) {
  const currentRound = ref(1);
  const roundNumber = ref<number[]>([]);
  const allPlayerStats = ref<PlayerStatsBase[]>([]);

  const getTeamPlayers = (team: Team): PlayerStatsBase[] => {
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
  };

  const calculateKDRatio = (player: PlayerStatsBase): string => {
    if (!player) return '0.00';
    if (player.deaths === 0) return player.kills === 0 ? '0.00' : player.kills.toFixed(2);
    return (Math.max(0, player.kills) / Math.max(1, player.deaths)).toFixed(2);
  };

  const calculateHeadshotPercentage = (player: PlayerStatsBase): string => {
    return (player.kills > 0 ? (player.headshots / player.kills) * 100 : 0).toFixed(1);
  };

  const getPlayerMostUsedWeapon = (playerName: PlayerName): string => {
    const kills = killData.kills.filter(kill =>
        kill.round <= currentRound.value && kill.killer.name === playerName
    );

    const weaponCounts: Record<string, number> = {};
    kills.forEach(kill => {
      weaponCounts[kill.weapon] = (weaponCounts[kill.weapon] || 0) + 1;
    });

    const mostUsedWeapon = Object.entries(weaponCounts)
        .sort(([, a], [, b]) => b - a)[0];

    return mostUsedWeapon ? `${mostUsedWeapon[0]}: ${mostUsedWeapon[1]}` : '-';
  };

  const transformPlayerStats = (): PlayerStatsBase[] => {
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

      killData.kills.forEach((kill: KillEvent) => {
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
    allPlayerStats.value = stats;
    return stats;
  };

  return {
    currentRound,
    roundNumber,
    allPlayerStats,
    calculateKDRatio,
    calculateHeadshotPercentage,
    getPlayerMostUsedWeapon,
    transformPlayerStats,
    getTeamPlayers
  };
}