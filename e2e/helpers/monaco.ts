import type { Page } from '@playwright/test'

type PfWindow = Window & {
  __pfSetEditorSource?: (v: string) => void
  __pfGetEditorSource?: () => string
}

/** Wait for Monaco onMount hook, then set source (updates React via onChange). */
export async function setMonacoValue(page: Page, source: string) {
  const editor = page.getByTestId('monaco-editor')
  await editor.waitFor({ state: 'visible' })
  await page.waitForFunction(() => {
    const w = window as PfWindow
    return typeof w.__pfSetEditorSource === 'function'
  })
  await page.evaluate(async (code) => {
    const w = window as PfWindow
    if (!w.__pfSetEditorSource) throw new Error('__pfSetEditorSource missing')
    w.__pfSetEditorSource(code)
    // Two frames so React can commit onChange → source before Run/Submit.
    await new Promise<void>((resolve) => {
      requestAnimationFrame(() => requestAnimationFrame(() => resolve()))
    })
  }, source)
}
