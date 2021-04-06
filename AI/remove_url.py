import csv


playlists_file = 'playlists.csv'
tracks_file = 'tracks.csv'

csv.field_size_limit(1000000)

with open(tracks_file, 'r', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile)
    with open('tracks_wop.csv', 'w', encoding='utf-8', newline='') as file:
        spamwriter = csv.writer(file, delimiter=';')
        for row in spamreader:
            new_row = row[0].split(';')
            new_row = new_row[:-2]
            spamwriter.writerow([new_row[0] + ';' + new_row[1] + ';' + new_row[2]])
