import machine, neopixel, urandom
import ujson as json
from time import sleep

# RANDINT FUNCTION NOT AVAILABLE IN
# MICROPYTHON STANDARD LIBRARY
def randint(min, max):
    span = max - min + 1
    div = 0x3fffffff // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val

# PIXEL ARRAY DEFINITION FUNCTION
def create_frames(no_frames, pixels_per_frame):
  total_pixels = no_frames * pixels_per_frame
  frames = {}
  for x in range(no_frames):
    for y in range(pixels_per_frame):
      frame = []
      first_pixel = x * pixels_per_frame
      last_pixel = first_pixel + 29
      for pixel in range(first_pixel, last_pixel + 1):
        frame.append(pixel)
    frames[x] = frame
  return total_pixels, frames

class PixelArray:
  def __init__(self, pin, total_pixels, frames):
    self.tp = total_pixels
    self.pin = pin
    self.array = neopixel.NeoPixel(machine.Pin(self.pin), self.tp)
    self.frames = frames
 
  def clear(self):
    self.array.fill((0, 0, 0))
    self.array.write()

  def on(self, pixels='all', colour=100100100):
    print("<< Command called. Params: {} / {} >>".format(pixels, colour))
    if pixels == 'all':
      pixels = []
      print(pixels)
      for i in range(self.tp):
        pixels.append(i)
    if type(pixels) == list:
      for pixel in pixels:
        print(self.array, pixel)
        self.array[int(pixel)] = colour
        self.array.write()
    else:
      self.array[pixels] = colour
      self.array.write()    

  def execute(self, command, params):
    class_funcs = {
    'random' : self.random,
    'flash_all' : self.flash_all,
    'on' : self.on,
    }
    class_funcs[command](params)
  
  @staticmethod
  def rgb_parse(rgb_string):
    """
    Parses a 9-character string of rgb values to a tuple of 3x 3-digits
    """
    rgb_string = rgb_string.strip('rgb=')
    r = int(rgb_string[:3])
    g = int(rgb_string[3:6])
    b = int(rgb_string[6:9])
    rgb = (r,g,b)
    return rgb

# FANCY FUNCTIONS BELOW - REMOTELY EXECUTED
  def random(self, cycles=1):
    for x in range(cycles):
      for i in range(self.tp):
        r = randint(0,255)
        g = randint(0,255)
        b = randint(0,255)
        self.array[i] = (r, g, b)
        self.array.write()
      sleep(0.5)
      self.clear()
  
  def flash_all(self, rgb=(0,100,0)):
    if type(rgb) == str:
      rgb = self.rgb_parse(rgb)
    for x in range(2):
      self.array.fill(rgb)
      self.array.write()
      sleep(0.25)
      self.clear()
      sleep(0.25)

  def scroll(self):
    for frame in self.frames.keys():
      for pixel in self.frames[frame]:
        r = randint(0,255)
        g = randint(0,255)
        b = randint(0,255)
        self.array[pixel] = (r,g,b)
        self.array.write()
        sleep(0.1)
        self.array[pixel] = (0,0,0)
        self.array.write()