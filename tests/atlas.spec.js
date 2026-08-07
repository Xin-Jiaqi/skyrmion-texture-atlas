const { test, expect } = require('@playwright/test');

const PRESETS = [
  'neel_out', 'neel_in', 'bloch_cw', 'bloch_ccw', 'intermediate',
  'higher2', 'anti', 'skyrmionium', 'biskyrmion', 'meron',
  'bimeron', 'afm_sk', 'ferri_sk',
];

function collectErrors(page) {
  const errors = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  page.on('pageerror', (e) => errors.push('pageerror: ' + String(e)));
  return errors;
}

async function paintedPixels(page) {
  return page.evaluate(() => {
    const c = document.querySelector('#mainCanvas');
    const data = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
    let n = 0;
    for (let i = 3; i < data.length; i += 4) if (data[i] > 0) n++;
    return n;
  });
}

async function noHorizontalOverflow(page) {
  return page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
}

async function selectPreset(page, key) {
  await page.selectOption('#preset', key);
}

async function runPresetSweep(page) {
  const errors = collectErrors(page);
  await page.goto('/');
  for (const key of PRESETS) {
    await selectPreset(page, key);
    const painted = await paintedPixels(page);
    expect(painted, `${key}: main canvas painted`).toBeGreaterThan(5000);
    const charge = await page.locator('#chargeBadge').textContent();
    expect(charge.length).toBeGreaterThan(0);
    const overflow = await noHorizontalOverflow(page);
    expect(overflow, `${key}: no horizontal overflow`).toBeTruthy();
    const title = await page.locator('#infoTitle').textContent();
    expect(title.length).toBeGreaterThan(0);
  }
  expect(errors, 'no console errors across all presets').toEqual([]);
}

test.describe('atlas', () => {
  test('desktop 1280px: all 13 presets render without errors', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== 'desktop', 'desktop project only');
    await runPresetSweep(page);
    for (const key of PRESETS) {
      await selectPreset(page, key);
      await page.screenshot({ path: `screenshots/${key}.png`, fullPage: true });
    }
  });

  test('desktop: views, params and export entry work', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== 'desktop', 'desktop project only');
    const errors = collectErrors(page);
    await page.goto('/');
    for (const view of ['paper', 'top', 'side']) {
      await page.click(`[data-view="${view}"]`);
    }
    await page.click('#resetPreset');
    await page.locator('#p').evaluate((el) => { el.value = '-1'; el.dispatchEvent(new Event('input')); });
    expect(await page.locator('#infoN').textContent()).toContain('−1');
    expect(errors, 'no console errors').toEqual([]);
  });

  test('mobile 390px: single-column layout, no overflow, all presets render', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== 'mobile', 'mobile project only');
    await runPresetSweep(page);
    const visualCols = await page.evaluate(() => getComputedStyle(document.querySelector('.visualGrid')).gridTemplateColumns.split(' ').length);
    expect(visualCols, 'visualGrid single column at 390px').toBe(1);
    const splitCols = await page.evaluate(() => getComputedStyle(document.querySelector('.splitCol')).gridTemplateColumns.split(' ').length);
    expect(splitCols, 'splitCol single column at 390px').toBe(1);
    await selectPreset(page, 'ferri_sk');
    await page.screenshot({ path: 'screenshots/mobile-390.png', fullPage: true });
  });
});
