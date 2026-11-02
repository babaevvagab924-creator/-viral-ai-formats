// Scene timing is derived from the voice files: each scene = lead + its clips (back to back with short gaps) + tail.
// `speech` = duration until the end of speech (trailing silence trimmed), measured with ffmpeg silencedetect.
export const FPS = 30;

// Subtitle chunks (2–4 words). Start times come from speech recognition timestamps, relative to the clip start.
const CLIPS = {
  vo1: { speech: 3.16, speaker: "narrator", subs: [[0, "У ChatGPT"], [1.08, "на тебя тоже"], [2.0, "есть компромат"]] },
  vo2: { speech: 3.21, speaker: "narrator", subs: [[0, "Но в клуб"], [0.68, "«Компромат» пускали"], [2.24, "только своих"]] },
  point: { speech: 1.15, speaker: "point", subs: [[0, "Не положено!"]] },
  vo3a: { speech: 2.12, speaker: "narrator", subs: [[0, "ChatGPT пытался"], [1.32, "прорваться…"]] },
  bubble: { speech: 2.24, speaker: "bubble", subs: [[0, "Я Клод."], [1.44, "Честно."]] },
  vo3b: { speech: 1.13, speaker: "narrator", subs: [[0.06, "Не вышло."]] },
  vo4: { speech: 4.23, speaker: "narrator", subs: [[0.04, "Теперь"], [1.76, "ChatGPT и DeepSeek"], [3.4, "тоже внутри"]] },
  vo5: { speech: 5.18, speaker: "narrator", subs: [[0, "Сколько чатов,"], [1.44, "во сколько ты пишешь"], [2.68, "по ночам —"], [3.92, "всё всплывает"]] },
  vo6: { speech: 2.37, speaker: "narrator", subs: [[0, "Какой у тебя тип?"], [1.28, "Пиши в комментах"]] },
  vo7: { speech: 6.27, speaker: "narrator", subs: [[0, "Закажи экспорт"], [1.0, "в настройках,"], [1.84, "дождись письма"], [2.88, "и загрузи архив."], [4.32, "Всё считается"], [5.24, "прямо в телефоне"]] },
  vo8: { speech: 2.69, speaker: "narrator", subs: [[0, "Компромат —"], [1.28, "ссылка в профиле"]] },
};

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
