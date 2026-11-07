import { expect, test } from '@playwright/test';
import path from 'node:path';

test('the browser QA harness loads a document', async ({ page }) => {
  const fixture = path.resolve('qa/fixtures/health.html');
  await page.goto(`file://${fixture}`);

  await expect(page).toHaveTitle('Document Intake QA Harness');
  await expect(page.getByTestId('qa-ready')).toHaveText('QA harness ready');
});
