from autobahn.twisted.websocket import WebSocketServerProtocol
import socket
import sys
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory
import time
from threading import Thread

temp = "NULL"
humidity = "NULL"
water = "NULL"
bindata = 0

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        #print("Client connecting: {}\n".format(request.peer))
        print("Client connecting: {}\n")

    def onOpen(self):
        print("WebSocket connection open.\n")
        #self.sendMessage("", False)
                
    def onMessage(self, payload, isBinary):
        global temp, humidity, water;

        if isBinary:
            print("Binary message received: {} bytes\n".format(len(payload)))
        else:
            print("Text message received: {}\n".format(payload.decode('utf8')))
            # echo back message verbatim
            self.sendMessage(temp, False)
            self.sendMessage(humidity, False)
            self.sendMessage(water, False)

    def onClose(self, wasClean, code, reason):
        #print("WebSocket connection closed: {}\n".format(reason))
        print("WebSocket connection closed\n")

    @classmethod
    def broadcast_message(cls, data):
        payload = json.dumps(data, ensure_ascii = False).encode('utf8')
        for c in set(cls.connections):
            reactor.callFromThread(cls.sendMessage, c, payload)


def func(i):
    global temp, humidity, water, bindata;

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('45.55.37.169', 9001)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)
    
    # Listen for incoming connections
    sock.listen(1)    

    # WAIT FOR THE GARDEN HOUSE TO CONNECT
    while True:
        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()

        try:
            print >>sys.stderr, 'connection from', client_address
        
            while True:
                print "AWAITING DATA"
                #bindata  = connection.recv(70000)
                #print "got bindata"
                temp     = connection.recv(32)
                #print "got temp"
                humidity = connection.recv(32)
                #print "got hum"
                water    = connection.recv(32)
                #print "got water"
                #time.sleep(5)
                #print >>sys.stderr, 'received "%s"' % bindata
                print >>sys.stderr, 'received "%s"' % temp
                print >>sys.stderr, 'received "%s"' % humidity
                print >>sys.stderr, 'received "%s"' % water
                
            #if data:
            #    print >>sys.stderr, 'sending data back to the client'
            #    connection.sendall(data)
            #else:
            #    print >>sys.stderr, 'no more data from', client_address
            #    break
            
        finally:
            print "finally"
            #Clean up the connection
            connection.close()

t = Thread(target=func, args=(1,))
t.start()

factory = WebSocketServerFactory()
log.startLogging(sys.stdout)
factory.protocol = MyServerProtocol

reactor.listenTCP(9000, factory)
reactor.run()
