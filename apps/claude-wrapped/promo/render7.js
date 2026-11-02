// node render5.js out.mp4 [fps] [from] [to] — renders promo7.html (served on :8765) via render5(t) to MP4
const { chromium } = require('playwright'); const { spawn } = require('child_process');
(async () => {
  const [out, fpsA, fromA, toA] = process.argv.slice(2), fps = +(fpsA || 60);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 400, height: 700 } }); const errs = [];
  p.on('pageerror', (e) => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/promo7.html'); await p.waitForFunction(() => window.ready7); await p.evaluate(() => window.ready7);
  const from = +(fromA || 0), to = +(toA || 30), n = Math.round((to - from) * fps);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(fps), '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) {
    const d = await p.evaluate((t) => { window.render7(t); return document.getElementById('out').toDataURL('image/jpeg', 0.92); }, from + i / fps);
    if (!ff.stdin.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise((r) => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise((r) => ff.on('close', r)); console.log('frames', n, 'errors', errs); await b.close();
})();
