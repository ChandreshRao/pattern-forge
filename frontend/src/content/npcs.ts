import moraNeutral from '@/assets/themes/detective_academy/characters/mora/neutral.svg'
import moraStern from '@/assets/themes/detective_academy/characters/mora/stern.svg'
import moraPleased from '@/assets/themes/detective_academy/characters/mora/pleased.svg'
import moraConcerned from '@/assets/themes/detective_academy/characters/mora/concerned.svg'
import moraThinking from '@/assets/themes/detective_academy/characters/mora/thinking.svg'
import quinNeutral from '@/assets/themes/detective_academy/characters/quin/neutral.svg'
import quinStern from '@/assets/themes/detective_academy/characters/quin/stern.svg'
import quinPleased from '@/assets/themes/detective_academy/characters/quin/pleased.svg'
import quinConcerned from '@/assets/themes/detective_academy/characters/quin/concerned.svg'
import quinThinking from '@/assets/themes/detective_academy/characters/quin/thinking.svg'
import nightDesk from '@/assets/themes/detective_academy/environments/night_desk.svg'
import evidenceLocker from '@/assets/themes/detective_academy/environments/evidence_locker.svg'
import recordsRoom from '@/assets/themes/detective_academy/environments/records_room.svg'

export type NpcId = 'mora' | 'quin'
export type Expression = 'neutral' | 'stern' | 'pleased' | 'concerned' | 'thinking'
export type EnvironmentId = 'night_desk' | 'evidence_locker' | 'records_room'

export type StoryBeatCue = {
  speaker: NpcId
  expression: Expression
  environment: EnvironmentId
  reflectionSpeaker: NpcId
  reflectionExpression: Expression
}

const expressions = {
  mora: {
    neutral: moraNeutral,
    stern: moraStern,
    pleased: moraPleased,
    concerned: moraConcerned,
    thinking: moraThinking,
  },
  quin: {
    neutral: quinNeutral,
    stern: quinStern,
    pleased: quinPleased,
    concerned: quinConcerned,
    thinking: quinThinking,
  },
} as const satisfies Record<NpcId, Record<Expression, string>>

export const npcs = {
  mora: {
    id: 'mora' as const,
    displayName: 'Captain Mora',
    role: 'Captain',
    portraits: expressions.mora,
  },
  quin: {
    id: 'quin' as const,
    displayName: 'Archivist Quin',
    role: 'Archivist',
    portraits: expressions.quin,
  },
} as const

export const environments: Record<EnvironmentId, string> = {
  night_desk: nightDesk,
  evidence_locker: evidenceLocker,
  records_room: recordsRoom,
}

/** Beat → speaker / expression / location (STORY_BIBLE Chapter 1a). */
export const beatCues: Record<string, StoryBeatCue> = {
  B1: {
    speaker: 'mora',
    expression: 'stern',
    environment: 'night_desk',
    reflectionSpeaker: 'quin',
    reflectionExpression: 'thinking',
  },
  B2: {
    speaker: 'mora',
    expression: 'concerned',
    environment: 'evidence_locker',
    reflectionSpeaker: 'quin',
    reflectionExpression: 'thinking',
  },
  B3: {
    speaker: 'quin',
    expression: 'thinking',
    environment: 'records_room',
    reflectionSpeaker: 'mora',
    reflectionExpression: 'pleased',
  },
  B4: {
    speaker: 'mora',
    expression: 'stern',
    environment: 'records_room',
    reflectionSpeaker: 'quin',
    reflectionExpression: 'thinking',
  },
  B5: {
    speaker: 'quin',
    expression: 'thinking',
    environment: 'evidence_locker',
    reflectionSpeaker: 'mora',
    reflectionExpression: 'pleased',
  },
  B6: {
    speaker: 'mora',
    expression: 'concerned',
    environment: 'records_room',
    reflectionSpeaker: 'quin',
    reflectionExpression: 'thinking',
  },
  B7: {
    speaker: 'quin',
    expression: 'thinking',
    environment: 'night_desk',
    reflectionSpeaker: 'mora',
    reflectionExpression: 'stern',
  },
  B8: {
    speaker: 'mora',
    expression: 'stern',
    environment: 'evidence_locker',
    reflectionSpeaker: 'quin',
    reflectionExpression: 'pleased',
  },
  B9: {
    speaker: 'mora',
    expression: 'stern',
    environment: 'night_desk',
    reflectionSpeaker: 'quin',
    reflectionExpression: 'thinking',
  },
  B10: {
    speaker: 'mora',
    expression: 'pleased',
    environment: 'records_room',
    reflectionSpeaker: 'quin',
    reflectionExpression: 'pleased',
  },
}

const defaultCue: StoryBeatCue = {
  speaker: 'mora',
  expression: 'neutral',
  environment: 'night_desk',
  reflectionSpeaker: 'quin',
  reflectionExpression: 'pleased',
}

export function cueForBeat(beatId: string | undefined): StoryBeatCue {
  if (!beatId) return defaultCue
  return beatCues[beatId] ?? defaultCue
}

const questBeatIds: Record<string, string> = {
  q01_two_sum: 'B1',
  q02_contains_duplicate: 'B2',
  q03_valid_anagram: 'B3',
  q04_best_time_to_buy_and_sell_stock: 'B4',
  q05_valid_parentheses: 'B5',
  q06_group_anagrams: 'B6',
  q07_product_of_array_except_self: 'B7',
  q08_reverse_linked_list: 'B8',
  q09_longest_substring_without_repeating: 'B9',
  q10_maximum_subarray: 'B10',
}

export function cueForQuest(questId: string | undefined): StoryBeatCue {
  if (!questId) return defaultCue
  return cueForBeat(questBeatIds[questId])
}

export function portraitUrl(npcId: NpcId, expression: Expression): string {
  return npcs[npcId].portraits[expression]
}

export function environmentUrl(id: EnvironmentId): string {
  return environments[id]
}
