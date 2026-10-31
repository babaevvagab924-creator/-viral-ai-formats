// Renders promo.html frame by frame into an MP4: node render.js promo.html out.mp4 [fps]
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path');
(async () => {
  const [src, out, fpsArg] = process.argv.slice(2), fps = +(fpsArg || 30);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 400, height: 700 } });
  const errs = []; p.on('pageerror', (e) => errs.push(e.message));
  await p.goto('file://' + path.resolve(src)); await p.evaluate(() => window.ready);
  const dur = await p.evaluate(() => window.DUR), n = Math.round(dur * fps);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) {
    const data = await p.evaluate((t) => { window.render(t); return document.getElementById('c').toDataURL('image/jpeg', 0.93); }, i / fps);
    if (!ff.stdin.write(Buffer.from(data.split(',')[1], 'base64'))) await new Promise((r) => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise((r) => ff.on('close', r));
  console.log('frames', n, 'errors', errs); await b.close();
})();
