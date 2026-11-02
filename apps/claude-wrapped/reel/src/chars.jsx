// Flat 2.5D characters drawn in SVG: soft gradients + highlights for volume, no 3D, no external images.
import React from "react";

const Eye = ({ x, y, rx = 22, ry = 26, look = [0, 0], squint = 0, wide = 0, id }) => {
  const R = ry * (1 + wide * 0.25);
  return (
    <g>
      <clipPath id={id}><ellipse cx={x} cy={y} rx={rx * (1 + wide * 0.2)} ry={R} /></clipPath>
      <ellipse cx={x} cy={y} rx={rx * (1 + wide * 0.2)} ry={R} fill="#fff" />
      <circle cx={x + look[0] * 8} cy={y + 4 + look[1] * 6} r={11 * (1 - wide * 0.25)} fill="#12101a" />
      <circle cx={x + look[0] * 8 + 4} cy={y - 1 + look[1] * 6} r={3.5} fill="#fff" />
      {/* eyelids for squint / blink */}
      <g clipPath={`url(#${id})`}>
        <rect x={x - 40} y={y - R - 2} width={80} height={(R * 2 + 4) * squint * 0.62} fill="rgba(0,0,0,.92)" />
        <rect x={x - 40} y={y + R + 2 - (R * 2 + 4) * squint * 0.3} width={80} height={(R * 2 + 4) * squint * 0.3} fill="rgba(0,0,0,.92)" />
      </g>
    </g>
  );
};

/** Точка — orange ball bouncer with a bow tie. */
export const Point = ({ id = "pt", talk = 0, squint = 0, look = [0, 0], frown = 0, smile = 0, blink = 0 }) => (
  <svg width={300} height={340} viewBox="-150 -150 300 340" style={{ overflow: "visible" }}>
    <defs>
      <radialGradient id={`${id}-g`} cx="36%" cy="30%" r="78%">
        <stop offset="0" stopColor="#ffbe7d" /><stop offset="0.5" stopColor="#ff7a1a" /><stop offset="1" stopColor="#a63f08" />
      </radialGradient>
    </defs>
    <circle r={125} fill={`url(#${id}-g)`} />
    <ellipse cx={-48} cy={-66} rx={40} ry={22} fill="#fff" opacity={0.38} transform="rotate(-32 -48 -66)" />
    <ellipse cx={58} cy={70} rx={30} ry={14} fill="#ffd2a6" opacity={0.18} transform="rotate(-30 58 70)" />
    {/* brows */}
    <path d={`M -72 ${-52 + frown * 10} L -18 ${-48 - squint * 2 - frown * 8}`} stroke="#3a1606" strokeWidth={11} strokeLinecap="round" />
    <path d={`M 72 ${-52 + frown * 10} L 18 ${-48 - squint * 2 - frown * 8}`} stroke="#3a1606" strokeWidth={11} strokeLinecap="round" />
    <Eye id={`${id}-el`} x={-44} y={-14} look={look} squint={Math.max(squint, blink)} />
    <Eye id={`${id}-er`} x={44} y={-14} look={look} squint={Math.max(squint, blink)} />
    {talk > 0.05
      ? <ellipse cx={0} cy={50} rx={20} ry={5 + talk * 16} fill="#3a1606" />
      : <path d={smile > 0 ? "M -26 44 Q 0 70 26 44" : "M -24 52 L 24 52"} stroke="#3a1606" strokeWidth={8} fill="none" strokeLinecap="round" />}
    {/* bouncer bow tie + earpiece */}
    <path d="M -34 112 L -4 124 L -34 136 Z M 34 112 L 4 124 L 34 136 Z" fill="#12101a" />
    <circle cx={0} cy={124} r={8} fill="#12101a" />
    <path d="M 118 -20 q 22 30 2 70" stroke="#12101a" strokeWidth={4} fill="none" />
    <circle cx={120} cy={-22} r={7} fill="#12101a" />
  </svg>
);

/** Бабл — green chat bubble with a "ChatGPT" sign; optional disguise (glasses + moustache) and corrected sign. */
export const Bubble = ({ id = "bb", talk = 0, blush = 0, look = [0, 0], squint = 0, wide = 0, disguise = 0, moustache = 1, marker = 0, sign = true, signText = "ChatGPT", smile = 0 }) => (
  <svg width={340} height={420} viewBox="-170 -150 340 420" style={{ overflow: "visible" }}>
    <defs>
      <linearGradient id={`${id}-g`} x1="0" y1="0" x2="0.4" y2="1">
        <stop offset="0" stopColor="#7bf5b8" /><stop offset="0.5" stopColor="#1fbf74" /><stop offset="1" stopColor="#0a7343" />
      </linearGradient>
    </defs>
    <path d="M -140 -70 Q -140 -120 -90 -120 L 90 -120 Q 140 -120 140 -70 L 140 40 Q 140 90 90 90 L -40 90 L -100 135 L -88 90 L -90 90 Q -140 90 -140 40 Z" fill={`url(#${id}-g)`} />
    <rect x={-140} y={-120} width={280} height={255} fill="#ff3b3b" opacity={blush * 0.35} style={{ mixBlendMode: "multiply" }} clipPath={`url(#${id}-clip)`} />
    <clipPath id={`${id}-clip`}><path d="M -140 -70 Q -140 -120 -90 -120 L 90 -120 Q 140 -120 140 -70 L 140 40 Q 140 90 90 90 L -40 90 L -100 135 L -88 90 L -90 90 Q -140 90 -140 40 Z" /></clipPath>
    <ellipse cx={-70} cy={-92} rx={46} ry={16} fill="#fff" opacity={0.4} />
    <Eye id={`${id}-el`} x={-42} y={-30} look={look} squint={squint} wide={wide} />
    <Eye id={`${id}-er`} x={42} y={-30} look={look} squint={squint} wide={wide} />
    <ellipse cx={-80} cy={14} rx={20} ry={11} fill="#ff6b8a" opacity={0.25 + blush * 0.6} />
    <ellipse cx={80} cy={14} rx={20} ry={11} fill="#ff6b8a" opacity={0.25 + blush * 0.6} />
    {talk > 0.05 ? <ellipse cx={0} cy={36} rx={22} ry={4 + talk * 16} fill="#0b3b25" />
      : <path d={smile > 0 ? "M -26 30 Q 0 56 26 30" : "M -22 38 Q 0 46 22 38"} stroke="#0b3b25" strokeWidth={8} fill="none" strokeLinecap="round" />}
    {disguise > 0 && (
      <g opacity={disguise}>
        <circle cx={-42} cy={-30} r={34} fill="rgba(255,255,255,.08)" stroke="#12101a" strokeWidth={8} />
        <circle cx={42} cy={-30} r={34} fill="rgba(255,255,255,.08)" stroke="#12101a" strokeWidth={8} />
        <path d="M -8 -32 Q 0 -40 8 -32" stroke="#12101a" strokeWidth={7} fill="none" />
        {moustache > 0 && <path d="M -62 18 Q -40 2 -6 14 Q 0 6 6 14 Q 40 2 62 18 Q 40 34 6 22 Q 0 28 -6 22 Q -40 34 -62 18 Z" fill="#2a1a10" />}
      </g>
    )}
    {sign && (
      <g>
        <line x1={-70} y1={88} x2={-80} y2={168} stroke="#c8c0b0" strokeWidth={4} />
        <line x1={70} y1={88} x2={80} y2={168} stroke="#c8c0b0" strokeWidth={4} />
        <rect x={-120} y={160} width={240} height={marker > 0 ? 136 : 76} rx={12} fill="#f3efe6" />
        <text x={0} y={marker > 0 ? 200 : 212} textAnchor="middle" fontFamily="Unbounded" fontWeight={900} fontSize={marker > 0 ? 28 : signText.length > 8 ? 30 : 38} fill="#12101a">{signText}</text>
        {marker > 0 && (
          <g>
            <line x1={-88} y1={190} x2={-88 + 176 * Math.min(1, marker * 2)} y2={186} stroke="#e8322b" strokeWidth={8} strokeLinecap="round" />
            <clipPath id={`${id}-mk`}><rect x={-120} y={200} width={240 * Math.max(0, marker * 2 - 1)} height={100} /></clipPath>
            <text x={0} y={280} textAnchor="middle" fontFamily="Caveat" fontWeight={700} fontSize={78} fill="#e8322b" transform="rotate(-6 0 262)" clipPath={`url(#${id}-mk)`}>Claude</text>
          </g>
        )}
      </g>
    )}
  </svg>
);

/** Облачко Claude — light puffy cloud with eyes and a "Claude" label. */
export const ClaudeCloud = ({ id = "cc", talk = 0, giggle = 0, look = [0, 0], blink = 0, holding = null }) => (
  <svg width={260} height={250} viewBox="-130 -120 260 250" style={{ overflow: "visible" }}>
    <defs>
      <radialGradient id={`${id}-g`} cx="40%" cy="30%" r="80%">
        <stop offset="0" stopColor="#ffffff" /><stop offset="0.6" stopColor="#f0e9dc" /><stop offset="1" stopColor="#c9bca6" />
      </radialGradient>
    </defs>
    <g fill={`url(#${id}-g)`}>
      <circle cx={-55} cy={10} r={58} /><circle cx={0} cy={-25} r={72} /><circle cx={60} cy={8} r={60} /><rect x={-100} y={10} width={200} height={60} rx={30} />
    </g>
    <ellipse cx={-20} cy={-70} rx={34} ry={13} fill="#fff" opacity={0.8} />
    <Eye id={`${id}-el`} x={-26} y={-6} rx={15} ry={18} look={look} squint={Math.max(blink, giggle * 0.75)} />
    <Eye id={`${id}-er`} x={26} y={-6} rx={15} ry={18} look={look} squint={Math.max(blink, giggle * 0.75)} />
    {giggle > 0.1 ? <path d="M -18 26 Q 0 46 18 26 Z" fill="#7a3d1c" /> : talk > 0.05 ? <ellipse cx={0} cy={30} rx={12} ry={3 + talk * 9} fill="#7a3d1c" /> : <path d="M -12 28 Q 0 36 12 28" stroke="#7a3d1c" strokeWidth={5} fill="none" strokeLinecap="round" />}
    <ellipse cx={-48} cy={20} rx={12} ry={7} fill="#ff9a7a" opacity={0.35 + giggle * 0.4} />
    <ellipse cx={48} cy={20} rx={12} ry={7} fill="#ff9a7a" opacity={0.35 + giggle * 0.4} />
    <rect x={-50} y={74} width={100} height={34} rx={10} fill="#ff7a1a" />
    <text x={0} y={98} textAnchor="middle" fontFamily="Unbounded" fontWeight={900} fontSize={20} fill="#12101a">Claude</text>
  </svg>
);

/** Soft contact shadow under a character. */
export const Shadow = ({ x, y, w = 220, o = 0.5 }) => (
  <div style={{ position: "absolute", left: x - w / 2, top: y - w * 0.09, width: w, height: w * 0.18, borderRadius: "50%", background: `radial-gradient(closest-side, rgba(0,0,0,${o}), rgba(0,0,0,0))` }} />
);
