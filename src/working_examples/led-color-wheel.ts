import { colorwheel, StripType, ws281x } from "piixel";

const LEDS = 1;

// Configure the library. Must be called before calling `render`.
// See APIDocs for the full list of options
// https://github.com/bjoerge/pipixel/blob/main/docs/piixel.ws281xconfig.md
ws281x.configure({
  gpio: 12,
  leds: LEDS,
});

const pixels = new Uint32Array(LEDS);
for (let i = 0; i < LEDS; i++) {
  pixels[i] = colorwheel(100);
}

const timer = (ms) => new Promise((res) => setTimeout(res, ms));

// Render pixels to the LED strip
const main = async () => {
  while (true) {
    for (let i = 0; i < 256; i++) {
      pixels[0] = colorwheel(i);
      ws281x.render({ pixels, brightness: 0.4 });
      await timer(10);
    }
  }
};

main();
