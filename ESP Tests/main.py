import machine
from neopixel import NeoPixel
from utime import sleep

# LED STRIP SETUP
PIX_PIN = 14
T_PIX = 30

lights = NeoPixel(machine.Pin(PIX_PIN), T_PIX)

# LIGHT FUNCTIONS
def lights_on():
  lights.fill((50,0,0))
  lights.write()

def lights_off():
  lights.fill((0,0,0))
  lights.write()

# ENSURE LIGHTS OFF ON START
lights_off()

while True:
    lights_on()
    sleep(1)
    lights_off()
    sleep(1)