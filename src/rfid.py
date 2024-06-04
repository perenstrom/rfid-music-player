import socketio
from time import sleep
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()

# with socketio.SimpleClient(logger=True, engineio_logger=True) as sio:
with socketio.SimpleClient() as sio:
  sio.connect('http://localhost:3000')

  active_id = None

  try:
    while True:
      id = reader.read_id_no_block()
      if id == None:
        id = reader.read_id_no_block()

        if id == None:
          if active_id != None:
            print("Tag removed")
            active_id = None
            sio.emit('card_removed', {'id': id})
      else:
        if active_id != id:
          print("Tag read:")
          print(id)
          active_id = id
          sio.emit('card_read', {'id': id})
      sleep(2)
  finally:
      GPIO.cleanup()
      raise