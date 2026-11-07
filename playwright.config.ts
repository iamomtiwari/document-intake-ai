import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './qa',
  reporter: 'list',
  use: {
    browserName: 'chromium',
    trace: 'retain-on-failure',
  },
});
