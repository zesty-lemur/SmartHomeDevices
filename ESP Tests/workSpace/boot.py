from utime import sleep
import network
import esp
esp.osdebug(None)
import gc
gc.collect()


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
    
connect_wifi(SSID, PASS)

@staticmethod
def _otaUpdate():
    ulogging.info('Checking for Updates...')
    from .ota_updater import OTAUpdater
    otaUpdater = OTAUpdater('https://github.com/rdehuyss/chicken-shed-mgr', github_src_dir='src', main_dir='app', secrets_file="secrets.py")
    otaUpdater.install_update_if_available()
    del(otaUpdater)
