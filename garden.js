// Socket Declarations
var ws;

// Websock Declarations
var ws = new WebSocket('ws://localhost:9000', 'garden-protocol');

ws.onmessage = function (event) {
    var msg = event.data;

    switch (msg) {	
	default: console.log("Got " + msg + "\n"); break;
    }
}
