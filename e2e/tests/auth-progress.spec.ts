import { test, expect } from '@playwright/test'
import { clearAuth, loginViaUi, registerViaUi, uniqueCredentials } from '../helpers/auth'
import { completeTwoSumPython, goToCaseBoard } from '../helpers/quest'

test.describe('auth progress', () => {
  test('register → complete quest → durable across reload and re-login', async ({ page }) => {
    const { email, password } = uniqueCredentials()
    await registerViaUi(page, email, password)
    await expect(page.getByTestId('case-board-xp')).toContainText(email)

    await completeTwoSumPython(page)
    await goToCaseBoard(page)
    await expect(page.getByTestId('quest-card-q01_two_sum')).toHaveAttribute('data-state', 'completed')
    await expect(page.getByTestId('quest-card-q02_contains_duplicate')).toHaveAttribute(
      'data-state',
      'unlocked',
    )
    await expect(page.getByTestId('case-board-xp')).toContainText('XP: 100')

    await page.reload()
    await expect(page.getByTestId('quest-card-q01_two_sum')).toHaveAttribute('data-state', 'completed')
    await expect(page.getByTestId('case-board-xp')).toContainText('XP: 100')
    await expect(page.getByTestId('case-board-xp')).toContainText(email)

    await page.getByTestId('sign-out').click()
    await page.waitForURL('**/campaign')
    await expect(page.getByTestId('case-board-xp')).toContainText('guest')
    await expect(page.getByTestId('quest-card-q01_two_sum')).toHaveAttribute('data-state', 'unlocked')
    await expect(page.getByTestId('quest-locked-q02_contains_duplicate')).toBeVisible()

    await clearAuth(page)
    await loginViaUi(page, email, password)
    await expect(page.getByTestId('quest-card-q01_two_sum')).toHaveAttribute('data-state', 'completed')
    await expect(page.getByTestId('quest-card-q02_contains_duplicate')).toHaveAttribute(
      'data-state',
      'unlocked',
    )
    await expect(page.getByTestId('case-board-xp')).toContainText('XP: 100')
  })
})
