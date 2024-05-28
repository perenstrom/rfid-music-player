import socketio
from time import sleep
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()

# with socketio.SimpleClient(logger=True, engineio_logger=True) as sio:
with socketio.SimpleClient() as sio:
  sio.connect('http://localhost:3000')

  try:
    while True:
      id = reader.read()
      sio.emit('card_read', {'id': id[0]})
      sleep(5)
  finally:
      GPIO.cleanup()
      raise

