import time
import grovepi
import pygame, sys
from pygame.locals import *
import pygame.camera
import socket

# setup cam
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0", (10000, 5000))

DHT_SENSOR   = 4 #DIGITAL PORT D4 (Temperature & Humidity Sensor Pro)
WATER_SENSOR = 2 #DIGITAL PORT D2 (Water Sensor)
TEMP_SENSOR  = 0 #Analog Port A0 

grovepi.pinMode(WATER_SENSOR, "INPUT")

# There are two humidity sensors, pick one.
BLUE = 0
WHITE = 1

# connect to server
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('poorhackers.com', 9001)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

# Grab Picture #
cam.start()
image = cam.get_image()
pygame.image.save(image, '101.jpg')
cam.stop()        

while True:
    try:
        # Grab temp in C and Humidity in %/100 #
        [temp, humidity] = grovepi.dht(DHT_SENSOR, WHITE)
        
        # convert to F from C
        tempint = ((temp*1.8) + 32)

        #print("DHT: %.02f , %.02f%%" % (temp, humidity))

        # Grab temp in F #
        analog_temp = ( grovepi.temp(TEMP_SENSOR, '1.2')*1.8 ) + 32

        #print("Temperature Sensor: ", temp)

        # Grab Water Present as boolean #
        #water = grovepi.digitalRead(WATER_SENSOR)
        #print("Water Present: ")

        #if (water == 1):
           #print "NO WATER"
        #elif (water == 0):
           #print "WATER"
            #else:
           #print "WATER ERROR"

        # Grab Picture #
        cam.start()
        image = cam.get_image()
        pygame.image.save(image, '101.jpg')
        cam.stop()        

        fileContent = None
        print("Hello")

        with open("101.jpg", mode='rb') as file: #b is important -> binary
            fileContent = file.read()
    
        sock.send(str(len(fileContent)))
        sent = sock.send(fileContent)
        print('File content length: ' + str(len(fileContent)))
        print('sent ' + str(sent))

        #sendem after collection so no IOERROR problems
        time.sleep(5)
        sock.sendall( str(tempint) )
        #time.sleep(1)
        #sock.sendall( str(humidity) )
        #time.sleep(1)
        #sock.sendall( str(water) )        
        #time.sleep(1)

        # Sleep #
        time.sleep(5)

    except KeyboardInterrupt:
        break
    except IOError:
        print ("IOError")
    except TypeError:
        pass
