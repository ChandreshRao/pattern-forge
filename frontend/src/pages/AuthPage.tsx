import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { login, register } from '@/lib/api'
import { Button } from '@/components/ui/button'

type Mode = 'login' | 'register'

export function AuthPage({ initialMode = 'login' }: { initialMode?: Mode }) {
  const navigate = useNavigate()
  const [mode, setMode] = useState<Mode>(initialMode)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setBusy(true)
    setError(null)
    try {
      if (mode === 'register') await register(email.trim(), password)
      else await login(email.trim(), password)
      navigate('/campaign')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Auth failed')
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-6 py-12">
      <Link to="/" className="font-[family-name:var(--font-ui)] text-sm text-[var(--color-lamp)] hover:underline">
        ← PatternForge
      </Link>
      <h1 className="mt-6 font-[family-name:var(--font-display)] text-3xl text-[var(--color-paper-bright)]">
        {mode === 'login' ? 'Sign in' : 'Create account'}
      </h1>
      <p className="mt-2 text-sm text-[var(--color-paper)]/75">
        Logged-in progress is saved. Guest play stays ephemeral.
      </p>
      <form onSubmit={onSubmit} className="mt-8 space-y-4">
        <label className="block">
          <span className="font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.2em] text-[var(--color-cork)]">
            Email
          </span>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 w-full rounded-md border border-[rgba(232,220,200,0.15)] bg-[rgba(28,40,56,0.8)] px-3 py-2 text-[var(--color-paper)] outline-none focus:border-[var(--color-lamp)]"
          />
        </label>
        <label className="block">
          <span className="font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.2em] text-[var(--color-cork)]">
            Password
          </span>
          <input
            type="password"
            required
            minLength={6}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 w-full rounded-md border border-[rgba(232,220,200,0.15)] bg-[rgba(28,40,56,0.8)] px-3 py-2 text-[var(--color-paper)] outline-none focus:border-[var(--color-lamp)]"
          />
        </label>
        {error && (
          <p className="rounded-md border border-[var(--color-danger)]/40 bg-[var(--color-danger)]/10 p-3 text-sm">
            {error}
          </p>
        )}
        <Button type="submit" disabled={busy} className="w-full">
          {busy ? 'Working…' : mode === 'login' ? 'Sign in' : 'Register'}
        </Button>
      </form>
      <button
        type="button"
        className="mt-6 text-left font-[family-name:var(--font-ui)] text-sm text-[var(--color-lamp)] hover:underline"
        onClick={() => {
          setMode(mode === 'login' ? 'register' : 'login')
          setError(null)
        }}
      >
        {mode === 'login' ? 'Need an account? Register' : 'Have an account? Sign in'}
      </button>
    </main>
  )
}
