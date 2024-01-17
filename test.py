


# fabi = Player()
# fabi.generate_token()

# ugo = Player()

# room = Room(creator=fabi)
# game_code = room.id_generator()

# print(room)

# fabi.get_all_saved_tracks()

# rdtrack = fabi.select_one_random_track()
# print(rdtrack)

# ## prints the 200 to 209th song
# # print('\n', *fabi.saved_tracks[200:210], sep='\n')

def same_tracks(track1, track2):
    if track1 == track2:
        return True
    else:
        return False
    

def does_list_have_duplicates(tracklist):
    index = 1
    for track1 in tracklist:
        for track2 in tracklist[index:]:
            if same_tracks(track1, track2):
                return True
        index += 1
    return False



liste = [1,2,5,3,4,5,6,7,8]
print(does_list_have_duplicates(liste))