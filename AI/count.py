import csv

csv.field_size_limit(1000000)

with open('tracks_wop.csv', encoding='utf-8') as tracks_file:
    tracks_reader = csv.reader(tracks_file)
    with open('playlists.csv', encoding='utf-8') as playlists_file:
        playlists_reader = csv.reader(playlists_file)
        tracks_ = {}    # empty tracks dictionary
        playlists = {}  # so far haven't used this one
        no_entry = []   # to catch tracks that are not found in tracks_wop.csv

        # creates dictionary with track id's as keys to lists containing:
        # [0] - artist
        # [1] - track name
        # [2] - number of occurrences in playlists
        for row in tracks_reader:
            items = row[0].split(';')
            tracks_[items[0]] = [items[1], items[2], 0]

        # counts occurrences of tracks in playlists
        num_of_tracks_in_playlists = 0
        for playlist in playlists_reader:
            current_playlist = playlist[0].split(';')
            for track in current_playlist[2:]:
                try:
                    tracks_[track][2] += 1
                except KeyError:
                    no_entry.append(track)

        # counts number of tracks that occur more than min_occ
        i = 0
        num_pop_tracks = 0
        min_occ = 1
        num_unique_tracks = len(tracks_)
        for track in tracks_:
            if tracks_[track][2] > min_occ:
                # print(f'{tracks_[track][1]} by {tracks_[track][0]}\n Occurrences: {tracks_[track][2]}\n')
                num_pop_tracks += 1


        print(f'Number of unique tracks {num_unique_tracks}')
        print(f'Number of tracks that occur more than {min_occ} time(s): {num_pop_tracks}')
        print(f'Number of tracks that are not found in tracks_wop: {len(no_entry)}')
