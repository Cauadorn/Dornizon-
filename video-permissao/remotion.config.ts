import {Config} from '@remotion/cli/config';

// Runs locally on Windows: Remotion downloads its own headless Chrome on first use.
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setConcurrency(null);
