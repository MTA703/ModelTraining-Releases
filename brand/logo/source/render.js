// usage: node render.js <svg> <outdir> <size> <fps> <duration_s> [times_csv]
const { chromium } = require(process.env.PW || 'playwright');
const fs = require('fs');
const [svgPath, outDir, size, fps, dur, times] = process.argv.slice(2);
(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +size, height: +size } });
  const svg = fs.readFileSync(svgPath, 'utf8');
  await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ', '<svg width="' + size + '" height="' + size + '" ')}</body></html>`);
  await p.evaluate(() => document.getAnimations().forEach(a => a.pause()));
  const list = times ? times.split(',').map(Number) : [...Array(Math.round(dur * fps) + 1).keys()].map(i => i / fps);
  let i = 0;
  for (const t of list) {
    await p.evaluate(ms => document.getAnimations().forEach(a => { a.currentTime = ms; }), t * 1000);
    await p.screenshot({ path: `${outDir}/f${String(i++).padStart(4, '0')}.png`, omitBackground: true });
  }
  await b.close();
})();
