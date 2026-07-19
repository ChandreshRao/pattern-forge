import { test, expect } from '@playwright/test'

test.describe('quest locks', () => {
  test('fresh guest: only q01 open; later quests sealed', async ({ page }) => {
    await page.goto('/campaign')
    await expect(page.getByTestId('case-board')).toBeVisible()

    await expect(page.getByTestId('quest-card-q01_two_sum')).toHaveAttribute('data-state', 'unlocked')
    await expect(page.getByTestId('quest-open-q01_two_sum')).toBeVisible()

    await expect(page.getByTestId('quest-card-q02_contains_duplicate')).toHaveAttribute(
      'data-state',
      'locked',
    )
    await expect(page.getByTestId('quest-locked-q02_contains_duplicate')).toBeVisible()
    await expect(page.getByTestId('quest-open-q02_contains_duplicate')).toHaveCount(0)

    await expect(page.getByTestId('quest-card-q03_valid_anagram')).toHaveAttribute(
      'data-state',
      'locked',
    )
    await expect(page.getByTestId('quest-locked-q03_valid_anagram')).toBeVisible()
  })
})
