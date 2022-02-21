import configparser
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pyairtable import Table

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.cfg")

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

music_player_id = config["UIDS"]["player"]
pprint(spotify_map)
sp.start_playback(music_player_id, spotify_map['asdf'])
