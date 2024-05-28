import Mopidy from "mopidy";
const mopidy = new Mopidy({
  webSocketUrl: "ws://localhost:6680/mopidy/ws/",
});

mopidy.on("state", console.log);
mopidy.on("event", console.log);

mopidy.on("state:online", async () => {
  console.log("Connected to Mopidy");

  // play spotify track in mopidy
  await mopidy.tracklist.add({
    uris: ["/usr/share/sounds/alsa/Front_Center.wav"],
  });
  await mopidy.playback.play();
});
