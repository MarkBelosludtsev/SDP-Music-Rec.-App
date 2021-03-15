# filter out Spotify (Spotify Originals?) and playlists > some size (50?)

import sys
import csv
import spotipy
import spotipy.util as util
import os.path


scope = 'user-library-read'
# You can get credentials from https://developer.spotify.com/dashboard/applications
username = 'samiam22228'
client_id='294228a969f74f44b6bfbc4d294d10dd'
client_secret='f7d44d057afe465da3f2da0fa8f88c84'
redirect_uri='https://www.google.com/'

csv.field_size_limit(1000000) # for really long playlists!

def get_tracks_from_playlist(sp, playlist_id):
    playlist_tracks = []
    playlist_tracks_ids = []
    if sp is None:
        token = util.prompt_for_user_token(username,scope, client_id, client_secret, redirect_uri)
        sp = spotipy.Spotify(token)
    try:
        results = sp.user_playlist(username, playlist_id, fields='tracks,next')
    except spotipy.client.SpotifyException:
        token = util.prompt_for_user_token(username,scope, client_id, client_secret, redirect_uri)
        sp = spotipy.Spotify(token)
        results = sp.user_playlist(username, playlist_id, fields='tracks,next')
    tracks = results['tracks']
    while tracks:
        track_ids = []
        for item in tracks['items']:
            track = item['track']
            if track and 'id' in track and track['id']:
                track_ids.append(track['id'])
        for item in tracks['items']:
            track = item['track']
            if track and 'id' in track and track['id']:
                playlist_tracks_ids.append(track['id'])
                artist = track['artists'][0]['name']
                if artist: artist = artist.replace(';', '')
                else: artist = ''
                name = track['name']
                if name: name = name.replace(';', '')
                else: name = ''
                playlist_tracks.append((artist, name, track['preview_url']))
        if tracks['next']:
            try:
                tracks = sp.next(tracks)
            except:
                token = util.prompt_for_user_token(username,scope, client_id, client_secret, redirect_uri)
                sp = spotipy.Spotify(token)
                tracks = sp.next(tracks)
        else:
            tracks = None
    return sp, playlist_tracks_ids, playlist_tracks

def get_playlists():
    playlists_ = {}
    # read temporary file (if exists)
    if os.path.exists('playlists_temp.csv'):
        with open('playlists_temp.csv', 'r', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                columns = str(row)[2:-2].split(';')
                playlists_[columns[0]] = (columns[1], columns[2], None)
            print('Found', len(playlists_), 'playlists')
    token = util.prompt_for_user_token(username,scope, client_id, client_secret, redirect_uri)
    sp = spotipy.Spotify(token)
    # output each playlist (temporarily) as name, owner
    with open('playlists_temp.csv', 'a+', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        for search in range(ord('+'), ord('@') + 1): #A to z
            i = 0
            try:
                playlists = sp.search(chr(search), 10, 0, 'playlist')
            except spotipy.client.SpotifyException:
                token = util.prompt_for_user_token(username,scope, client_id, client_secret, redirect_uri)
                sp = spotipy.Spotify(token)
                playlists = sp.search(chr(search), 10, 0, 'playlist')
            while playlists:
                for playlist in playlists['playlists']['items']:
                    if not(playlist['id'] in playlists_):
                        name = playlist['name']
                        if name: name = name.replace(';', '')
                        else: name = ''
                        owner = playlist['owner']['display_name']
                        if owner: owner = owner.replace(';', '')
                        else: owner = ''
                        playlists_[playlist['id']] = (name, owner, None)
                        spamwriter.writerow([playlist['id'] + ';' + name + ';' + owner])
                i = i + 1
                sys.stdout.write('\r')
                sys.stdout.write('%c (%d/100): %d playlists' % (chr(search), i, len(playlists_)))
                sys.stdout.flush()
                if i < 100 and 'next' in playlists['playlists']: # i < 200
                    try:
                        playlists = sp.next(playlists['playlists'])
                    except spotipy.client.SpotifyException:
                        token = util.prompt_for_user_token(username,scope, client_id, client_secret, redirect_uri)
                        sp = spotipy.Spotify(token)
                        playlists = sp.next(playlists['playlists'])
                else:
                    playlists = None
    print()
    return playlists_

def get_tracks_from_playlists(playlists={}):
    sp = None
    # read file (if exists)
    tracks_ = {}

    # ["37i9dQZF1DX5IOhx43PGIa;Jasmine;Spotify"]
    # my work v
    if os.path.exists('playlists_temp.csv') and not playlists:
        with open('playlists_temp.csv', 'r', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                columns = str(row)[2:-2].split(';')
                playlists[columns[0]] = (columns[1], columns[2], None)
    # my work ^

    if os.path.exists('tracks.csv'):
        with open('tracks.csv', "r", encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                columns = str(row)[2:-2].split(';')
                tracks_[columns[0]] = (columns[1], columns[2], columns[3])
    already_done = 0
    done_ids = {}
    if os.path.exists('playlists.csv'):
        with open('playlists.csv', "r", encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                columns = str(row)[2:-2].split(';')
                done_ids[columns[0]] = 1
                already_done = already_done + 1
    print('Already done %d/%d' % (already_done, len(playlists)))
    # output each track as id, artist name, name, preview url
    with open('tracks.csv', 'a+', newline='', encoding='utf-8') as csvfile_tracks:
        spamwriter_tracks = csv.writer(csvfile_tracks, delimiter=';')
        with open('playlists.csv', 'a+', newline='', encoding='utf-8') as csvfile_playlists:
            spamwriter_playlists = csv.writer(csvfile_playlists, delimiter=';')
            caught_up = 0
            for j, key in enumerate(playlists.keys()):
                if not(caught_up):
                    if j < already_done or key in done_ids: # might have had to skip some
                        continue
                    else:
                        print('Starting with playlist', j)
                        caught_up = 1
                try:
                    sp, playlist_tracks_ids, playlist_tracks = get_tracks_from_playlist(sp, key)
                except spotipy.client.SpotifyException:
                    print('Missing playlist', playlists[key][0], 'by', playlists[key][1])
                    continue
                for i in range(0, len(playlist_tracks_ids)):
                    track_key = playlist_tracks_ids[i]
                    if not(track_key in tracks_):
                        tracks_[track_key] = playlist_tracks[i]
                        if tracks_[track_key][2]:
                            url = tracks_[track_key][2]
                        else:
                            url = ''
                        spamwriter_tracks.writerow([track_key + ';' + tracks_[track_key][0] + ';' + tracks_[track_key][1] + ';' + url + ';'])
                playlists[key] = (playlists[key][0], playlists[key][1], playlist_tracks_ids)
                playlist = playlists[key]
                if (len(playlist[2]) > 0):
                    tracks = ''
                    for i in range(len(playlist[2]) - 1):
                        tracks = tracks + str(playlist[2][i]) + ';'
                    tracks = tracks + str(playlist[2][len(playlist[2]) - 1])
                    spamwriter_playlists.writerow([playlist[0] + ';' + playlist[1] + ';' + tracks])
                sys.stdout.write('\r')
                sys.stdout.write('playlist %d/%d: %d tracks' % (j + 1, len(playlists), len(tracks_)))
                sys.stdout.flush()
    print()
    return tracks_

# main
playlists = get_playlists()
# tracks = get_tracks_from_playlists()
# print('TOTAL :', len(playlists), 'playlists') # , len(tracks), 'tracks')
