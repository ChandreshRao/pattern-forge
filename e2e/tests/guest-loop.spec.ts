import { test, expect } from '@playwright/test'
import { SOLUTIONS } from '../fixtures/solutions'
import { setMonacoValue } from '../helpers/monaco'
import { goToCaseBoard } from '../helpers/quest'

test.describe('guest loop', () => {
  test('landing → solve q01 → reflection → unlock q02', async ({ page }) => {
    await page.goto('/')
    await page.getByRole('button', { name: 'Enter Detective Academy' }).click()
    await page.waitForURL('**/campaign')
    await expect(page.getByTestId('case-board')).toBeVisible()

    await page.getByTestId('quest-open-q01_two_sum').click()
    await page.waitForURL('**/quest/q01_two_sum')
    await page.getByRole('button', { name: 'Open editor' }).click()
    await page.waitForURL('**/quest/q01_two_sum/solve')

    await setMonacoValue(page, SOLUTIONS.q01_two_sum.python)
    const runResponse = page.waitForResponse(
      (r) => r.url().includes('/submit') && r.request().method() === 'POST',
      { timeout: 120_000 },
    )
    await page.getByTestId('run-code').click()
    await runResponse
    await expect(page.getByTestId('run-results')).toBeVisible({ timeout: 15_000 })
    await expect(page.getByTestId('run-results-heading')).toContainText('All passed')

    const submitResponse = page.waitForResponse(
      (r) => r.url().includes('/submit') && r.request().method() === 'POST',
      { timeout: 120_000 },
    )
    await page.getByTestId('submit-code').click()
    const submitBody = (await (await submitResponse).json()) as { passed?: boolean }
    if (!submitBody.passed) {
      throw new Error(`Submit did not pass: ${JSON.stringify(submitBody).slice(0, 500)}`)
    }
    await page.waitForURL('**/quest/q01_two_sum/reflection', { timeout: 30_000 })
    await expect(page.getByTestId('reflection-page')).toBeVisible()
    await expect(page.getByTestId('reflection-pattern')).toContainText('Hash Map')
    await expect(page.getByTestId('reflection-xp')).toContainText('+100 XP')

    await goToCaseBoard(page)
    await expect(page.getByTestId('quest-card-q01_two_sum')).toHaveAttribute('data-state', 'completed')
    await expect(page.getByTestId('quest-card-q02_contains_duplicate')).toHaveAttribute(
      'data-state',
      'unlocked',
    )
    await expect(page.getByTestId('case-board-xp')).toContainText('XP: 100')
  })

  test('JavaScript language tab submits q01', async ({ page }) => {
    await page.goto('/quest/q01_two_sum/solve')
    await page.getByTestId('lang-javascript').click()
    await setMonacoValue(page, SOLUTIONS.q01_two_sum.javascript)
    const submitResponse = page.waitForResponse(
      (r) => r.url().includes('/submit') && r.request().method() === 'POST',
      { timeout: 120_000 },
    )
    await page.getByTestId('submit-code').click()
    const submitBody = (await (await submitResponse).json()) as { passed?: boolean }
    if (!submitBody.passed) {
      throw new Error(`JS submit did not pass: ${JSON.stringify(submitBody).slice(0, 500)}`)
    }
    await page.waitForURL('**/quest/q01_two_sum/reflection', { timeout: 30_000 })
    await expect(page.getByTestId('reflection-pattern')).toContainText('Hash Map')
  })
})
