from autobahn.twisted.websocket import WebSocketServerProtocol

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        #print("Client connecting: {}\n".format(request.peer))
        print("Client connecting: {}\n")

    def onOpen(self):
        print("WebSocket connection open.\n")
        self.sendMessage("Hello", False)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {} bytes\n".format(len(payload)))
        else:
            print("Text message received: {}\n".format(payload.decode('utf8')))

        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        #print("WebSocket connection closed: {}\n".format(reason))
        print("WebSocket connection closed\n")

import sys

from twisted.python import log
from twisted.internet import reactor
log.startLogging(sys.stdout)

from autobahn.twisted.websocket import WebSocketServerFactory
factory = WebSocketServerFactory()
factory.protocol = MyServerProtocol

reactor.listenTCP(9000, factory)
reactor.run()
