import configparser
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pyairtable import Table
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.cfg")

music_player_id = config["UIDS"]["player"]

reader = SimpleMFRC522()

spotify_map_table = Table(config["AIRTABLE"]["api_key"], config["AIRTABLE"]
                          ["base_id"], config["AIRTABLE"]["table_name"])
spotify_map = {}
for record in spotify_map_table.all():
  spotify_map[record["fields"]["id"]
    ] = record["fields"]["spotify_context_url"]

sp = spotipy.Spotify(
  auth_manager=SpotifyOAuth(
    client_id=config["AUTH"]["client_id"],
    client_secret=config["AUTH"]["client_secret"],
    redirect_uri=config["AUTH"]["redirect_uri"],
    scope=config["AUTH"]["scope"],
    open_browser=False
  )
)

def get_current_device_id():
  device_id = sp.current_playback()["device"]["id"]
  return device_id

def play_tag(tag):
  print("Playing tag", tag)
  sp.start_playback(music_player_id, spotify_map[tag])

def stop_playing():
  print("Stopping playback")
  sp.pause_playback(music_player_id)

def read_tag():
  id = reader.read_id_no_block()
  if(id == None):
    id = reader.read_id_no_block()
    if(id == None):
      return None
  return str(id)

def main():
  print("Started")
  current_playing_tag = None

  try:
    while True:
      tag = read_tag()
      if(tag == None and current_playing_tag != None):
        current_playing_tag = None
        stop_playing()
      elif(tag != None and tag != current_playing_tag):
        current_playing_tag = tag
        play_tag(tag)

      time.sleep(1)
  finally:
    GPIO.cleanup()

main()

