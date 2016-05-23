import time
import grovepi
import pygame, sys
from pygame.locals import *
import pygame.camera

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

while True:
    try:
        # Grab temp in C and Humidity in %/100 #
        [temp, humidity] = grovepi.dht(DHT_SENSOR, WHITE)
        
        # convert to F from C
        temp = ((temp*1.8) + 32)

        print("DHT: %.02f , %.02f%%" % (temp, humidity))

        # Grab temp in F #
        analog_temp = ( grovepi.temp(TEMP_SENSOR, '1.2')*1.8 ) + 32

        print("Temperature Sensor: ", temp)

        # Grab Water Present as boolean #
        water = grovepi.digitalRead(WATER_SENSOR)
        print("Water Present: ")

        if (water == 1):
           print "NO WATER"
        elif (water == 0):
           print "WATER"
        else:
           print "WATER ERROR"

        # Grab Picture #
        cam.start()
        image = cam.get_image()
        pygame.image.save(image, '101.jpg')
        cam.stop()        

        # Sleep #
        time.sleep(10)

    except KeyboardInterrupt:
        break
    except IOError:
        print ("IOError")
