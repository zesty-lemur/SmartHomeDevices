import utime as time
from pixel import PixelArray, create_frames
import ujson as json

# SYSTEM FUNCTIONS
def restart(reason):
  global client, CLIENT_ID, CLIENT_NAME
  print("<< Restarting. [{}] >>".format(reason))
  msg = '{} [{}] restarting. Reason: {}'.format(CLIENT_NAME, CLIENT_ID, reason)
  client.publish(TOPIC_PUB, msg)
  time.sleep(2)
  machine.reset()
  
sys_funcs = {
  'restart' : restart,
}

# MQTT CONNECTION, CONSTANTS & VARIABLES
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
CLIENT_NAME = 'StairsESP8266'
TOPIC_SUB = b'house/lights/stairs'
TOPIC_PUB = b'house/devices'

start_time = time.time()
message_interval = 10
counter = 1

def connect_and_subscribe(client_id, server, topic_sub):
  client = MQTTClient(client_id, server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('<< Connected to MQTT broker at {}; subscribed to topic "{}" >>'.format(server, topic_sub))
  return client

def sub_cb(topic, msg):
  print("Raw Msg: {}".format(msg)) # For debugging only
  msg = json.loads(msg)
  target = msg['target']
  command = msg['command']
  params = msg['params']
  
  if target == 'system':
    global sys_funcs
    sys_funcs[command](params)
  
  elif target == 'array':
    global array
    array.execute(command, params)

def check_in(client, client_id, counter, topic_pub):
  msg = b'esp8266 [{}] online. Count [{}]'.format(client_id, counter)
  client.publish(topic_pub, msg)
  print("<< Checked in >>")
  last_message = time.time()
  counter += 1
  return counter

try:
  client = connect_and_subscribe(CLIENT_ID, SERVER, TOPIC_SUB)
except OSError as e:
  restart(e)

# INSTANTIATING THE PIXELS
PIN = 13
FRAMES = 4
PIXELS_PER_FRAME = 30
total_pixels, frames = create_frames(FRAMES, PIXELS_PER_FRAME)
array = PixelArray(PIN, total_pixels, frames)
print("<< Checking light array >>")
array.flash_all()
print("<< Check complete >>")

# MAIN LOOP
while True:
  try:
    client.check_msg()
    if (time.time() - start_time) > (message_interval * counter):
      rtn = check_in(client, CLIENT_ID, counter, TOPIC_PUB)
      if rtn != None:
        counter = rtn
  except OSError as e:
    restart(e)


