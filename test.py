import spotipy
import spotipy.oauth2 as oauth2
import webbrowser
import urllib.parse
import base64
import requests
from spotipy.oauth2 import SpotifyOAuth 
from pathlib import Path
import random 
import string
from config import Config
from spotipy.client import Spotify

# define a player object
# a player belongs to a room 
class Player():
    def __init__(self):
        self.saved_tracks = []
        self.points = 0
        self.config = Config()
        # self.temp_files_path = room.config.tempfiles_path
        # self.text_file_path = self.temp_files_path +  '/' + self.room.game_code + '/' + self.player_id + ".txt"

    
    def __str__(self):
        return self.display_name


    # generate session token
    def generate_token(self):
        """ Generate the token. Please respect these credentials :) """
        sp_token = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.config.client_id, client_secret=self.config.client_secret,
                                                              redirect_uri=self.config.redirect_uri, scope="user-library-read"))
        self.sp_token = sp_token
        self.player_id = sp_token.me()['id']
        self.display_name = sp_token.me()['display_name']
        return sp_token
    
    
    # write all saved tracks of the session player 
    def get_all_saved_tracks(self):
        # temp_files_path = self.temp_files_path
        # game_code = self.game_code
        sp_token = self.sp_token

        ## creates tempfiles/gamecode path if not exists
        # Path(temp_files_path + '/' + game_code).mkdir(parents=True, exist_ok=True)

        current_offset = 0
        while True:
            # limit has a maximum of 50 tracks at a time
            results = sp_token.current_user_saved_tracks(limit = 50, offset=current_offset)
            self.write_tracks_url_to_player(results)
            # 1 set of results = 50 tracks
            # check if there's more
            if results['next']:
                current_offset += 50

            else:
                break

    ## write a batch of 50 tracks urls into the player's list
    def write_tracks_url_to_player(self, player_saved_tracks):
        # text_file_path = self.text_file_path
        # with open(text_file_path, 'a') as file_out:
        for idx, item in enumerate(player_saved_tracks['items']):
                track = item['track']
                self.saved_tracks += [Track(track, self.player_id)]
                # track_url = track['external_urls']['spotify']
                # file_out.write(track_url + '\n')
            # file_out.close()

    
    # return one random track oin a txt file
    def select_one_random_track(self):
        return random.choice(self.saved_tracks)
        # txt_file = self.text_file_path
        # file = open(txt_file, "r")
        # all_tracks = file.read().split('\n')
        # return Track(Spotify.track(self.sp_token, track_id= random.choice(all_tracks)), self.player_id)


    # give points to a player
    def add_points(self, amount=1):
        self.points += amount
        return self.points


# Track object, which has a Sp url, name & artist
# also includes the json just in case
class Track():
    def __init__(self, track_json, player):
        self.players = [player]
        self.track_json = track_json
        self.url = self.track_json['external_urls']['spotify']
        self.artist = self.track_json['artists'][0]['name']
        self.title = self.track_json['name']
    
    def __str__(self):
        return self.artist + ' - ' + self.title


    def add_player(self, player):
        if player not in self.players:
            self.players += [player] 
        return self.players
    

# Room object,
class Room():
    def __init__(self, creator):
        self.config = Config()
        self.game_code = ''
        self.players = [creator]

        # takes 20 points to win the game, changeable with "modify_threshold"
        self.points_win_threshold = 20


    def __str__(self):
        players = ''
        for player in self.players:
            players += player.display_name + ' '
        return self.game_code + ' ' + players


    # generate game room ID 
    def id_generator(self):
        code_size = int(self.config.game_code_size)
        game_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=code_size))
        self.game_code = game_code
        return game_code


    def modify_threshold(self, amount):
        # can't be less than the arbitrary 5 that's in the conf file
        if amount >= self.config.minimum_points_threshold :
            self.points_win_threshold = amount

        return self.points_win_threshold
    
    
    def add_player(self, player):
        self.players += [player]


fabi = Player()
fabi.generate_token()

ugo = Player()

room = Room(creator=fabi)
game_code = room.id_generator()

print(room)

fabi.get_all_saved_tracks()

rdtrack = fabi.select_one_random_track()
print(rdtrack)

## prints the 200 to 209th song
# print('\n', *fabi.saved_tracks[200:210], sep='\n')