import { Server } from "socket.io";

const io = new Server({
  /* options */
});

io.on("connection", (socket) => {
  socket.on("card_read", (data) => {
    console.log(`Card read: ${data.id}`);
  });
});

io.listen(3000);
