import { spawn } from 'child_process';
import { chromium } from '@playwright/test';

const CELL_W = 360;
const CELL_H = 260;
const GAP = 16;
const PAD = 16;

const panels = {
  four: {
    cells: [
      { img: 'assets/presets/neel.png', label: 'Néel' },
      { img: 'assets/presets/antiskyrmion.png', label: 'Antiskyrmion' },
      { img: 'assets/presets/afm.png', label: 'AFM' },
      { img: 'assets/presets/ferri.png', label: 'FiM' },
    ],
    cols: 2,
    out: 'assets/four_panel.png',
  },
  comparison: {
    cells: [
      { img: 'assets/presets/afm.png', label: 'AFM' },
      { img: 'assets/presets/ferri.png', label: 'FiM' },
    ],
    cols: 2,
    out: 'assets/afm_fim_comparison.png',
  },
};

function htmlFor(p) {
  const cols = p.cols;
  const rows = Math.ceil(p.cells.length / cols);
  const cells = p.cells
    .map((c) => {
      const style = `width:${CELL_W}px;height:${CELL_H}px;display:flex;align-items:center;justify-content:center;background:#fff;overflow:hidden`;
      return `<div style="${style}"><img src="http://localhost:8080/${c.img}" style="max-width:100%;max-height:100%;object-fit:contain"></div>`;
    })
    .join('');
  const grid = `display:grid;grid-template-columns:repeat(${cols},${CELL_W}px);grid-template-rows:repeat(${rows},${CELL_H}px);gap:${GAP}px;background:#fff`;
  return `<!doctype html><html><head><style>html,body{margin:0;background:#fff}</style></head><body><div style="padding:${PAD}px;background:#fff"><div style="${grid}">${cells}</div></div></body></html>`;
}

(async () => {
  const server = spawn('python3', ['-m', 'http.server', '8080', '--directory', '.'], { stdio: 'ignore' });
  await new Promise((r) => setTimeout(r, 1500));
  try {
    const browser = await chromium.launch();
    const page = await browser.newPage({ deviceScaleFactor: 2 });
    for (const p of Object.values(panels)) {
      const cols = p.cols;
      const rows = Math.ceil(p.cells.length / cols);
      const w = PAD * 2 + cols * CELL_W + (cols - 1) * GAP;
      const h = PAD * 2 + rows * CELL_H + (rows - 1) * GAP;
      await page.setViewportSize({ width: w, height: h });
      await page.setContent(htmlFor(p));
      await page.waitForTimeout(200);
      await page.screenshot({ path: p.out });
      console.log(`exported ${p.out} (${w}x${h})`);
    }
    await browser.close();
  } finally {
    server.kill();
  }
})().catch((e) => { console.error(e); process.exit(1); });
