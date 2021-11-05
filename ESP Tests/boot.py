from utime import sleep
import gc
gc.enable()

# WIFI CONNECTION
SSID = "Number_41"
PASS = "Redandyellow123"

def connect_wifi(SSID, PASS):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    attempts = 0
    while not wlan.isconnected():
      attempts += 1
      print('<< Connecting to network [{}] - attempt {} >>'.format(SSID, attempts))
      wlan.connect(SSID, PASS)
      if wlan.isconnected():
        break
      else:
        sleep(5)
    print('<< Connected. IP: {} >>'.format(wlan.ifconfig()[0]))

def update():
    import senko, machine
    OTA = senko.Senko(
        user="jack-baird",
        repo="SmartHomeDevices",
        branch="master",
        working_dir="ESP Tests",
        files=["boot.py","main.py"]
    )
    print("Checking for updates...")
    if OTA.update():
        print("Updated to the latest version! Rebooting...")
        machine.reset()
    print("No updates found. Finishing boot...")

connect_wifi(SSID, PASS)
update()