const socket = new WebSocket("ws://0.0.0.0:8765/test");

socket.addEventListener("open", (event) => {
	socket.send("BUY:AAPL:10:150.0");
	socket.send("SELL:AAPL:10:160.0");
});

socket.addEventListener("message", (event) => {
	console.log("Message from server ", event.data);
});
