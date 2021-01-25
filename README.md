# it_project_pong

Simple multiplayer pong game written in pygame and nodejs for IT classes.

Needed dependencies for client: Python+pygame+socketio.
for server: nodejs+socketio+express.

To run server, run that from your shell:
<code>node server.js </code>

There are two variants of clients: A and B, 
once you get proper communication you need to run both clients separetelty on two different machines

In line 116 in both clients you need to write address of your server.

If you are running server from your home network you need to enable ports in firewall, router or sth. 
Server is set on 3000 port

Clients supports sounds files, 
to enable it just uncomment what is between 127 and 132 lines and put your own files in main folder with code, names are written in code.
