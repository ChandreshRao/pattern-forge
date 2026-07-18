import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { fetchMe, isLoggedIn, logout } from '@/lib/api'
import type { AuthUser } from '@/lib/types'

export function LandingPage() {
  const [user, setUser] = useState<AuthUser | null>(null)

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      if (!isLoggedIn()) return
      const me = await fetchMe()
      if (!cancelled) setUser(me)
    })()
    return () => {
      cancelled = true
    }
  }, [])

  return (
    <main className="relative min-h-screen overflow-hidden">
      <div
        className="pointer-events-none absolute inset-0 opacity-40"
        style={{
          backgroundImage:
            'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(232,220,200,0.03) 2px, rgba(232,220,200,0.03) 3px)',
        }}
      />
      <div className="relative mx-auto flex min-h-screen max-w-5xl flex-col justify-center px-6 py-16">
        <motion.p
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="font-[family-name:var(--font-ui)] text-xs uppercase tracking-[0.35em] text-[var(--color-lamp)]"
        >
          Pattern recognition · story desk
        </motion.p>
        <motion.h1
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="mt-4 font-[family-name:var(--font-display)] text-6xl leading-[1.05] tracking-tight text-[var(--color-paper-bright)] sm:text-7xl md:text-8xl"
        >
          PatternForge
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.25 }}
          className="mt-6 max-w-xl text-lg text-[var(--color-paper)]/85 sm:text-xl"
        >
          Learn algorithms as discoveries under pressure — not as problems to memorize.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mt-10 flex flex-wrap gap-3"
        >
          <Link to="/campaign">
            <Button className="px-6 py-3 text-base">Enter Detective Academy</Button>
          </Link>
          {user ? (
            <Button
              variant="secondary"
              className="px-6 py-3 text-base"
              onClick={() => {
                logout()
                setUser(null)
              }}
            >
              Sign out ({user.email})
            </Button>
          ) : (
            <>
              <Link to="/login">
                <Button variant="secondary" className="px-6 py-3 text-base">
                  Sign in
                </Button>
              </Link>
              <Link to="/register">
                <Button variant="ghost" className="px-6 py-3 text-base">
                  Register
                </Button>
              </Link>
            </>
          )}
        </motion.div>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
          className="mt-16 font-[family-name:var(--font-ui)] text-sm text-[var(--color-ink-muted)]"
        >
          {user
            ? 'Signed in · progress saved to your account'
            : 'Guest play is ephemeral · register to keep XP and unlocks'}
        </motion.p>
      </div>
    </main>
  )
}
