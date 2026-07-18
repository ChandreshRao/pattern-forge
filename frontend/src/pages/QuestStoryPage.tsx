import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { fetchQuest, syncProgress } from '@/lib/api'
import type { Quest } from '@/lib/types'
import { Button } from '@/components/ui/button'

export function QuestStoryPage() {
  const { questId } = useParams<{ questId: string }>()
  const navigate = useNavigate()
  const [quest, setQuest] = useState<Quest | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!questId) return
    let cancelled = false
    ;(async () => {
      try {
        await syncProgress()
        const q = await fetchQuest(questId)
        if (!cancelled) setQuest(q)
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : 'Failed to load quest')
      }
    })()
    return () => {
      cancelled = true
    }
  }, [questId])

  if (error) {
    return (
      <main className="mx-auto max-w-2xl px-6 py-12">
        <p className="text-[var(--color-danger)]">{error}</p>
        <Link to="/campaign" className="mt-4 inline-block text-[var(--color-lamp)]">
          ← Case Board
        </Link>
      </main>
    )
  }

  if (!quest) {
    return (
      <main className="mx-auto max-w-2xl px-6 py-12 font-[family-name:var(--font-ui)] text-sm text-[var(--color-ink-muted)]">
        Opening case file…
      </main>
    )
  }

  return (
    <main className="mx-auto min-h-screen max-w-2xl px-6 py-12">
      <Link
        to="/campaign"
        className="font-[family-name:var(--font-ui)] text-sm text-[var(--color-lamp)] hover:underline"
      >
        ← Case Board
      </Link>
      <motion.article
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="mt-6 rounded-md border border-[rgba(232,220,200,0.15)] bg-[rgba(243,235,224,0.06)] p-6 shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]"
      >
        <p className="font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.3em] text-[var(--color-cork)]">
          Case file · {quest.beat_id}
        </p>
        <h1 className="mt-3 font-[family-name:var(--font-display)] text-3xl text-[var(--color-paper-bright)]">
          {quest.canon.title}
        </h1>
        <p className="mt-6 whitespace-pre-wrap leading-relaxed text-[var(--color-paper)]/90">
          {quest.story.hook}
        </p>
        <h2 className="mt-8 font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.25em] text-[var(--color-lamp)]">
          Briefing
        </h2>
        <p className="mt-3 whitespace-pre-wrap leading-relaxed text-[var(--color-paper)]/90">
          {quest.story.briefing}
        </p>
        <h2 className="mt-8 font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.25em] text-[var(--color-lamp)]">
          Objective
        </h2>
        <p className="mt-3 text-lg text-[var(--color-paper-bright)]">{quest.story.objective_in_world}</p>
        <h2 className="mt-8 font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.25em] text-[var(--color-lamp)]">
          Evidence samples
        </h2>
        <ul className="mt-3 space-y-2 font-[family-name:var(--font-mono)] text-sm">
          {quest.canon.examples.map((ex, i) => (
            <li
              key={i}
              className="rounded border border-[rgba(232,220,200,0.1)] bg-[var(--color-desk)]/60 px-3 py-2"
            >
              <div className="text-[var(--color-ink-muted)]">input</div>
              <pre className="overflow-x-auto whitespace-pre-wrap text-[var(--color-paper)]">
                {JSON.stringify(ex.input)}
              </pre>
              <div className="mt-2 text-[var(--color-ink-muted)]">output</div>
              <pre className="overflow-x-auto whitespace-pre-wrap text-[var(--color-lamp)]">
                {JSON.stringify(ex.output)}
              </pre>
            </li>
          ))}
        </ul>
        <p className="mt-6 text-sm text-[var(--color-ink-muted)]">{quest.canon.constraints_text}</p>
        <div className="mt-8">
          <Button onClick={() => navigate(`/quest/${quest.id}/solve`)}>Open editor</Button>
        </div>
      </motion.article>
    </main>
  )
}
