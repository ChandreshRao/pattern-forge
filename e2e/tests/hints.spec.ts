import { test, expect } from '@playwright/test'

test.describe('hint ladder', () => {
  test('reveals L1–L5 then disables further hints', async ({ page }) => {
    await page.goto('/quest/q01_two_sum/solve')
    await expect(page.getByTestId('hint-next')).toHaveText('Hint L1')

    for (let level = 1; level <= 5; level++) {
      await page.getByTestId('hint-next').click()
      await expect(page.getByTestId('hint-ladder')).toBeVisible()
      await expect(page.getByTestId(`hint-l${level}`)).toBeVisible()
      if (level < 5) {
        await expect(page.getByTestId('hint-next')).toHaveText(`Hint L${level + 1}`)
      }
    }

    await expect(page.getByTestId('hint-next')).toHaveText('All hints revealed')
    await expect(page.getByTestId('hint-next')).toBeDisabled()
    for (let level = 1; level <= 5; level++) {
      await expect(page.getByTestId(`hint-l${level}`)).toBeVisible()
    }
  })
})
