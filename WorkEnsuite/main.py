import machine
import ujson as json
from utime import sleep, time
from umqttsimple import MQTTClient
from neopixel import NeoPixel
from ldr import LDR

# SYSTEM FUNCTIONS
def restart(reason):
  print("<< Restarting. [{}] >>".format(reason))
  sleep(2)
  machine.reset()

# MOSQUITTO SETUP
CLIENT_ID = 'EnsuiteController'
MQTT_SERVER = '192.168.1.116'
TOPIC_SUB = 'Ensuite'
TOPIC_PUB = 'Devices'

birth = time()
msg_interval = 10
msg_counter = 0

def sub_cb(topic, msg):
  global state
  try:
    msg = json.loads(msg)
    r, g, b = msg['r'], msg['g'], msg['b']
    state = (r,g,b)
    colour(state)
  except Exception as e:
    print("<< Error: {} >>".format(e))

def connect_and_subscribe(client_id, server, topic_sub):
  client = MQTTClient(client_id, server, port=1883)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print("<< Connected to broker at {}, subscribed to {} >>".format(MQTT_SERVER, TOPIC_SUB))
  return client

def restart_and_reconnect():
  sleep(5)
  machine.reset()

# AUTOMATED LIGHT SETUP
SLEEP_TIME = 30

# LED STRIP SETUP
PIX_PIN = 14
T_PIX = 30

lights = NeoPixel(machine.Pin(PIX_PIN), T_PIX)

state = (0,0,0)

# LDR SETUP
LDR_PIN = 0

ldr = LDR(LDR_PIN)

# PIR SETUP
motion = False

def handle_interrupt(pin):
  global motion
  motion = True

pir = machine.Pin(5, machine.Pin.IN)

pir.irq(trigger=machine.Pin.IRQ_RISING, handler=handle_interrupt)

# LIGHT FUNCTIONS
def lights_on():
  lights.fill((50,0,0))
  lights.write()

def lights_off():
  lights.fill((0,0,0))
  lights.write()

def colour(col):
  r, g, b = col
  lights.fill((r, g, b))
  lights.write()


# ENSURE LIGHTS OFF ON START
lights_off()

try:
  client = connect_and_subscribe(CLIENT_ID, MQTT_SERVER, TOPIC_SUB)
except OSError as e:
  print("<< Error: {} >>".format(e))
  restart_and_reconnect()


while True:

  try:

    client.check_msg()

    if (time() - birth) > (msg_interval * msg_counter):
      client.publish(TOPIC_PUB, "EnsuiteController online [{}]".format(msg_counter))
      msg_counter += 1

  except OSError as e:
    print("<< Error: {}".format(e))

    # if motion and ldr.value() < 5:

    #     lights_on()
    #     sleep(SLEEP_TIME)
    #     lights_off()
    #     motion = False