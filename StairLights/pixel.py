import machine
from neopixel import NeoPixel
import ujson as json
import urandom as random
from utime import sleep
from colours import colours

# RANDINT FUNCTION NOT AVAILABLE IN
# MICROPYTHON STANDARD LIBRARY
def randint(min, max):
    span = max - min + 1
    div = 0x3fffffff // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val

class Pixel(NeoPixel):
    def __init__(self, pin, pixels, strips=None):
        super().__init__(machine.Pin(pin), pixels)
        # COLOUR DICTIONARY
        #[ ]: Make this an import
        self.colours = colours
        # RATCHET CODE HERE
        if strips:
            d = {}
            for x in range(strips):
                l = []
                [l.append(y) for y in range(int(x*(pixels / strips)), int((x + 1) * (pixels / strips)))]
                d[x] = l
            self.strips = d
            del d, l, x
    
    def clear(self):
        self.fill((000,000,000))
        self.write()

    def percent_on(self, strip, percent):
        num_pix = int((len(self.strips[strip]) * percent) / 100)
        for x in self.strips[strip][:num_pix]:
            print(x)
            print(self[x])
            self[x] = (100,100,100)
            self.write()
    
    def percent_off(self, strip, percent):
        num_pix = int((len(self.strips[strip]) * percent) / 100)
        for x in self.strips[strip][num_pix::-1]:
            print(x)
            print(self[x])
            self[x] = (000,000,000)
            self.write()