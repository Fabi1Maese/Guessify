import spotipy
import spotipy.oauth2 as oauth2
import configparser

config = configparser.ConfigParser()
config.read('conf.ini')
print(config['CREDS']['client_id'])  



# def generate_token():
#     """ Generate the token. Please respect these credentials :) """
#     credentials = oauth2.SpotifyClientCredentials(
#         client_id=client_id,
#         client_secret=client_secret)
#     token = credentials.get_access_token()
#     return token


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


# def write_playlist(username, playlist_id):
#     results = spotify.user_playlist(username, playlist_id,
#                                     fields='tracks,next,name')
#     text_file = u'{0}.txt'.format(results['name'], ok='-_()[]{}')
#     print(u'Writing {0} tracks to {1}'.format(
#             results['tracks']['total'], text_file))
#     tracks = results['tracks']
#     write_tracks(text_file, tracks)


# token = generate_token()
# spotify = spotipy.Spotify(auth=token)

# # example playlist
# write_playlist('doldher', '0B4jhlB6QUGHzY8i3rEwTt')