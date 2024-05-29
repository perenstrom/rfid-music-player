import Mopidy from 'mopidy';
const mopidy = new Mopidy({
  webSocketUrl: 'ws://localhost:6680/mopidy/ws/',
});

mopidy.on('state', console.log);
mopidy.on('event', console.log);

mopidy.on('state:online', async () => {
  console.log('Connected to Mopidy');

  if (mopidy.tracklist && mopidy.playback) {
    // play spotify track in mopidy
    await mopidy.tracklist.add({
      uris: ["spotify:track:6zlBbflwOH6hMa3wBJwDAc"],
    });
    await mopidy.playback.play({});

    setTimeout(() => {
      mopidy.playback?.stop();
    }, 10000);
  }
});
