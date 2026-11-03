// Renderer cadangan (HyperFrames plugin tidak ada di sesi cloud): seek GSAP timeline per frame, screenshot, pipe ke ffmpeg.
//   node render.js snap 1.0 5.5 ...        -> renders/snap_<t>.jpg
//   node render.js video renders/visual.mp4 -> video 30 fps tanpa audio
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

(async () => {
  const [mode, ...args] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(__dirname, 'public', 'index.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const dur = await page.evaluate(() => parseFloat(document.getElementById('root').dataset.duration));
  const seek = (t) => page.evaluate((t) => { window.__timelines.hari3.seek(Math.max(t, 0.001), false); }, t);
  fs.mkdirSync(path.join(__dirname, 'renders'), { recursive: true });
  if (mode === 'snap') {
    for (const a of args) {
      await seek(parseFloat(a));
      await page.screenshot({ path: path.join(__dirname, 'renders', `snap_${a}.jpg`), type: 'jpeg', quality: 80 });
    }
  } else {
    const out = args[0] || 'renders/visual.mp4';
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', path.join(__dirname, out)], { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round(dur * 30);
    for (let f = 0; f < n; f++) {
      await seek(f / 30);
      const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
      if (f % 300 === 0) console.log(`frame ${f}/${n}`);
    }
    ff.stdin.end();
    await new Promise((r) => ff.on('close', r));
  }
  await browser.close();
})();
