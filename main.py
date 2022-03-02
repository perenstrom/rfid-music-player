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

pprint(spotify_map)

sp = spotipy.Spotify(
  auth_manager=SpotifyOAuth(
    client_id=config["AUTH"]["client_id"],
    client_secret=config["AUTH"]["client_secret"],
    redirect_uri=config["AUTH"]["redirect_uri"],
    scope=config["AUTH"]["scope"],
    open_browser=False
  )
)

def getCurrentDeviceId():
  pprint(sp.current_playback()["device"]["id"])

def playTag(tag):
  sp.start_playback(music_player_id, spotify_map[tag])

try:
  print("Started")
  while True:
    id = reader.read_id()
    print(id)
    playTag(str(id))
    time.sleep(0.5)
finally:
  GPIO.cleanup()