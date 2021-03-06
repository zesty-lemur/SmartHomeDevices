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
        self.colours = colours
        # CLASS METHODS
        self.methods = {
            'check_array' : self.check_array,
            'clear' : self.clear,
            'percent_on' : self.percent_on,
            'percent_off' : self.percent_off,
        }
        # RATCHET CODE HERE
        if strips:
            d = {}
            for x in range(strips):
                d[x] = {}
                l = []
                [l.append(y) for y in range(int(x*(pixels / strips)), int((x + 1) * (pixels / strips)))]
                d[x]['pixels'] = l
                d[x]['active'] = []
            self.strips = d

    def execute(self, method, params):
        self.methods[method](params)
    
    def check_array(self):
        a, b = sorted(self.strips.keys()), sorted(self.strips.keys(), reverse=True)
        [self.percent_on(params={'strip':y, 'percent':100, 'colour' : None}) for y in a]
        [self.percent_off(params={'strip':y, 'percent':100, 'colour' : None}) for y in b]
    
    def clear(self, params):
        self.fill((000,000,000))
        self.write()

    def percent_on(self, params):
        strip = params['strip']
        percent = params['percent']
        colour = params['colour']
        if not colour:
            colour = self.colours['dim']['green']
        num_pix = int((len(self.strips[strip]['pixels']) * percent) / 100)
        for x in self.strips[strip]['pixels'][:num_pix]:
            l = self.strips[strip]['active']
            l.append(x)
            self.strips[strip]['active'] = l
            self[x] = colour
            self.write()
    
    def percent_off(self, params):
        strip = params['strip']
        percent = params['percent']
        colour = params['colour']
        num_pix = int((len(self.strips[strip]['pixels']) * percent) / 100)
        m = max(self.strips[strip]['active'])
        for x in range(m, m-(num_pix-1)-1, -1):
            l = self.strips[strip]['active']
            l.remove(x)
            self.strips[strip]['active'] = l
            self[x] = self.colours['off']
            self.write()