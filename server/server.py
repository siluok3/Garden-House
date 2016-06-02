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
bindata = None
bin_done = False

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        #print("Client connecting: {}\n".format(request.peer))
        print("Client connecting: {}\n")

    def onOpen(self):
        print("WebSocket connection open.\n")
        #self.sendMessage("", False)
                
    def onMessage(self, payload, isBinary):
        global temp, humidity, water, bindata, bin_done;

        if isBinary:
            print("Binary message received: {} bytes\n".format(len(payload)))
        else:
            print("Text message received: {}\n".format(payload.decode('utf8')))
            # echo back message verbatim
            try:
                if bin_done:
                    bin_done = False
                    self.sendMessage(bindata, True)
                    self.sendMessage(temp, False)
                    self.sendMessage(humidity, False)
                    self.sendMessage(water, False)
            except AssertionError:
                pass

    def onClose(self, wasClean, code, reason):
        #print("WebSocket connection closed: {}\n".format(reason))
        print("WebSocket connection closed\n")

    @classmethod
    def broadcast_message(cls, data):
        payload = json.dumps(data, ensure_ascii = False).encode('utf8')
        for c in set(cls.connections):
            reactor.callFromThread(cls.sendMessage, c, payload)


def func(i):
    global temp, humidity, water, bindata, bin_done;

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
                data_size = connection.recv(32)
                uni_data_size = unicode(data_size, errors='ignore')

                if (data_size == ''):
                    continue

                print 'data size = ' + data_size

                bindata = connection.recv( int(data_size) )
                print 'Got bindata size: ' + str(len(bindata))
                total = len(bindata)

                while True:
                    if int(total) == int(data_size):
                        print 'breaking w total of : ' + str(total)
                        bin_done = True
                        break

                    new_data = connection.recv( int(str(data_size)) )
                    bindata += new_data
                    print 'Got bindata size: ' + str(len(new_data))
                    total += len(new_data)
                
                time.sleep(5)

                '''
                bindata += connection.recv(10000)
                bindata += connection.recv(10000)
                bindata += connection.recv(10000)
                bindata += connection.recv(10000)
                bindata += connection.recv(10000)
                bindata += connection.recv(10000)
                '''

                #bindata += connection.recv(60000)
                #print "got bindata 2"
                #temp     = connection.recv(32)
                #print "got temp"
                #humidity = connection.recv(32)
                #print "got hum"
                #water    = connection.recv(32)
                #print "got water"
                #time.sleep(5)
                #print >>sys.stderr, 'received "%s"' % bindata
                #print >>sys.stderr, 'received "%s"' % temp
                #print >>sys.stderr, 'received "%s"' % humidity
                #print >>sys.stderr, 'received "%s"' % water
                
            #if data:
            #    print >>sys.stderr, 'sending data back to the client'
            #    connection.sendall(data)
            #else:
            #    print >>sys.stderr, 'no more data from', client_address
            #    break
        #except ValueError:
            #pass
        #except UnicodeDecodeError:
            #pass
                
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
