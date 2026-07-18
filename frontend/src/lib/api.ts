import type { Campaign, ProgressPayload, Quest, SubmitResponse, Language, AuthUser, AuthResponse, HintsResponse, CodexResponse } from './types'

const API = '/api'
const TOKEN_KEY = 'pf_token'
const CAMPAIGN_ID = 'detective_academy'

/** In-memory guest progress — cleared on full page reload by design. */
let guestProgress: ProgressPayload | null = null

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string | null) {
  if (token) localStorage.setItem(TOKEN_KEY, token)
  else localStorage.removeItem(TOKEN_KEY)
}

export function isLoggedIn(): boolean {
  return Boolean(getToken())
}

export function getGuestProgress(): ProgressPayload | null {
  return guestProgress
}

export function setGuestProgress(progress: ProgressPayload | null) {
  guestProgress = progress
}

function authHeaders(): Record<string, string> {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders(),
      ...(init?.headers || {}),
    },
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || res.statusText)
  }
  return res.json() as Promise<T>
}

export async function register(email: string, password: string): Promise<AuthResponse> {
  const res = await api<AuthResponse>('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
  setToken(res.access_token)
  guestProgress = null
  return res
}

export async function login(email: string, password: string): Promise<AuthResponse> {
  const res = await api<AuthResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
  setToken(res.access_token)
  guestProgress = null
  return res
}

export function logout() {
  setToken(null)
  guestProgress = null
}

export async function fetchMe(): Promise<AuthUser | null> {
  if (!getToken()) return null
  try {
    return await api<AuthUser>('/auth/me')
  } catch {
    setToken(null)
    return null
  }
}

export async function fetchCampaign(): Promise<Campaign> {
  return api<Campaign>(`/campaigns/${CAMPAIGN_ID}`)
}

export async function fetchQuest(questId: string): Promise<Quest> {
  return api<Quest>(`/quests/${questId}`)
}

export async function fetchHints(questId: string, maxLevel: number): Promise<HintsResponse> {
  return api<HintsResponse>(`/quests/${questId}/hints?max_level=${maxLevel}`)
}

export async function fetchCodex(completedQuestIds?: string): Promise<CodexResponse> {
  if (completedQuestIds) {
    return api<CodexResponse>(`/codex?completed=${encodeURIComponent(completedQuestIds)}`)
  }
  return api<CodexResponse>('/codex')
}

function defaultGuestProgress(): ProgressPayload {
  return {
    user_id: null,
    campaign_id: CAMPAIGN_ID,
    xp: 0,
    unlocked_quest_ids: ['q01_two_sum'],
    completed_quest_ids: [],
    last_language: null,
    ephemeral: true,
  }
}

export async function syncProgress(): Promise<ProgressPayload> {
  if (isLoggedIn()) {
    return api<ProgressPayload>(`/progress?campaign_id=${CAMPAIGN_ID}`)
  }
  if (!guestProgress) {
    guestProgress = defaultGuestProgress()
  }
  return guestProgress
}

export async function submitCode(params: {
  questId: string
  language: Language
  source: string
  mode: 'run' | 'submit'
}): Promise<SubmitResponse> {
  const body: Record<string, unknown> = {
    quest_id: params.questId,
    language: params.language,
    source: params.source,
    mode: params.mode,
  }
  if (!isLoggedIn()) {
    const g = guestProgress ?? defaultGuestProgress()
    body.guest_id = crypto.randomUUID()
    body.xp = g.xp
    body.unlocked_quest_ids = g.unlocked_quest_ids
    body.completed_quest_ids = g.completed_quest_ids
  }
  const result = await api<SubmitResponse>('/submit', {
    method: 'POST',
    body: JSON.stringify(body),
  })
  if (result.progress) {
    if (isLoggedIn()) {
      // server is source of truth
    } else {
      guestProgress = result.progress
    }
  }
  return result
}

export { CAMPAIGN_ID }
