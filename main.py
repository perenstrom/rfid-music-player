import configparser
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pyairtable import Table
import time
from mfrc522 import SimpleMFRC522
from gpiozero import Button
from signal import pause
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
config = None
sp = None
reader = None
spotify_map_table = None
spotify_map = None
music_player_id = None
save_tag_btn = None
play_pause_btn = None
previous_btn = None
next_btn = None
current_playing_tag = None
state = "reading"
timer = None

def init_config():
  global config
  config = configparser.ConfigParser(allow_no_value=True)
  config.read("config.cfg")

def init_reader():
  global reader
  reader = SimpleMFRC522()

def init_constants():
  global music_player_id
  music_player_id = config["UIDS"]["player"]

def init_spotify():
  global sp
  sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
      client_id=config["AUTH"]["client_id"],
      client_secret=config["AUTH"]["client_secret"],
      redirect_uri=config["AUTH"]["redirect_uri"],
      scope=config["AUTH"]["scope"],
      open_browser=False
    )
  )
  sp.volume(100, music_player_id)

def init_airtable():
  global spotify_map
  global spotify_map_table
  spotify_map_table = Table(config["AIRTABLE"]["api_key"], config["AIRTABLE"]
                            ["base_id"], config["AIRTABLE"]["table_name"])

def set_airtable_map():
  global spotify_map

  spotify_map_temp = {}
  for record in spotify_map_table.all():
    spotify_map_temp[record["fields"]["id"]
      ] = {
        'uri': record["fields"]["spotify_context_uri"], 
        'airtable_id': record['id']
      }
  spotify_map = spotify_map_temp

def tag_exists(tag):
  return tag in spotify_map

def get_current_device_id():
  device_id = sp.current_playback()["device"]["id"]
  return device_id

def get_current_playing_uri():
  current = sp.current_playback()
  if(current == None):
    return None
  else:
    return current["context"]["uri"]

def get_is_playing():
  playing = sp.current_playback()

  if(playing == None):
    return False
  elif(playing["is_playing"]):
    return True
  else:
    return False

def set_state(value):
  global state
  state = value

def play_tag(tag):
  print("Playing tag", tag)
  sp.start_playback(music_player_id, spotify_map[tag]['uri'])

def stop_playing():
  print("Stopping playback")
  sp.pause_playback(music_player_id)

def start_playing():
  print("Starting playback")
  sp.start_playback(music_player_id)

def previous_track():
  print("Going to previous track")
  sp.previous_track(music_player_id)

def next_track():
  print("Going to next track")
  sp.next_track(music_player_id)

def read_tag():
  id = reader.read_id_no_block()
  if(id == None):
    id = reader.read_id_no_block()
    if(id == None):
      return None
  return str(id)

def handle_save_btn():
  set_state("start_saving")

def handle_play_pause_btn():
  if(get_is_playing()):
    stop_playing()
  else:
    start_playing()
  set_state('reading')

def handle_previous_btn():  
  previous_track()

def handle_next_btn():
  next_track()

def init_buttons():
  global save_tag_btn
  global play_pause_btn
  global previous_btn
  global next_btn
  save_tag_btn = Button(3)
  save_tag_btn.when_pressed = handle_save_btn
  play_pause_btn = Button(4)
  play_pause_btn.when_pressed = handle_play_pause_btn
  previous_btn = Button(14)
  previous_btn.when_pressed = handle_previous_btn
  next_btn = Button(15)
  next_btn.when_pressed = handle_next_btn

def read_and_handle_tag():
  global current_playing_tag
  tag = read_tag()
  if(tag == None and current_playing_tag != None):
    current_playing_tag = None
    stop_playing()
  elif(tag != None and tag != current_playing_tag):
    if(tag_exists(tag)):
      current_playing_tag = tag
      play_tag(tag)
    else:
      print("Tag", tag, "not on record")

def start_saving_mode():
  global timer
  timer = time.time()
  set_state("saving")

def read_and_handle_saving():
  global timer
  time_elapsed = time.time() - timer
  if(time_elapsed < 10):
    tag = read_tag()
    if(tag != None):
      current_playing = get_current_playing_uri()
      if(current_playing == None):
        print("Noting playing, will not save tag")
      else:
        if(tag_exists(tag)):
          print("will update", current_playing, "for tag", tag)
          spotify_map_table.update(spotify_map[tag]['airtable_id'], {'id': tag, 'spotify_context_uri': current_playing})
          set_airtable_map()
        else:
          print("will save", current_playing, "for tag", tag)
          spotify_map_table.create({'id': tag, 'spotify_context_uri': current_playing})
          set_airtable_map()

      timer = None
      set_state("reading")
  else:
    set_state("reading")


def main():
  init_config()
  init_constants()
  init_reader()
  init_spotify()
  init_airtable()
  set_airtable_map()
  init_buttons()

  print("Started")

  while True:
    print(state)
    if(state == "reading"):
      read_and_handle_tag()
    elif(state == "start_saving"):
      start_saving_mode()
    elif(state == "saving"):
      read_and_handle_saving()
    time.sleep(0.5)
  
main()

