import type { ReactNode } from 'react'
import { motion } from 'framer-motion'
import { environmentUrl, npcs, portraitUrl, type Expression, type EnvironmentId, type NpcId } from '@/content/npcs'

type NpcDialoguePanelProps = {
  npcId: NpcId
  expression: Expression
  environment?: EnvironmentId
  lines: Array<{ label?: string; text: string }>
  children?: ReactNode
}

export function NpcDialoguePanel({
  npcId,
  expression,
  environment,
  lines,
  children,
}: NpcDialoguePanelProps) {
  const npc = npcs[npcId]
  const src = portraitUrl(npcId, expression)
  const bg = environment ? environmentUrl(environment) : undefined

  return (
    <div className="relative overflow-hidden rounded-md border border-[rgba(232,220,200,0.15)] bg-[rgba(243,235,224,0.06)] shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
      {bg ? (
        <img
          src={bg}
          alt=""
          aria-hidden
          className="pointer-events-none absolute inset-0 h-full w-full object-cover opacity-[0.22]"
        />
      ) : null}
      <div className="relative flex flex-col gap-5 p-6 sm:flex-row sm:gap-6">
        <motion.figure
          key={`${npcId}-${expression}`}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="mx-auto w-36 shrink-0 sm:mx-0 sm:w-44"
        >
          <motion.img
            src={src}
            alt=""
            animate={{ y: [0, -3, 0] }}
            transition={{ duration: 4.5, repeat: Infinity, ease: 'easeInOut' }}
            className="aspect-[4/5] w-full rounded-sm border border-[rgba(201,162,39,0.25)] object-cover shadow-[0_8px_24px_rgba(0,0,0,0.35)]"
          />
          <figcaption className="mt-2 text-center font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.2em] text-[var(--color-lamp)]">
            {npc.displayName}
          </figcaption>
        </motion.figure>
        <div className="min-w-0 flex-1">
          {lines.map((line, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.12 + i * 0.08, duration: 0.35 }}
              className={i > 0 ? 'mt-5' : undefined}
            >
              {line.label ? (
                <p className="font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.25em] text-[var(--color-lamp)]">
                  {line.label}
                </p>
              ) : null}
              <p
                className={`whitespace-pre-wrap leading-relaxed text-[var(--color-paper)]/90 ${line.label ? 'mt-2' : ''}`}
              >
                {line.text}
              </p>
            </motion.div>
          ))}
          {children}
        </div>
      </div>
    </div>
  )
}
