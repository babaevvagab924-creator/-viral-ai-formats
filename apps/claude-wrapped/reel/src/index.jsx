import React from "react";
import { registerRoot, Composition } from "remotion";
import { Reel } from "./Reel.jsx";
import { FPS, TOTAL_FRAMES } from "./timeline.js";

const Root = () => (
  <Composition id="Kompromat" component={Reel} durationInFrames={TOTAL_FRAMES} fps={FPS} width={1080} height={1920} />
);
registerRoot(Root);
