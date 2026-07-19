import type { Page } from '@playwright/test'
import { SOLUTIONS } from '../fixtures/solutions'
import { setMonacoValue } from './monaco'

/** Guest or logged-in: open q01, paste Python solution, submit through reflection. */
export async function completeTwoSumPython(page: Page) {
  await page.goto('/quest/q01_two_sum')
  await page.getByRole('button', { name: 'Open editor' }).click()
  await page.waitForURL('**/quest/q01_two_sum/solve')
  await setMonacoValue(page, SOLUTIONS.q01_two_sum.python)

  const submitResponse = page.waitForResponse(
    (r) => r.url().includes('/submit') && r.request().method() === 'POST',
    { timeout: 120_000 },
  )
  await page.getByTestId('submit-code').click()
  const res = await submitResponse
  const body = (await res.json()) as { passed?: boolean; failed?: number }
  if (!body.passed) {
    throw new Error(`Submit did not pass: ${JSON.stringify(body).slice(0, 500)}`)
  }
  await page.waitForURL('**/quest/q01_two_sum/reflection', { timeout: 30_000 })
  await page.getByTestId('reflection-page').waitFor({ state: 'visible' })
}

export async function goToCaseBoard(page: Page) {
  await page.getByRole('button', { name: 'Case Board' }).click()
  await page.waitForURL('**/campaign')
  await page.getByTestId('case-board').waitFor({ state: 'visible' })
}
