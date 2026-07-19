import { Link, useLocation, useNavigate, useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import type { ProgressPayload, ReflectionPayload } from '@/lib/types'
import { Button } from '@/components/ui/button'
import { NpcDialoguePanel } from '@/components/NpcDialoguePanel'
import { cueForQuest } from '@/content/npcs'

type LocState = {
  reflection?: ReflectionPayload
  progress?: ProgressPayload | null
}

export function ReflectionPage() {
  const { questId } = useParams<{ questId: string }>()
  const location = useLocation()
  const navigate = useNavigate()
  const state = (location.state || {}) as LocState
  const reflection = state.reflection
  const cue = cueForQuest(questId)

  if (!reflection) {
    return (
      <main className="mx-auto max-w-2xl px-6 py-12">
        <p className="text-[var(--color-paper)]/80">No reflection on this visit.</p>
        <Link to="/campaign" className="mt-4 inline-block text-[var(--color-lamp)]">
          ← Case Board
        </Link>
      </main>
    )
  }

  return (
    <main className="mx-auto min-h-screen max-w-3xl px-6 py-12" data-testid="reflection-page">
      <motion.div
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.45 }}
      >
        <p className="font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.3em] text-[var(--color-lamp)]">
          Case closed
        </p>
        <h1 className="mt-3 font-[family-name:var(--font-display)] text-3xl text-[var(--color-paper-bright)]">
          {reflection.success_line}
        </h1>

        <div className="mt-6">
          <NpcDialoguePanel
            npcId={cue.reflectionSpeaker}
            expression={cue.reflectionExpression}
            environment={cue.environment}
            lines={[{ label: 'Debrief', text: reflection.reflection_flavor }]}
          >
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.25 }}
              className="mt-6"
            >
              <p className="font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.25em] text-[var(--color-cork)]">
                Pattern discovered
              </p>
              <p
                className="mt-2 font-[family-name:var(--font-display)] text-3xl text-[var(--color-lamp-glow)] sm:text-4xl"
                data-testid="reflection-pattern"
              >
                {reflection.pattern_reveal_name}
              </p>
              <p className="mt-4 leading-relaxed text-[var(--color-paper)]/90">{reflection.why}</p>
            </motion.div>
          </NpcDialoguePanel>
        </div>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.45 }}
          className="mt-8 font-[family-name:var(--font-ui)] text-lg text-[var(--color-lamp)]"
          data-testid="reflection-xp"
        >
          +{reflection.xp_awarded} XP
          {state.progress ? ` · Total ${state.progress.xp}` : ''}
        </motion.p>
        <div className="mt-8 flex flex-wrap gap-3">
          {reflection.next_quest_id ? (
            <Button onClick={() => navigate(`/quest/${reflection.next_quest_id}`)}>
              Next case
            </Button>
          ) : (
            <Button onClick={() => navigate('/campaign')}>Return to Case Board</Button>
          )}
          <Button variant="ghost" onClick={() => navigate('/campaign')}>
            Case Board
          </Button>
        </div>
        <p className="mt-6 font-[family-name:var(--font-ui)] text-xs text-[var(--color-ink-muted)]">
          Quest {questId}
        </p>
      </motion.div>
    </main>
  )
}
