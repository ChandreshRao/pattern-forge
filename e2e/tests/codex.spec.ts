import { test, expect } from '@playwright/test'
import { registerViaUi, uniqueCredentials } from '../helpers/auth'
import { completeTwoSumPython, goToCaseBoard } from '../helpers/quest'

test.describe('pattern codex', () => {
  test('guest: empty then Hash Map after closing q01', async ({ page }) => {
    await page.goto('/codex')
    await expect(page.getByTestId('codex-empty')).toBeVisible()

    await completeTwoSumPython(page)
    await goToCaseBoard(page)
    await page.getByTestId('nav-codex').click()
    await page.waitForURL('**/codex')
    await expect(page.getByTestId('codex-list')).toBeVisible()
    await expect(page.getByTestId('codex-pattern-hash_map')).toContainText('Hash Map')
  })

  test('logged-in: Codex lists pattern after q01', async ({ page }) => {
    const { email, password } = uniqueCredentials()
    await registerViaUi(page, email, password)
    await completeTwoSumPython(page)
    await goToCaseBoard(page)
    await page.getByTestId('nav-codex').click()
    await page.waitForURL('**/codex')
    await expect(page.getByTestId('codex-pattern-hash_map')).toContainText('Hash Map')
  })
})
