import { Gpio } from "onoff";
import { colorwheel, StripType, ws281x } from "piixel";

const button = new Gpio(515, "in", "rising", { debounceTimeout: 10 });

button.watch((err, value) => {
  if (err) {
    throw err;
  }

  flashLed();
});

ws281x.configure({
  gpio: 12,
  leds: 1,
});

const pixels = new Uint32Array(1);
pixels[0] = colorwheel(100);

const flashLed = () => {
  ws281x.render({ pixels, brightness: 0.4 });

  setTimeout(() => {
    ws281x.render({ pixels, brightness: 0 });
  }, 200);
};

process.on("SIGINT", (_) => {
  button.unexport();
});
