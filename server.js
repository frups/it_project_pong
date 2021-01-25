const express = require('express');
const socketIO = require('socket.io');
const PORT = process.env.PORT || 3000;
const INDEX = '/index.html';

const server = express()
  .use((req, res) => res.sendFile(INDEX, { root: __dirname }))
  .listen(PORT, () => console.log(`listening on ${PORT}`));

const io = socketIO(server, always_connect=true);


io.on("connection", (socket) => {
  console.log('client connected');
  socket.on('close', () => console.log('client disconnected'));
  socket.on('a', (arg) => {
    console.log(arg); 
	socket.broadcast.emit('r',arg);
  });
  socket.on('b', (arg) => {
    console.log(arg); 
	socket.broadcast.emit('r',arg);
  });
});
