import type { Page } from '@playwright/test'

export function uniqueCredentials() {
  const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 8)
  return {
    email: `e2e_${id}@example.com`,
    password: 'testpass123',
  }
}

export async function registerViaUi(page: Page, email: string, password: string) {
  await page.goto('/register')
  await page.getByTestId('auth-email').fill(email)
  await page.getByTestId('auth-password').fill(password)
  await page.getByTestId('auth-submit').click()
  await page.waitForURL('**/campaign')
}

export async function loginViaUi(page: Page, email: string, password: string) {
  await page.goto('/login')
  await page.getByTestId('auth-email').fill(email)
  await page.getByTestId('auth-password').fill(password)
  await page.getByTestId('auth-submit').click()
  await page.waitForURL('**/campaign')
}

/** Clear JWT so the next load is a guest session. */
export async function clearAuth(page: Page) {
  await page.evaluate(() => localStorage.removeItem('pf_token'))
}
