import socketio
from time import sleep
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()

# with socketio.SimpleClient(logger=True, engineio_logger=True) as sio:
with socketio.SimpleClient() as sio:
  sio.connect('http://localhost:3000')

  try:
    print("hello")
    while True:
      print("Hold a tag near the reader")
      id = reader.read()
      print("here comes the id")
      print(id[0])
      sio.emit('card_read', {'id': id[0]})
      sleep(5)
  finally:
      GPIO.cleanup()
      raise

