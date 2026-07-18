import type { Campaign, ProgressPayload, Quest, SubmitResponse, Language } from './types'

const API = '/api'
const GUEST_KEY = 'pf_guest_id'
const PROGRESS_KEY = 'pf_progress'
const CAMPAIGN_ID = 'detective_academy'

export function getOrCreateGuestId(): string {
  let id = localStorage.getItem(GUEST_KEY)
  if (!id) {
    id = crypto.randomUUID()
    localStorage.setItem(GUEST_KEY, id)
  }
  return id
}

export function readLocalProgress(): ProgressPayload | null {
  const raw = localStorage.getItem(PROGRESS_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw) as ProgressPayload
  } catch {
    return null
  }
}

export function writeLocalProgress(progress: ProgressPayload) {
  localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress))
}

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || res.statusText)
  }
  return res.json() as Promise<T>
}

export async function fetchCampaign(): Promise<Campaign> {
  return api<Campaign>(`/campaigns/${CAMPAIGN_ID}`)
}

export async function fetchQuest(questId: string): Promise<Quest> {
  return api<Quest>(`/quests/${questId}`)
}

export async function fetchProgress(guestId: string): Promise<ProgressPayload> {
  return api<ProgressPayload>(`/progress/${guestId}?campaign_id=${CAMPAIGN_ID}`)
}

export async function putProgress(progress: ProgressPayload): Promise<ProgressPayload> {
  return api<ProgressPayload>(`/progress/${progress.guest_id}`, {
    method: 'PUT',
    body: JSON.stringify(progress),
  })
}

export async function syncProgress(): Promise<ProgressPayload> {
  const guestId = getOrCreateGuestId()
  const local = readLocalProgress()
  let remote = await fetchProgress(guestId)

  if (local && local.guest_id === guestId) {
    const merged: ProgressPayload = {
      guest_id: guestId,
      campaign_id: CAMPAIGN_ID,
      xp: Math.max(local.xp, remote.xp),
      unlocked_quest_ids: Array.from(
        new Set([...local.unlocked_quest_ids, ...remote.unlocked_quest_ids]),
      ),
      completed_quest_ids: Array.from(
        new Set([...local.completed_quest_ids, ...remote.completed_quest_ids]),
      ),
      last_language: local.last_language || remote.last_language,
    }
    remote = await putProgress(merged)
  }

  writeLocalProgress(remote)
  return remote
}

export async function submitCode(params: {
  questId: string
  language: Language
  source: string
  mode: 'run' | 'submit'
}): Promise<SubmitResponse> {
  const guestId = getOrCreateGuestId()
  const result = await api<SubmitResponse>('/submit', {
    method: 'POST',
    body: JSON.stringify({
      guest_id: guestId,
      quest_id: params.questId,
      language: params.language,
      source: params.source,
      mode: params.mode,
    }),
  })
  if (result.progress) {
    writeLocalProgress(result.progress)
  }
  return result
}

export { CAMPAIGN_ID }
