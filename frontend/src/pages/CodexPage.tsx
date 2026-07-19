import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchCodex, getGuestProgress, isLoggedIn, syncProgress } from '@/lib/api'
import type { CodexEntry } from '@/lib/types'

export function CodexPage() {
  const [patterns, setPatterns] = useState<CodexEntry[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      try {
        let entries: CodexEntry[]
        if (isLoggedIn()) {
          const res = await fetchCodex()
          entries = res.patterns
        } else {
          const p = getGuestProgress() ?? (await syncProgress())
          const ids = p.completed_quest_ids.join(',')
          const res = await fetchCodex(ids)
          entries = res.patterns
        }
        if (!cancelled) setPatterns(entries)
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : 'Failed to load')
      }
    })()
    return () => {
      cancelled = true
    }
  }, [])

  return (
    <main className="mx-auto min-h-screen max-w-3xl px-6 py-12" data-testid="codex-page">
      <Link to="/campaign" className="font-[family-name:var(--font-ui)] text-sm text-[var(--color-lamp)] hover:underline">
        ← Case Board
      </Link>
      <h1 className="mt-6 font-[family-name:var(--font-display)] text-4xl text-[var(--color-paper-bright)]">
        Pattern Codex
      </h1>
      <p className="mt-3 text-[var(--color-paper)]/80">
        Patterns you have discovered on closed cases.
      </p>
      {error && (
        <p className="mt-6 rounded-md border border-[var(--color-danger)]/40 bg-[var(--color-danger)]/10 p-3 text-sm">
          {error}
        </p>
      )}
      {patterns.length === 0 && !error ? (
        <p
          className="mt-10 font-[family-name:var(--font-ui)] text-sm text-[var(--color-ink-muted)]"
          data-testid="codex-empty"
        >
          No patterns yet — close a case to reveal one.
        </p>
      ) : (
        <ul className="mt-10 space-y-4" data-testid="codex-list">
          {patterns.map((p) => (
            <li
              key={p.pattern_id}
              data-testid={`codex-pattern-${p.pattern_id}`}
              className="rounded-md border border-[rgba(232,220,200,0.12)] bg-[rgba(28,40,56,0.65)] px-4 py-4"
            >
              <p className="font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.25em] text-[var(--color-cork)]">
                {p.quest_id}
              </p>
              <h2 className="mt-1 font-[family-name:var(--font-display)] text-2xl text-[var(--color-lamp-glow)]">
                {p.pattern_reveal_name}
              </h2>
              <p className="mt-2 text-[var(--color-paper)]/85">{p.why}</p>
            </li>
          ))}
        </ul>
      )}
    </main>
  )
}
