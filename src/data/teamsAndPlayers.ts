export type NaviPlayer = 's1mple' | 'b1t' | 'electronic' | 'Boombl4' | 'Perfecto';
export type VitalityPlayer = 'ZywOo' | 'apEX' | 'misutaaa' | 'Kyojin' | 'shox ';
export type PlayerName = NaviPlayer | VitalityPlayer;

export const NAVI_PLAYERS: readonly NaviPlayer[] = ['s1mple', 'b1t', 'electronic', 'Boombl4', 'Perfecto'] as const;
export const VITALITY_PLAYERS: readonly VitalityPlayer[] = ['ZywOo', 'apEX', 'misutaaa', 'Kyojin', 'shox '] as const;

export enum Team {
  Navi = 'NAVI',
  Vitality = 'Vitality'
}