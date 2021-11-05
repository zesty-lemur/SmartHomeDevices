import time
import network
import esp
esp.osdebug(None)
import gc
gc.collect()


# WIFI CONNECTION
SSID = "Jack's WiFi"
PASS = "Indie2020"

def connect_wifi(SSID, PASS):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('<< Connecting to network [{}] >>'.format(SSID))
        wlan.connect(SSID, PASS)
        while not wlan.isconnected():
            pass
    print('<< Connected. IP: {} >>'.format(wlan.ifconfig()[0]))
    
connect_wifi(SSID, PASS)