import { cn } from '@/lib/utils'
import type { ButtonHTMLAttributes } from 'react'

type Variant = 'primary' | 'secondary' | 'ghost'

const styles: Record<Variant, string> = {
  primary:
    'bg-[var(--color-lamp)] text-[var(--color-desk)] hover:bg-[var(--color-lamp-glow)] shadow-[0_0_24px_rgba(201,162,39,0.25)]',
  secondary:
    'bg-[var(--color-slate-panel)] text-[var(--color-paper)] border border-[rgba(232,220,200,0.2)] hover:border-[rgba(201,162,39,0.5)]',
  ghost: 'bg-transparent text-[var(--color-paper)] hover:bg-white/5',
}

export function Button({
  className,
  variant = 'primary',
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant }) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center gap-2 rounded-md px-4 py-2 font-[family-name:var(--font-ui)] text-sm font-medium transition disabled:opacity-50 disabled:pointer-events-none',
        styles[variant],
        className,
      )}
      {...props}
    />
  )
}
