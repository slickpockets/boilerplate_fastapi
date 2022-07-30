var url = window.location.hostname;
var socket = io(url+':8000', {
path: '/ws/socket.io', transports:["websocket"]
});
