import spotipy
import spotipy.oauth2 as oauth2
import configparser
import webbrowser
import urllib.parse
import base64
import requests
from spotipy.oauth2 import SpotifyOAuth 
from pathlib import Path
import random 
import string

config = configparser.ConfigParser()
config.read('conf.ini')

client_id = config['CREDS']['client_id']
client_secret = config['CREDS']['client_secret']
redirect_uri = config['CREDS']['redirect_uri']

# auth_headers = {
#     "client_id": client_id,
#     "response_type": "code",
#     "redirect_uri": config['CREDS']['redirect_uri'],
#     "scope": "user-library-read"
# }

# auth_code = config['CREDS']['auth_code']
# webbrowser.open("https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(auth_headers))

# encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

# token_headers = {
#     "Authorization": "Basic " + encoded_credentials,
#     "Content-Type": "application/x-www-form-urlencoded"
# }

# token_data = {
#     "grant_type": "authorization_code",
#     "code": auth_code,
#     "redirect_uri": config['CREDS']['redirect_uri']
# }

# r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
# token = r.json()

# try : 
#     print(token["access_token"])
# except:
#     print("invalid token")


# define the User object
class User():
    def __init__(self, sp_token):
        self.sp_token = sp_token
        self.user_id = sp_token.me()['id']
        self.display_name = sp_token.me()['display_name']
        self.saved_tracks = []
        self.temp_files_path = config['tempfiles']['path']
        self.text_file_path = self.temp_files_path +  '/' + game_code + '/' + self.user_id + ".txt"


    def assign_to_room(self, game_code):
        self.game_code = game_code

    # write all saved tracks of the session user 
    def write_all_saved_tracks_url(self):
        temp_files_path = self.temp_files_path
        game_code = self.game_code
        sp_token = self.sp_token

        # creates tempfiles/gamecode path if not exists
        Path(temp_files_path + '/' + game_code).mkdir(parents=True, exist_ok=True)

        current_offset = 0
        while True:
            # limit has a maximum of 50 tracks at a time
            results = sp_token.current_user_saved_tracks(limit = 50, offset=current_offset)
            self.write_tracks_url_to_txt(results)
            # 1 set of results = 50 tracks
            # check if there's more
            if results['next']:
                current_offset += 50

            else:
                break

    # write a batch of 50 tracks urls into the appropriate txt file
    def write_tracks_url_to_txt(self, user_saved_tracks):
        text_file_path = self.text_file_path
        with open(text_file_path, 'a') as file_out:
            for idx, item in enumerate(user_saved_tracks['items']):
                    track = item['track']
                    track_url = track['external_urls']['spotify']
                    file_out.write(track_url + '\n')
            file_out.close()

    
    # return one random track url in a txt file
    def select_one_random_track(self):
        txt_file = self.text_file_path
        file = open(txt_file, "r")
        all_tracks = file.read().split('\n')
        return random.choice(all_tracks)


class Track():
    def __init__(self, url):
        self.url = url
    


# generate session token
def generate_token():
    """ Generate the token. Please respect these credentials :) """
    sp_token = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="user-library-read"))

    return sp_token


# generate game room ID 
def id_generator():
    code_size = int(config['settings']['game_code_size'])
    game_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=code_size))
    return game_code


game_code = id_generator()
sp_token = generate_token()

fabi = User(sp_token)
fabi.assign_to_room(game_code)
fabi.write_all_saved_tracks_url()
rdtrack = fabi.select_one_random_track()
print(rdtrack)
# write_all_saved_tracks_url(sp_token, game_code)


text_file_path = "./tempfiles/YPAM/21uplahr2yn5wjynybk5vv3nq.txt"
# print(select_one_random_track(text_file_path))

# def write_tracks(text_file, tracks):
#     with open(text_file, 'a') as file_out:
#         while True:
#             for item in tracks['items']:
#                 if 'track' in item:
#                     track = item['track']
#                 else:
#                     track = item
#                 try:
#                     track_url = track['external_urls']['spotify']
#                     file_out.write(track_url + '\n')
#                 except KeyError:
#                     print(u'Skipping track {0} by {1} (local only?)'.format(
#                             track['name'], track['artists'][0]['name']))
#             # 1 page = 50 results
#             # check if there are more pages
#             if tracks['next']:
#                 tracks = spotify.next(tracks)
#             else:
#                 break