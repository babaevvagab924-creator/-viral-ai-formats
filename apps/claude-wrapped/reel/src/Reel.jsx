import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, interpolate, Easing, spring } from "remotion";
import { loadFont as loadUnbounded } from "@remotion/google-fonts/Unbounded";
import { loadFont as loadOnest } from "@remotion/google-fonts/Onest";
import { loadFont as loadCaveat } from "@remotion/google-fonts/Caveat";
import { Point, Bubble, ClaudeCloud, Shadow } from "./chars.jsx";
import { SCENES, FPS, clipOf } from "./timeline.js";

loadUnbounded("normal", { weights: ["700", "900"], subsets: ["cyrillic", "latin"] });
loadOnest("normal", { weights: ["500", "700"], subsets: ["cyrillic", "latin"] });
loadCaveat("normal", { weights: ["700"], subsets: ["latin", "cyrillic"] });

const C = { bg: "#12101a", ink2: "#1d1a28", paper: "#f3efe6", orange: "#ff7a1a", cobalt: "#2f3fe3", plum: "#3b1540", lemon: "#f2e94e", mint: "#bff0d4", rose: "#ff5f7e", red: "#e8322b" };
const FLOOR = 1290;
const ease = Easing.bezier(0.2, 0.8, 0.2, 1);
const lerp = (t, a, b, from, to, e = ease) => interpolate(t, [a, b], [from, to], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });
const useT = () => useCurrentFrame() / FPS;
// 0..1 mouth/bob amount while a clip is playing
const talkAmt = (t, clip) => (clip && t >= clip.at && t <= clip.at + clip.speech ? 0.35 + 0.65 * Math.abs(Math.sin((t - clip.at) * 13)) : 0);
const talkStyle = (t, amt) => (amt ? { transform: `rotate(${Math.sin(t * 9) * 4 * amt}deg) translateY(${-Math.abs(Math.sin(t * 9)) * 10 * amt}px)` } : {});
const blinkAt = (t, period = 3.4, off = 0) => (((t + off) % period) > period - 0.12 ? 1 : 0);

/* ---------- character placement (anchored at the feet) ---------- */
const Place = ({ x, y = FLOOR, s = 1, sx = 1, sy = 1, rot = 0, shadow = 240, children, z = 2, o = 1 }) => (
  <>
    {shadow ? <Shadow x={x} y={y} w={shadow * s * sx} o={0.55 * o} /> : null}
    <div style={{ position: "absolute", left: x, top: y, transform: `translate(-50%, -100%) rotate(${rot}deg) scale(${s * sx}, ${s * sy})`, transformOrigin: "50% 100%", zIndex: z, opacity: o }}>{children}</div>
  </>
);

/* ---------- background: 3 parallax layers ---------- */
const Background = ({ t, camX, club }) => (
  <AbsoluteFill>
    <AbsoluteFill style={{ background: C.bg }} />
    <AbsoluteFill style={{ transform: `translateX(${-camX * 0.25}px)` }}>
      <div style={{ position: "absolute", left: -200 + Math.sin(t * 0.3) * 60, top: 80, width: 900, height: 900, borderRadius: "50%", background: "radial-gradient(closest-side, rgba(255,122,26,.20), rgba(255,122,26,0))" }} />
      <div style={{ position: "absolute", left: 520, top: 520 + Math.cos(t * 0.25) * 50, width: 900, height: 900, borderRadius: "50%", background: "radial-gradient(closest-side, rgba(110,60,200,.22), rgba(110,60,200,0))" }} />
      <AbsoluteFill style={{ backgroundImage: "radial-gradient(rgba(243,239,230,.10) 2px, transparent 2.5px)", backgroundSize: "54px 54px", backgroundPosition: `${(t * 6) % 54}px ${(t * 3) % 54}px`, opacity: 0.6 }} />
    </AbsoluteFill>
    {club && (
      <AbsoluteFill style={{ transform: `translateX(${-camX * 0.55}px)` }}>
        <div style={{ position: "absolute", left: -120, right: -120, top: 360, height: FLOOR - 360, background: "linear-gradient(#1b1824, #15121d)", boxShadow: "inset 0 40px 80px rgba(0,0,0,.5)" }} />
        <div style={{ position: "absolute", left: -120, right: -120, top: 360, height: FLOOR - 360, opacity: 0.25,
          backgroundImage: "linear-gradient(rgba(0,0,0,.6) 3px, transparent 3px), linear-gradient(90deg, rgba(0,0,0,.6) 3px, transparent 3px)", backgroundSize: "120px 60px, 120px 120px" }} />
      </AbsoluteFill>
    )}
    <div style={{ position: "absolute", left: -200, right: -200, top: FLOOR - 20, bottom: -100, transform: `translateX(${-camX * 0.9}px)`, background: "linear-gradient(#23202f, #0b0a10 70%)" }} />
    <div style={{ position: "absolute", left: 140, width: 800, top: FLOOR - 70, height: 220, borderRadius: "50%", background: "radial-gradient(closest-side, rgba(255,170,90,.16), rgba(0,0,0,0))", transform: `translateX(${-camX * 0.9}px)` }} />
  </AbsoluteFill>
);

/* ---------- camera: slow push-in + sway ---------- */
const Camera = ({ t, dur, children, punch = 0 }) => {
  const p = t / dur, s = 1 + 0.05 * p + punch;
  return <AbsoluteFill style={{ transform: `scale(${s}) rotate(${Math.sin(t * 0.9) * 0.6}deg) translate(${Math.sin(t * 0.7) * 8}px, ${Math.cos(t * 0.6) * 5}px)` }}>{children}</AbsoluteFill>;
};

const Title = ({ text, t, at = 0.2, y = 250, size = 64, color = C.paper }) => {
  const p = lerp(t, at, at + 0.45, 0, 1);
  return <div style={{ position: "absolute", left: 70, right: 70, top: y, textAlign: "center", fontFamily: "Unbounded", fontWeight: 900, fontSize: size, lineHeight: 1.12, color, opacity: p, transform: `translateY(${(1 - p) * 40}px)`, whiteSpace: "pre-line", textShadow: "0 6px 24px rgba(0,0,0,.6)" }}>{text}</div>;
};

/* ---------- props ---------- */
const Door = ({ signText, flip = 0, signPop = 1, glow = 1 }) => (
  <>
    <div style={{ position: "absolute", left: 540 - 240, top: 470, width: 480, textAlign: "center", fontFamily: "Unbounded", fontWeight: 900, fontSize: 64, color: "#ffd2a6", textShadow: `0 0 ${18 * glow}px #ff7a1a, 0 0 ${48 * glow}px #ff7a1a` }}>КОМПРОМАТ</div>
    <div style={{ position: "absolute", left: 540 - 190, top: 690, width: 380, height: FLOOR - 690, borderRadius: "26px 26px 0 0", background: "linear-gradient(#3a2a20, #24180f)", boxShadow: "0 0 0 16px #2b2433, inset 0 0 60px rgba(0,0,0,.6)" }}>
      <div style={{ position: "absolute", left: 30, top: 40, right: 30, bottom: 0, borderRadius: "16px 16px 0 0", background: "linear-gradient(90deg, #4a3526, #3a2a1d)" }} />
      <div style={{ position: "absolute", right: 46, top: 330, width: 26, height: 26, borderRadius: "50%", background: "radial-gradient(circle at 35% 35%, #ffe2a0, #c08a2a)" }} />
    </div>
    {/* sign above the door (flips on X) */}
    <div style={{ position: "absolute", left: 540 - 230, top: 568, width: 460, height: 100, transform: `scale(${signPop}) scaleY(${Math.abs(Math.cos(flip * Math.PI))})`, borderRadius: 16, background: C.paper, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center",
      fontFamily: "Unbounded", fontWeight: 900, fontSize: signText.length > 14 ? 30 : 42, lineHeight: 1.1, color: C.bg, boxShadow: "0 10px 30px rgba(0,0,0,.5)", whiteSpace: "pre-line" }}>{signText}</div>
  </>
);
const Barrier = ({ angle }) => (
  <>
    <div style={{ position: "absolute", left: 250, top: 960, width: 46, height: FLOOR - 960, borderRadius: 10, background: "linear-gradient(90deg, #6b6475, #3a3542)" }} />
    <div style={{ position: "absolute", left: 273, top: 985, width: 560, height: 36, borderRadius: 18, transformOrigin: "0 50%", transform: `rotate(${angle}deg)`,
      background: "repeating-linear-gradient(90deg, #e8322b 0 60px, #f3efe6 60px 120px)", boxShadow: "0 8px 18px rgba(0,0,0,.45)" }} />
    <div style={{ position: "absolute", left: 255, top: 978, width: 36, height: 36, borderRadius: "50%", background: "radial-gradient(circle at 35% 35%, #ff9a9a, #a01818)" }} />
  </>
);
const Folder = ({ stamp }) => (
  <div style={{ position: "relative", width: 560, height: 400 }}>
    <div style={{ position: "absolute", left: 0, top: -36, width: 220, height: 60, borderRadius: "18px 18px 0 0", background: "#c9a063" }} />
    <div style={{ position: "absolute", inset: 0, borderRadius: 18, background: "linear-gradient(160deg, #e2bd7c, #b98a45)", boxShadow: "0 30px 60px rgba(0,0,0,.5), inset 0 2px 0 rgba(255,255,255,.35)" }} />
    <div style={{ position: "absolute", left: 40, top: 40, fontFamily: "Unbounded", fontWeight: 700, fontSize: 30, color: "#5b3d14" }}>ДЕЛО № 2026</div>
    <div style={{ position: "absolute", left: 60, top: 170, padding: "10px 26px", border: "10px solid #e8322b", borderRadius: 18, color: "#e8322b", fontFamily: "Unbounded", fontWeight: 900, fontSize: 60,
      transform: `rotate(-8deg) scale(${stamp})`, opacity: stamp ? 0.95 : 0 }}>КОМПРОМАТ</div>
  </div>
);
const Card = ({ bg, fg, kicker, value, sub, w = 400, h = 300 }) => (
  <div style={{ width: w, height: h, borderRadius: 28, background: bg, color: fg, padding: 28, boxSizing: "border-box", display: "flex", flexDirection: "column", justifyContent: "space-between", boxShadow: "0 24px 50px rgba(0,0,0,.5), inset 0 2px 0 rgba(255,255,255,.25)" }}>
    <div style={{ fontFamily: "Onest", fontWeight: 700, fontSize: 24, letterSpacing: 3, textTransform: "uppercase", opacity: 0.85 }}>{kicker}</div>
    <div style={{ fontFamily: "Unbounded", fontWeight: 900, fontSize: value.length > 9 ? 52 : 74, lineHeight: 1 }}>{value}</div>
    {sub ? <div style={{ fontFamily: "Onest", fontWeight: 700, fontSize: 28 }}>{sub}</div> : <div />}
  </div>
);

/* ---------- scenes ---------- */
function Scene1({ sc }) {
  const t = useT(), fr = useCurrentFrame();
  const drop = spring({ frame: fr - 4, fps: FPS, config: { damping: 9, stiffness: 120 } });
  const stamp = t > 0.75 ? spring({ frame: fr - Math.round(0.75 * FPS), fps: FPS, from: 2.6, to: 1, config: { damping: 12 } }) : 0;
  const y = interpolate(drop, [0, 1], [-500, 820]);
  return (
    <Camera t={t} dur={sc.dur} punch={t > 0.75 && t < 1.0 ? 0.02 * (1 - (t - 0.75) / 0.25) : 0}>
      <Background t={t} camX={Math.sin(t * 0.7) * 30} />
      <Title text={"У ChatGPT на тебя\nтоже есть компромат 👀"} t={t} at={0.25} y={250} size={60} />
      <Shadow x={540} y={FLOOR - 40} w={520 * Math.min(1, drop)} o={0.6} />
      <div style={{ position: "absolute", left: 540 - 280, top: y, transform: `rotate(${(1 - drop) * -18 + 4}deg)` }}><Folder stamp={stamp} /></div>
      {t > 0.75 && t < 1.3 && <div style={{ position: "absolute", left: 300, top: 960, width: 500, height: 200, borderRadius: "50%", background: "radial-gradient(closest-side, rgba(232,50,43,.35), rgba(0,0,0,0))", opacity: 1 - (t - 0.75) / 0.55 }} />}
    </Camera>
  );
}

function Scene2({ sc }) {
  const t = useT(); const vo2 = clipOf(sc, "vo2"), pt = clipOf(sc, "point");
  const barrierDown = lerp(t, pt.at - 0.12, pt.at, -78, 0, Easing.in(Easing.quad));
  const pointTalk = talkAmt(t, pt), deflate = lerp(t, pt.at + pt.speech, pt.at + pt.speech + 0.45, 0, 1, Easing.out(Easing.quad));
  const signPop = t < 2.35 ? 0 : spring({ frame: Math.round((t - 2.35) * FPS), fps: FPS, config: { damping: 10 } });
  const cloud = (i) => { const a = 0.25 + i * 0.55; const p = lerp(t, a, a + 1.4, 0, 1, Easing.inOut(Easing.quad)); return { x: lerp(p, 0, 0.75, -200, 540), o: lerp(p, 0.75, 1, 1, 0), s: lerp(p, 0.7, 1, 0.75, 0.45) }; };
  const bx = lerp(t, 2.0, 3.4, -260, 190, Easing.out(Easing.quad));
  const bump = t > pt.at && t < pt.at + 0.4 ? Math.sin((t - pt.at) * 40) * 6 * (1 - (t - pt.at) / 0.4) : 0;
  return (
    <Camera t={t} dur={sc.dur}>
      <Background t={t} camX={Math.sin(t * 0.7) * 30} club />
      <Door signText={"Только Claude"} signPop={signPop} glow={0.8 + 0.2 * Math.sin(t * 8)} />
      {[0, 1].map((i) => { const c = cloud(i); return c.o > 0 && <Place key={i} x={c.x} s={c.s} o={c.o} z={1}><div style={{ transform: `translateY(${-Math.abs(Math.sin(t * 6 + i)) * 20}px)` }}><ClaudeCloud id={`c${i}`} look={[1, 0]} /></div></Place>; })}
      <Place x={bx + bump} sx={1 + deflate * 0.15} sy={1 - deflate * 0.42} s={0.82}><Bubble id="b2" look={[1, -0.3]} wide={t > pt.at ? 1 : 0} squint={0} talk={0} /></Place>
      <Barrier angle={barrierDown} />
      <Place x={860} s={0.95}><div style={talkStyle(t, pointTalk)}><Point id="p2" talk={pointTalk} frown={t > pt.at - 0.3 ? 1 : 0} look={[-1, 0]} blink={blinkAt(t)} /></div></Place>
    </Camera>
  );
}

function Scene3({ sc }) {
  const t = useT(); const bb = clipOf(sc, "bubble"), nv = clipOf(sc, "vo3b");
  const marker = lerp(t, 0.25, 1.15, 0, 1, Easing.linear);
  const squint = lerp(t, bb.at + 0.3, bb.at + 1.2, 0, 0.7);
  const rip = nv.at; const ripped = t > rip;
  const ptX = t < rip - 0.15 ? 860 : t < rip + 0.25 ? lerp(t, rip - 0.15, rip, 860, 560, Easing.in(Easing.quad)) : lerp(t, rip + 0.25, rip + 0.6, 560, 860);
  const bx = lerp(t, rip + 0.45, rip + 1.4, 250, -280, Easing.in(Easing.quad));
  const sidle = t > rip + 0.45 ? Math.abs(Math.sin(t * 14)) * 14 : 0;
  const mo = ripped ? lerp(t, rip, rip + 0.8, 0, 1, Easing.out(Easing.quad)) : 0;
  return (
    <Camera t={t} dur={sc.dur}>
      <Background t={t} camX={Math.sin(t * 0.7) * 30} club />
      <Door signText={"Только Claude"} />
      <Barrier angle={0} />
      <Place x={bx} y={FLOOR - sidle} s={0.82} rot={t > rip + 0.45 ? -6 : 0}><div style={talkStyle(t, talkAmt(t, bb))}><Bubble id="b3" disguise={1} moustache={ripped ? 0 : 1} marker={marker} talk={talkAmt(t, bb)} look={t > rip ? [-1, 0] : [1, 0]} wide={ripped ? 1 : 0} blush={ripped ? 0.8 : 0} /></div></Place>
      {ripped && <div style={{ position: "absolute", left: 300 + mo * 620, top: 1020 - mo * 520 + mo * mo * 260, transform: `rotate(${mo * 720}deg)`, zIndex: 5 }}>
        <svg width={140} height={50} viewBox="-70 -25 140 50"><path d="M -62 0 Q -40 -16 -6 -4 Q 0 -12 6 -4 Q 40 -16 62 0 Q 40 16 6 4 Q 0 10 -6 4 Q -40 16 -62 0 Z" fill="#2a1a10" /></svg></div>}
      <Place x={ptX} s={0.95}><Point id="p3" squint={ripped ? 0 : squint} frown={1} look={[-1, 0]} smile={t > rip + 0.6 ? 1 : 0} /></Place>
    </Camera>
  );
}

function Scene4({ sc }) {
  const t = useT(); const vo = clipOf(sc, "vo4");
  const flip = lerp(t, 0.25, 0.75, 0, 1, Easing.inOut(Easing.quad));
  const signText = flip < 0.5 ? "Только Claude" : "Теперь ChatGPT\nи DeepSeek тоже";
  const up = lerp(t, vo.at + 1.76, vo.at + 2.1, 0, -78);
  const fly = lerp(t, vo.at + 2.2, vo.at + 3.3, 0, 1, Easing.in(Easing.quad));
  return (
    <Camera t={t} dur={sc.dur}>
      <Background t={t} camX={Math.sin(t * 0.7) * 30} club />
      <Door signText={signText} flip={flip} />
      {fly < 1 && <Place x={lerp(fly, 0, 1, -200, 540)} y={FLOOR - Math.sin(fly * Math.PI) * 220} s={0.82 * (1 - fly * 0.55)} rot={fly * 20} o={1 - Math.max(0, fly - 0.85) / 0.15} z={1}><Bubble id="b4" look={[1, -0.5]} smile={1} /></Place>}
      <Barrier angle={up} />
      <Place x={860} s={0.95}><div style={{ transform: `rotate(${t > vo.at + 1.8 ? Math.sin(t * 6) * 4 : 0}deg)` }}><Point id="p4" smile={t > vo.at + 1.8 ? 1 : 0} look={t > vo.at + 2.2 ? [-1, 0] : [0, -0.6]} blink={blinkAt(t)} /></div></Place>
    </Camera>
  );
}

function Scene5({ sc }) {
  const t = useT(); const vo = clipOf(sc, "vo5"); const a = vo.at;
  const zipP = lerp(t, 0.25, 0.75, 0, 1, Easing.out(Easing.quad));
  const burst = t > 0.85;
  const cards = [
    { at: a, x: 300, y: 250, rot: -5, bg: C.cobalt, fg: C.paper, kicker: "чатов", value: String(Math.round(lerp(t, a, a + 1.3, 0, 1247, Easing.out(Easing.cubic)))).replace(/\B(?=(\d{3})+(?!\d))/g, " "), sub: "за год" },
    { at: a + 1.44, x: 780, y: 280, rot: 5, bg: C.plum, fg: C.lemon, kicker: "пиковый час", value: `${String(Math.round(lerp(t, a + 1.44, a + 2.4, 0, 3))).padStart(2, "0")}:00`, sub: "ночью" },
    { at: a + 2.68, x: 540, y: 600, rot: -2, bg: C.orange, fg: C.bg, kicker: "твой тип", value: "Ночная сова", sub: "" },
  ];
  const giggle = t > a + 3.8 ? Math.abs(Math.sin(t * 12)) : 0, blush = lerp(t, a + 3.92, a + 4.4, 0, 1);
  return (
    <Camera t={t} dur={sc.dur}>
      <Background t={t} camX={Math.sin(t * 0.7) * 30} />
      {!burst && <div style={{ position: "absolute", left: 540 - 90, top: lerp(zipP, 0, 1, 1000, 640), transform: `rotate(${zipP * 360}deg) scale(${0.6 + zipP * 0.6})`, width: 180, height: 220, borderRadius: 18, background: "linear-gradient(160deg, #ffd166, #e09b1a)", boxShadow: "0 16px 30px rgba(0,0,0,.5)" }}>
        <div style={{ position: "absolute", left: 76, top: 0, width: 28, height: 150, background: "repeating-linear-gradient(#7a5a10 0 14px, #e8c060 14px 28px)" }} />
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 22, textAlign: "center", fontFamily: "Unbounded", fontWeight: 900, fontSize: 34, color: C.bg }}>ZIP</div></div>}
      {burst && Array.from({ length: 9 }).map((_, i) => { const d = t - 0.85, ang = -Math.PI / 2 + (i - 4) * 0.42, sp = 700 + (i % 3) * 180; const show = d < 0.9; return show && (
        <div key={i} style={{ position: "absolute", left: 540 - 50 + Math.cos(ang) * sp * d, top: 720 + Math.sin(ang) * sp * d + 600 * d * d, width: 100, height: 130, borderRadius: 8, background: C.paper, transform: `rotate(${d * (i - 4) * 160}deg)`, opacity: 1 - Math.max(0, d - 0.6) / 0.3, boxShadow: "0 8px 16px rgba(0,0,0,.4)" }} />); })}
      {cards.map((c, i) => { if (t < Math.max(c.at, 1.2)) return null; const p = spring({ frame: Math.round((t - Math.max(c.at, 1.2)) * FPS), fps: FPS, config: { damping: 11 } });
        return <div key={i} style={{ position: "absolute", left: c.x - 200, top: c.y, transform: `rotate(${c.rot}deg) scale(${p})`, zIndex: 3 }}><Card {...c} /></div>; })}
      <Place x={150} s={0.6} z={1}><div style={{ transform: `translateY(${-giggle * 16}px)` }}><ClaudeCloud id="c5a" giggle={giggle} look={[1, 0]} /></div></Place>
      <Place x={930} s={0.6} z={1}><div style={{ transform: `translateY(${-giggle * 16}px)` }}><ClaudeCloud id="c5b" giggle={giggle} look={[-1, 0]} /></div></Place>
      <Place x={540} s={0.85}><div style={{ transform: `scale(${1 + (t > 0.2 && t < 0.4 ? 0.08 : 0)})` }}><Bubble id="b5" blush={blush} talk={t > 0.2 && t < 0.45 ? 1 : 0} look={[0, -1]} squint={blush * 0.4} /></div></Place>
    </Camera>
  );
}

function Scene6({ sc }) {
  const t = useT(); const raise = spring({ frame: Math.round(t * FPS) - 4, fps: FPS, config: { damping: 10 } });
  return (
    <Camera t={t} dur={sc.dur}>
      <Background t={t} camX={Math.sin(t * 0.7) * 30} />
      <Title text={"А у тебя какой?\nПиши в комментах 👇"} t={t} at={0.1} y={210} size={58} />
      {[[300, "c6", C.cobalt, C.paper, "Креатор", -6], [790, "b6", C.plum, C.lemon, "Ночная сова", 6]].map(([x, id, bg, fg, v, r], i) => (
        <div key={id} style={{ position: "absolute", left: x - 180, top: 520 - raise * 40 + Math.sin(t * 5 + i) * 10, transform: `rotate(${r + Math.sin(t * 3 + i) * 3}deg) scale(${raise})`, zIndex: 3 }}>
          <Card bg={bg} fg={fg} kicker="мой тип" value={v} w={360} h={260} /></div>))}
      <Place x={300} s={0.95}><div style={{ transform: `translateY(${-Math.abs(Math.sin(t * 5)) * 14}px)` }}><ClaudeCloud id="c6" look={[0, -1]} giggle={0.6} blink={blinkAt(t)} /></div></Place>
      <Place x={790} s={0.8}><div style={{ transform: `translateY(${-Math.abs(Math.sin(t * 5 + 1)) * 14}px)` }}><Bubble id="b6" sign={false} look={[0, -1]} smile={1} /></div></Place>
    </Camera>
  );
}

function Scene7({ sc }) {
  const t = useT(); const a = clipOf(sc, "vo7").at;
  const steps = [[a + 0.0, "Настройки → Экспорт данных"], [a + 1.84, "Жди письмо\n(ChatGPT — до пары дней)"], [a + 2.88, "Загрузи архив на сайт"]];
  const lock = spring({ frame: Math.round((t - (a + 4.32)) * FPS), fps: FPS, config: { damping: 11 } });
  return (
    <Camera t={t} dur={sc.dur}>
      <Background t={t} camX={Math.sin(t * 0.7) * 30} />
      <div style={{ position: "absolute", left: 540 - 300, top: 230, width: 600, height: 1040, borderRadius: 80, background: "#07060a", boxShadow: "0 40px 90px rgba(0,0,0,.6), inset 0 0 0 14px #2b2735" }}>
        <div style={{ position: "absolute", left: 240, top: 30, width: 120, height: 30, borderRadius: 16, background: "#000" }} />
        <div style={{ position: "absolute", left: 40, right: 40, top: 100, fontFamily: "Unbounded", fontWeight: 900, fontSize: 40, color: C.orange }}>Как получить</div>
        {steps.map(([at, s], i) => { const p = t < at ? 0 : spring({ frame: Math.round((t - at) * FPS), fps: FPS, config: { damping: 12 } });
          return <div key={i} style={{ position: "absolute", left: 40, right: 40, top: 190 + i * 210, minHeight: 170, borderRadius: 26, background: C.ink2, boxShadow: "inset 0 0 0 2px #2e2a3d", padding: "24px 26px", boxSizing: "border-box", display: "flex", gap: 20, alignItems: "center", opacity: p, transform: `translateY(${(1 - p) * 60}px) scale(${0.9 + 0.1 * p})` }}>
            <div style={{ flex: "0 0 64px", height: 64, borderRadius: "50%", background: C.orange, color: C.bg, fontFamily: "Unbounded", fontWeight: 900, fontSize: 34, display: "flex", alignItems: "center", justifyContent: "center" }}>{i + 1}</div>
            <div style={{ fontFamily: "Onest", fontWeight: 700, fontSize: 36, lineHeight: 1.2, color: C.paper, whiteSpace: "pre-line" }}>{s}</div></div>; })}
        <div style={{ position: "absolute", left: 40, right: 40, bottom: 60, display: "flex", gap: 18, alignItems: "center", opacity: t > a + 4.32 ? lock : 0, transform: `scale(${t > a + 4.32 ? lock : 0.5})` }}>
          <svg width={70} height={84} viewBox="0 0 70 84"><path d="M 15 38 V 24 a 20 20 0 0 1 40 0 V 38" stroke={C.mint} strokeWidth={9} fill="none" /><rect x={4} y={36} width={62} height={46} rx={10} fill={C.mint} /><circle cx={35} cy={58} r={7} fill={C.bg} /></svg>
          <div style={{ fontFamily: "Onest", fontWeight: 700, fontSize: 34, lineHeight: 1.2, color: C.mint }}>Всё считается у тебя в телефоне</div></div>
      </div>
      <Place x={150} y={FLOOR + 40} s={0.5} z={4}><Point id="p7" look={[1, -1]} blink={blinkAt(t)} smile={1} /></Place>
    </Camera>
  );
}

function Scene8({ sc }) {
  const t = useT(); const hug = spring({ frame: Math.round(t * FPS) - 3, fps: FPS, config: { damping: 9 } });
  return (
    <Camera t={t} dur={sc.dur}>
      <Background t={t} camX={Math.sin(t * 0.7) * 30} />
      <Title text={"Компромат —\nссылка в профиле"} t={t} at={0.1} y={240} size={74} color={C.orange} />
      {Array.from({ length: 7 }).map((_, i) => { const d = (t * 0.6 + i / 7) % 1; return <div key={i} style={{ position: "absolute", left: 380 + (i * 53) % 330, top: 1000 - d * 500, fontSize: 54, opacity: Math.sin(d * Math.PI) * 0.9 }}>❤</div>; })}
      <Place x={lerp(hug, 0, 1, 200, 430)} s={0.95} rot={8 * hug}><Point id="p8" smile={1} squint={0.55} /></Place>
      <Place x={lerp(hug, 0, 1, 880, 650)} s={0.82} rot={-8 * hug}><Bubble id="b8" sign={false} smile={1} squint={0.55} blush={0.5} /></Place>
    </Camera>
  );
}

const SCENE_COMPONENTS = [Scene1, Scene2, Scene3, Scene4, Scene5, Scene6, Scene7, Scene8];

/* ---------- subtitles: 2–4 words, in sync, above the Reels UI (bottom edge ≤ 75% of height) ---------- */
const SUBS = SCENES.flatMap((sc) => sc.clips.flatMap((c) => c.subs.map(([at, text], i) => {
  const start = sc.start + c.at + at, next = c.subs[i + 1] ? sc.start + c.at + c.subs[i + 1][0] : sc.start + c.at + c.speech + 0.15;
  return { start, end: next, text, speaker: c.speaker };
})));
const SUB_COLOR = { narrator: "#ffffff", point: "#ff7a1a", bubble: "#3fe08f" };
const Subtitles = () => {
  const t = useT(); const s = SUBS.find((q) => t >= q.start && t < q.end); if (!s) return null;
  const p = lerp(t, s.start, s.start + 0.12, 0.85, 1, Easing.out(Easing.back(2)));
  return (
    <div style={{ position: "absolute", left: 60, right: 60, bottom: 1920 * 0.25 + 30, textAlign: "center", transform: `scale(${p})`, zIndex: 50 }}>
      <span style={{ fontFamily: "Unbounded", fontWeight: 900, fontSize: 64, lineHeight: 1.1, color: SUB_COLOR[s.speaker] || "#fff", WebkitTextStroke: "14px #000", paintOrder: "stroke fill", textShadow: "0 6px 0 rgba(0,0,0,.35)" }}>{s.text}</span>
    </div>
  );
};

/* ---------- SFX (quieter than the voice) ---------- */
const sc = (n) => SCENES[n - 1];
const SFX = [
  [sc(1).start + 0.75, "stop", 0.35],
  [sc(2).start + 2.35, "ding", 0.3],
  [sc(2).start + clipOf(sc(2), "point").at - 0.12, "stop", 0.45],
  [sc(2).start + clipOf(sc(2), "point").at + clipOf(sc(2), "point").speech, "deflate", 0.3],
  [sc(3).start + 0.25, "marker", 0.35],
  [sc(3).start + clipOf(sc(3), "vo3b").at, "rip", 0.35],
  [sc(4).start + 0.45, "ding", 0.35],
  [sc(4).start + clipOf(sc(4), "vo4").at + 2.2, "whoosh", 0.3],
  [sc(5).start + 0.25, "pop", 0.35],
  [sc(5).start + 0.85, "whoosh", 0.25],
  [sc(7).start + clipOf(sc(7), "vo7").at + 4.32, "ding", 0.25],
];

export const Reel = () => (
  <AbsoluteFill style={{ background: C.bg, overflow: "hidden" }}>
    {SCENES.map((s, i) => { const Comp = SCENE_COMPONENTS[i]; return (
      <Sequence key={s.id} from={Math.round(s.start * FPS)} durationInFrames={Math.round(s.dur * FPS) + 1}>
        <Comp sc={s} />
        {s.clips.map((c) => <Sequence key={c.name} from={Math.round(c.at * FPS)}><Audio src={staticFile(c.src)} /></Sequence>)}
      </Sequence>); })}
    {SFX.map(([at, name, vol], i) => <Sequence key={i} from={Math.round(at * FPS)}><Audio src={staticFile(`sfx/${name}.wav`)} volume={vol} /></Sequence>)}
    <Subtitles />
    <AbsoluteFill style={{ pointerEvents: "none", background: "radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.45))" }} />
  </AbsoluteFill>
);
