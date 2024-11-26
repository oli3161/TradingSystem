const socket = new WebSocket("ws://0.0.0.0:8765");

socket.addEventListener("open", (event) => {
	socket.send("Hello Server!");
});

socket.addEventListener("message", (event) => {
	console.log("Message from server ", event.data);
});
