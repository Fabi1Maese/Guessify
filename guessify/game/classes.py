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


def list_has_duplicates(tracklist):
    index = 1
    for track1 in tracklist:
        for track2 in tracklist[index:]:
            if track1.same_tracks(track2):
                return True
        index += 1
    return False


# define a player object
# a player belongs to a room and listens to tracks
class Player():
    def __init__(self):
        self.saved_tracks = []
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

    
    # return one random track from the list
    def select_one_random_track(self):
        return random.choice(self.saved_tracks)
        # txt_file = self.text_file_path
        # file = open(txt_file, "r")
        # all_tracks = file.read().split('\n')
        # return Track(Spotify.track(self.sp_token, track_id= random.choice(all_tracks)), self.player_id)
    

    def select_several_random_tracks(self, number):
        tracklist = random.choices(self.saved_tracks, k = number)
        while list_has_duplicates(tracklist):
            tracklist = random.choices(self.saved_tracks, k = number)
    


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
    

    def same_tracks(self, other_track):
        if self.artist == other_track.artist and self.title == other_track.title:
            return True
        else:
            return False
    
    
    def not_in_list(self, tracklist):
        for track in tracklist:
            if self.same_tracks(track):
                return False
            else:
                return True
    


# Room object,
class Room():
    def __init__(self, creator):
        self.config = Config()
        self.game_code = ''
        self.players = [creator]
        self.tracks_list = []
        self.points = dict((player.display_name, 0) for player in self.players)

        # game will play 20 songs, changeable with "modify_threshold"
        self.songs_played_threshold = 20


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
        # can't be less or more than the arbitrary settings in the conf file
        if amount >= self.config.minimum_songs_threshold :
            self.songs_played_threshold = amount

        return self.songs_played_threshold
    
    
    def add_player(self, player):
        self.players += [player]

    
    def generate_tracks_played_no_dupes(self):
        # ex : 20 songs 3 players : int(20/3 + 1) (so 6.16666 + 1), effectively rounding up to next int
        nb_of_players = len(self.players)
        tracks_per_player = int( (self.songs_played_threshold / nb_of_players) + 1 ) 

        # create a temporary tracks_list that we will fill up, and from which we will pick at random the songs 
        # that will be played during the game
        tracks_list = []

        for player in self.players:
            # temporary list of pre-selected tracks from a player to add
            tracks_to_add = player.select_several_random_tracks(tracks_per_player)

            for track in tracks_to_add:

                # if a pre-selected track is not already in the final list defined before the loop, add it
                if track.not_in_list(tracks_list):
                    tracks_list.append(track)
                
                # if a pre-selected track is already in the final list, remove it from the temp list and add another random one
                else: 
                    tracks_to_add.remove(track)
                    random_new_track = player.select_one_random_track()
                    tracks_to_add.append(random_new_track)


        self.tracks_list = random.choices(tracks_list, k = self.songs_played_threshold)
        return self.tracks_list
            

    # give points to a player
    def add_points(self, player_name, amount=1):
        self.points[player_name] += amount
        return self.points