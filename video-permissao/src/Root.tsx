import React from 'react';
import {Composition} from 'remotion';
import {Film, TOTAL_FRAMES, FPS} from './Film';

export const Root: React.FC = () => (
  <Composition
    id="Permissao"
    component={Film}
    durationInFrames={TOTAL_FRAMES}
    fps={FPS}
    width={1920}
    height={1080}
  />
);
