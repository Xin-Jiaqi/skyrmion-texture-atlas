import { spawn } from 'child_process';
import { chromium } from '@playwright/test';

const key = process.argv[2];
const out = process.argv[3];
if (!key || !out) {
  console.error('usage: node scripts/export-thumbs.mjs <preset> <output.png>');
  process.exit(1);
}

const server = spawn('python3', ['-m', 'http.server', '8080', '--directory', '.'], { stdio: 'ignore' });
await new Promise((r) => setTimeout(r, 1500));
try {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto('http://localhost:8080/');
  await page.selectOption('#preset', key);
  await page.waitForTimeout(300);
  await page.locator('#mainCanvas').screenshot({ path: out });
  await browser.close();
  console.log(`exported ${key} -> ${out}`);
} finally {
  server.kill();
}
