// Scene timing is derived from the voice files: each scene = lead + its clips (back to back with short gaps) + tail.
// `speech` = duration until the end of speech (trailing silence trimmed), measured with ffmpeg silencedetect.
export const FPS = 30;

// Subtitle chunks (2–4 words) with the exact script. Word timing is spread evenly over the speech
// length of each file: a chunk starts at (words before it / words in the file) × speech.
const CLIPS = {
  vo1: { speech: 3.16, speaker: "narrator", chunks: ["У ChatGPT", "на тебя тоже", "есть компромат."] },
  vo2: { speech: 3.21, speaker: "narrator", chunks: ["Но в клуб", "«Компромат» пускали", "только своих."] },
  point: { speech: 1.15, speaker: "point", chunks: ["Не положено."] },
  vo3a: { speech: 2.12, speaker: "narrator", chunks: ["ChatGPT пытался", "прорваться…"] },
  bubble: { speech: 2.24, speaker: "bubble", chunks: ["Я Клод!", "Честно!"] },
  vo3b: { speech: 1.13, speaker: "narrator", chunks: ["Не вышло."] },
  vo4: { speech: 4.23, speaker: "narrator", chunks: ["А теперь —", "вышло!", "ChatGPT и DeepSeek", "тоже внутри."] },
  vo5: { speech: 5.18, speaker: "narrator", chunks: ["Сколько чатов,", "во сколько ты пишешь", "по ночам —", "всё всплывает."] },
  vo6: { speech: 2.37, speaker: "narrator", chunks: ["Какой у тебя тип?", "Пиши в комментах."] },
  vo7: { speech: 6.27, speaker: "narrator", chunks: ["Закажи экспорт", "в настройках,", "дождись письма", "и загрузи архив.", "Всё считается", "прямо в телефоне."] },
  vo8: { speech: 2.69, speaker: "narrator", chunks: ["Компромат.", "Ссылка в профиле."] },
};
const wordsIn = (s) => s.split(/\s+/).filter((w) => /[\p{L}\p{N}]/u.test(w)).length;
for (const c of Object.values(CLIPS)) {
  const total = c.chunks.reduce((n, ch) => n + wordsIn(ch), 0); let before = 0;
  c.subs = c.chunks.map((ch) => { const at = (before / total) * c.speech; before += wordsIn(ch); return [at, ch]; });
}

const LEAD = 0.15, GAP = 0.3;
const SCENES_DEF = [
  { id: 1, clips: ["vo1"], tail: 0.3 },
  { id: 2, clips: ["vo2", "point"], tail: 0.35 },
  { id: 3, clips: ["vo3a", "bubble", "vo3b"], tail: 0.35 },
  { id: 4, clips: ["vo4"], tail: 0.35 },
  { id: 5, clips: ["vo5"], tail: 0.5 },
  { id: 6, clips: ["vo6"], tail: 0.4 },
  { id: 7, clips: ["vo7"], tail: 0.45 },
  { id: 8, clips: ["vo8"], tail: 0.8 },
];

let cursor = 0;
export const SCENES = SCENES_DEF.map((s) => {
  let t = LEAD;
  const clips = s.clips.map((name, i) => {
    const c = { name, src: `vo/${name}.mp3`, at: t, ...CLIPS[name] };
    t += CLIPS[name].speech + (i < s.clips.length - 1 ? GAP : 0);
    return c;
  });
  const dur = t + s.tail;
  const scene = { id: s.id, start: cursor, dur, clips };
  cursor += dur;
  return scene;
});
export const TOTAL = cursor;
export const TOTAL_FRAMES = Math.ceil(TOTAL * FPS);
export const clipOf = (scene, name) => scene.clips.find((c) => c.name === name);
