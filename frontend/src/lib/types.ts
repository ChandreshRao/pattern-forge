export type Language = 'python' | 'javascript' | 'typescript'

export type ProgressPayload = {
  user_id: string | null
  campaign_id: string
  xp: number
  unlocked_quest_ids: string[]
  completed_quest_ids: string[]
  last_language: string | null
  ephemeral?: boolean
}

export type AuthUser = {
  id: string
  email: string
}

export type AuthResponse = {
  access_token: string
  token_type: string
  user: AuthUser
}

export type HintsResponse = {
  quest_id: string
  hints: Array<{ level: number; text: string }>
}

export type CodexEntry = {
  pattern_id: string
  pattern_reveal_name: string
  why: string
  quest_id: string
}

export type CodexResponse = {
  patterns: CodexEntry[]
}

export type QuestSummary = {
  id: string
  order: number
  title: string
  beat_id?: string
  difficulty_rank?: string
}

export type Campaign = {
  id: string
  title: string
  description?: string
  chapters: Array<{
    id: string
    title: string
    summary?: string
    quests: QuestSummary[]
  }>
}

export type Quest = {
  id: string
  order: number
  beat_id: string
  theme_id: string
  canon: {
    title: string
    pattern_id: string
    pattern_reveal_name: string
    difficulty_rank: string
    constraints_text: string
    examples: Array<{ input: unknown; output: unknown }>
    languages: Record<
      Language,
      {
        function_name: string
        starter: string
      }
    >
    tests?: Array<{
      id: string
      input: unknown
      expected: unknown
      hidden?: boolean
    }>
    reflection?: {
      why: string
      common_mistakes?: string[]
      complexity?: { time: string; space: string }
    }
  }
  story: {
    hook: string
    briefing: string
    objective_in_world: string
    success_line: string
    reflection_flavor: string
  }
}

export type TestResult = {
  id: string
  passed: boolean
  hidden: boolean
  expected?: unknown
  actual?: unknown
  error?: string | null
  stdout?: string | null
  stderr?: string | null
}

export type ReflectionPayload = {
  success_line: string
  pattern_reveal_name: string
  why: string
  reflection_flavor: string
  xp_awarded: number
  next_quest_id: string | null
}

export type SubmitResponse = {
  status: string
  passed: boolean
  failed: number
  results: TestResult[]
  reflection: ReflectionPayload | null
  progress: ProgressPayload | null
}
