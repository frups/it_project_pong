# it_project_pong
simple multiplayer pong game written in pygame and nodejs for IT classes

needed dependencies for client: pygame, socketio

to run server you need to have nodejs with socketio and express modules installed aswell 
and run for example from powershell using command:
node server.js 

there are two variant of clients A and B, you need to run every of that once to get properly communication

in line 116 in both clients you need to write address of your server

if you are running server from your home network you need to enable ports in firewall, router or sth. server is set on 3000 port

clients supports sounds files just uncomment what is between 127 and 132 lines and put your own files in main folder with code, names are written in code
