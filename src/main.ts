import { Gpio } from 'onoff';
import Mopidy from 'mopidy';
import { Server } from 'socket.io';

const io = new Server({
  /* options */
});

const mopidy = new Mopidy({
  webSocketUrl: 'ws://localhost:6680/mopidy/ws/',
});
const buttonPrev = new Gpio(516, 'in', 'rising', { debounceTimeout: 100 });
const buttonPlay = new Gpio(514, 'in', 'rising', { debounceTimeout: 100 });
const buttonNext = new Gpio(515, 'in', 'rising', { debounceTimeout: 100 });
const buttonPlus = new Gpio(527, 'in', 'rising', { debounceTimeout: 100 });

io.on('connection', (socket) => {
  socket.on('card_read', (data) => {
    console.log(`Card read: ${data.id}`);
  });
  socket.on('card_removed', () => {
    console.log(`Card removed`);
  });
});

const main = async () => {
  console.log('Connected to Mopidy');
  mopidy.tracklist?.clear();

  if (!mopidy.tracklist || !mopidy.playback) return;
  await mopidy.mixer?.setVolume({ volume: 50 });

  buttonPrev.watch(async (err) => {
    console.log('Prev button pressed');

    if (!mopidy.tracklist || !mopidy.playback) return;
    if (err) throw err;

    await mopidy.playback.previous();
  });

  buttonNext.watch(async (err) => {
    console.log('Next button pressed');

    if (!mopidy.tracklist || !mopidy.playback) return;
    if (err) throw err;

    await mopidy.playback.next();
  });

  buttonPlus.watch(async (err) => {
    await mopidy.tracklist?.clear();
    console.log('Plus button pressed');

    if (!mopidy.tracklist || !mopidy.playback) return;
    if (err) throw err;

    // play spotify track in mopidy
    await mopidy.tracklist.add({
      uris: ['spotify:album:4SFnIUrbBABqZedVSvKofm'],
    });

    await mopidy.playback.play({});
  });

  buttonPlay.watch(async (err) => {
    console.log('Play button pressed');

    if (!mopidy.tracklist || !mopidy.playback) return;
    if (err) throw err;

    const currentPlaybackState = await mopidy.playback.getState();
    if (currentPlaybackState === 'paused') {
      await mopidy.playback.resume();
    } else if (currentPlaybackState === 'stopped') {
      await mopidy.playback.play({});
    } else if (currentPlaybackState === 'playing') {
      await mopidy.playback.pause();
    }
  });
};

// Debug:
mopidy.on('state', console.log);
mopidy.on('event', console.log);
// ----

io.listen(3000);
mopidy.on('state:online', main);

process.on('SIGINT', () => {
  console.log('unexporting');
  buttonPlus.unexport();
  buttonPrev.unexport();
  buttonPlay.unexport();
  buttonNext.unexport();
  process.exit();
});
