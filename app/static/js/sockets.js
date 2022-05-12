var url = window.location.hostname;
var socket = io(url+':8000', {
path: '/ws/socket.io'
});

socket.on("hi", function() {
  console.log("hi")
})
socket.on("test", function(msg){
  console.log("test")
})
