import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import Editor from '@monaco-editor/react'
import { fetchHints, fetchQuest, submitCode } from '@/lib/api'
import type { Language, Quest, SubmitResponse } from '@/lib/types'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

const LANG_LABEL: Record<Language, string> = {
  python: 'Python',
  javascript: 'JavaScript',
  typescript: 'TypeScript',
}

const MONACO_LANG: Record<Language, string> = {
  python: 'python',
  javascript: 'javascript',
  typescript: 'typescript',
}

export function QuestSolvePage() {
  const { questId } = useParams<{ questId: string }>()
  const navigate = useNavigate()
  const [quest, setQuest] = useState<Quest | null>(null)
  const [language, setLanguage] = useState<Language>('python')
  const [source, setSource] = useState('')
  const [busy, setBusy] = useState(false)
  const [result, setResult] = useState<SubmitResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [hintLevel, setHintLevel] = useState(0)
  const [hints, setHints] = useState<Array<{ level: number; text: string }>>([])
  const [hintBusy, setHintBusy] = useState(false)

  useEffect(() => {
    if (!questId) return
    let cancelled = false
    ;(async () => {
      try {
        const q = await fetchQuest(questId)
        if (cancelled) return
        setQuest(q)
        const starter = q.canon.languages.python?.starter ?? ''
        setSource(starter)
        setLanguage('python')
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : 'Failed to load')
      }
    })()
    return () => {
      cancelled = true
    }
  }, [questId])

  function onLanguageChange(next: Language) {
    if (!quest) return
    setLanguage(next)
    setSource(quest.canon.languages[next]?.starter ?? '')
    setResult(null)
  }

  async function revealNextHint() {
    if (!questId || hintLevel >= 5) return
    const next = hintLevel + 1
    setHintBusy(true)
    try {
      const res = await fetchHints(questId, next)
      setHints(res.hints)
      setHintLevel(next)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load hint')
    } finally {
      setHintBusy(false)
    }
  }

  async function run(mode: 'run' | 'submit') {
    if (!questId) return
    setBusy(true)
    setError(null)
    try {
      const res = await submitCode({ questId, language, source, mode })
      setResult(res)
      if (mode === 'submit' && res.passed && res.reflection) {
        navigate(`/quest/${questId}/reflection`, {
          state: { reflection: res.reflection, progress: res.progress },
        })
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Submit failed')
    } finally {
      setBusy(false)
    }
  }

  if (error && !quest) {
    return (
      <main className="mx-auto max-w-4xl px-6 py-12">
        <p className="text-[var(--color-danger)]">{error}</p>
      </main>
    )
  }

  if (!quest) {
    return (
      <main className="mx-auto max-w-4xl px-6 py-12 font-[family-name:var(--font-ui)] text-sm text-[var(--color-ink-muted)]">
        Loading editor…
      </main>
    )
  }

  return (
    <main className="mx-auto min-h-screen max-w-5xl px-4 py-8 sm:px-6" data-testid="quest-solve">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <Link
            to={`/quest/${quest.id}`}
            className="font-[family-name:var(--font-ui)] text-sm text-[var(--color-lamp)] hover:underline"
          >
            ← Briefing
          </Link>
          <h1 className="mt-2 font-[family-name:var(--font-display)] text-2xl text-[var(--color-paper-bright)]">
            {quest.canon.title}
          </h1>
          <p className="mt-1 text-sm text-[var(--color-paper)]/75">{quest.story.objective_in_world}</p>
        </div>
        <div className="flex flex-wrap gap-2" data-testid="language-tabs">
          {(Object.keys(LANG_LABEL) as Language[]).map((lang) => (
            <button
              key={lang}
              type="button"
              data-testid={`lang-${lang}`}
              onClick={() => onLanguageChange(lang)}
              className={cn(
                'rounded-md px-3 py-1.5 font-[family-name:var(--font-ui)] text-xs',
                language === lang
                  ? 'bg-[var(--color-lamp)] text-[var(--color-desk)]'
                  : 'bg-[var(--color-slate-panel)] text-[var(--color-paper)]',
              )}
            >
              {LANG_LABEL[lang]}
            </button>
          ))}
        </div>
      </div>

      <div
        className="mt-4 overflow-hidden rounded-md border border-[rgba(232,220,200,0.12)]"
        data-testid="monaco-editor"
      >
        <Editor
          height="420px"
          theme="vs-dark"
          language={MONACO_LANG[language]}
          value={source}
          onChange={(v) => setSource(v ?? '')}
          onMount={(editor) => {
            const w = window as Window & {
              __pfSetEditorSource?: (v: string) => void
              __pfGetEditorSource?: () => string
            }
            w.__pfSetEditorSource = (v: string) => {
              editor.setValue(v)
            }
            w.__pfGetEditorSource = () => editor.getValue()
          }}
          options={{
            fontFamily: 'IBM Plex Mono, Consolas, monospace',
            fontSize: 14,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            automaticLayout: true,
          }}
        />
      </div>

      <div className="mt-4 flex flex-wrap gap-3">
        <Button variant="secondary" disabled={busy} data-testid="run-code" onClick={() => run('run')}>
          Run
        </Button>
        <Button disabled={busy} data-testid="submit-code" onClick={() => run('submit')}>
          Submit
        </Button>
        <Button
          variant="ghost"
          disabled={hintBusy || hintLevel >= 5}
          data-testid="hint-next"
          onClick={revealNextHint}
        >
          {hintLevel >= 5 ? 'All hints revealed' : `Hint L${hintLevel + 1}`}
        </Button>
        {busy && (
          <span className="self-center font-[family-name:var(--font-ui)] text-sm text-[var(--color-ink-muted)]">
            Judging…
          </span>
        )}
      </div>

      {hints.length > 0 && (
        <section
          className="mt-4 rounded-md border border-[rgba(232,220,200,0.12)] bg-[rgba(28,40,56,0.55)] p-4"
          data-testid="hint-ladder"
        >
          <h2 className="font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.25em] text-[var(--color-cork)]">
            Hint ladder
          </h2>
          <ul className="mt-3 space-y-2 text-sm text-[var(--color-paper)]/90">
            {hints.map((h) => (
              <li key={h.level} data-testid={`hint-l${h.level}`}>
                <span className="font-[family-name:var(--font-ui)] text-[var(--color-lamp)]">L{h.level}</span>
                {' — '}
                {h.text}
              </li>
            ))}
          </ul>
        </section>
      )}

      {error && (
        <p className="mt-4 rounded-md border border-[var(--color-danger)]/40 bg-[var(--color-danger)]/10 p-3 text-sm">
          {error}
        </p>
      )}

      {result && (
        <section
          className="mt-6 rounded-md border border-[rgba(232,220,200,0.12)] bg-[rgba(28,40,56,0.7)] p-4"
          data-testid="run-results"
        >
          <h2
            className="font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.25em] text-[var(--color-lamp)]"
            data-testid="run-results-heading"
          >
            Results · {result.passed ? 'All passed' : `${result.failed} failed`}
          </h2>
          <ul className="mt-3 space-y-2 font-[family-name:var(--font-mono)] text-sm">
            {result.results.map((r) => (
              <li
                key={r.id}
                className={cn(
                  'rounded border px-3 py-2',
                  r.passed
                    ? 'border-[var(--color-success)]/30 text-[var(--color-success)]'
                    : 'border-[var(--color-danger)]/30 text-[var(--color-paper)]',
                )}
              >
                <div className="flex justify-between gap-2">
                  <span>
                    {r.id}
                    {r.hidden ? ' (hidden)' : ''}
                  </span>
                  <span>{r.passed ? 'PASS' : 'FAIL'}</span>
                </div>
                {!r.passed && !r.hidden && (
                  <div className="mt-1 text-[var(--color-ink-muted)]">
                    expected {JSON.stringify(r.expected)} · got {JSON.stringify(r.actual)}
                    {r.error ? ` · ${r.error}` : ''}
                  </div>
                )}
                {!r.passed && r.hidden && r.error && (
                  <div className="mt-1 text-[var(--color-ink-muted)]">{r.error}</div>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  )
}
