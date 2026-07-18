import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { fetchCampaign, syncProgress } from '@/lib/api'
import type { Campaign, ProgressPayload } from '@/lib/types'
import { Button } from '@/components/ui/button'
import { Lock, CheckCircle2, FileText } from 'lucide-react'

export function CaseBoardPage() {
  const [campaign, setCampaign] = useState<Campaign | null>(null)
  const [progress, setProgress] = useState<ProgressPayload | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      try {
        const [c, p] = await Promise.all([fetchCampaign(), syncProgress()])
        if (!cancelled) {
          setCampaign(c)
          setProgress(p)
        }
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : 'Failed to load')
      }
    })()
    return () => {
      cancelled = true
    }
  }, [])

  const chapter = campaign?.chapters?.[0]
  const unlocked = new Set(progress?.unlocked_quest_ids ?? [])
  const completed = new Set(progress?.completed_quest_ids ?? [])

  return (
    <main className="mx-auto min-h-screen max-w-3xl px-6 py-12">
      <Link
        to="/"
        className="font-[family-name:var(--font-ui)] text-sm text-[var(--color-lamp)] hover:underline"
      >
        ← PatternForge
      </Link>
      <motion.h1
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mt-6 font-[family-name:var(--font-display)] text-4xl text-[var(--color-paper-bright)] sm:text-5xl"
      >
        Case Board
      </motion.h1>
      <p className="mt-3 max-w-2xl text-[var(--color-paper)]/80">
        {campaign?.description || 'Detective Academy — Chapter 1'}
      </p>
      <div className="mt-4 font-[family-name:var(--font-ui)] text-sm text-[var(--color-lamp)]">
        XP: {progress?.xp ?? 0}
      </div>

      {error && (
        <p className="mt-6 rounded-md border border-[var(--color-danger)]/40 bg-[var(--color-danger)]/10 p-3 text-sm">
          {error}
        </p>
      )}

      <section className="mt-10">
        <h2 className="font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.25em] text-[var(--color-cork)]">
          {chapter?.title || 'Chapter 1'}
        </h2>
        <ul className="mt-4 space-y-3">
          {(chapter?.quests ?? []).map((q, i) => {
            const isUnlocked = unlocked.has(q.id) || i === 0
            const isDone = completed.has(q.id)
            return (
              <motion.li
                key={q.id}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.08 }}
                className="flex items-center justify-between gap-4 rounded-md border border-[rgba(232,220,200,0.12)] bg-[rgba(28,40,56,0.65)] px-4 py-4 backdrop-blur"
              >
                <div className="flex items-start gap-3">
                  {isDone ? (
                    <CheckCircle2 className="mt-0.5 h-5 w-5 text-[var(--color-success)]" />
                  ) : isUnlocked ? (
                    <FileText className="mt-0.5 h-5 w-5 text-[var(--color-lamp)]" />
                  ) : (
                    <Lock className="mt-0.5 h-5 w-5 text-[var(--color-ink-muted)]" />
                  )}
                  <div>
                    <div className="font-[family-name:var(--font-display)] text-lg text-[var(--color-paper-bright)]">
                      {q.order}. {q.title}
                    </div>
                    <div className="font-[family-name:var(--font-ui)] text-xs text-[var(--color-ink-muted)]">
                      {q.beat_id} · {isDone ? 'Closed' : isUnlocked ? 'Open' : 'Sealed'}
                    </div>
                  </div>
                </div>
                {isUnlocked ? (
                  <Link to={`/quest/${q.id}`}>
                    <Button variant="secondary">{isDone ? 'Revisit' : 'Open case'}</Button>
                  </Link>
                ) : (
                  <span className="font-[family-name:var(--font-ui)] text-xs text-[var(--color-ink-muted)]">
                    Locked
                  </span>
                )}
              </motion.li>
            )
          })}
        </ul>
      </section>
    </main>
  )
}
