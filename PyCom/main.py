from network import LoRa
import socket
import time
from pycoproc_1 import Pycoproc
import ubinascii
import cayenneLPP
from SI7006A20 import SI7006A20

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('1096777862C42F16C6666C7E16E4C091')

print('Joining LoRa network...')
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined')
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

s.setblocking(True)

py = Pycoproc(Pycoproc.PYSENSE)
dht = SI7006A20(py)

while True:
    print('Sending temperature...')
    lpp = cayenneLPP.CayenneLPP(size = 100, sock = s)
    lpp.add_temperature(dht.temperature())
    lpp.add_relative_humidity(dht.humidity())
    lpp.send()
    print('Sent')
    time.sleep(60)