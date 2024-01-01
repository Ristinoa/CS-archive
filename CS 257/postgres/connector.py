'''connector.py'''

import csv

with open("albums.csv") as albums:
    albums_dict = {} # Using dictionary to match key:value pairs
    file = csv.reader(albums)
    for line in file:
        if line[1] not in albums_dict.keys():
            albums_dict[line[1]] = line[0]

with open("artists.csv") as artists:
    artists_dict = {} 
    file = csv.reader(artists)
    for line in file:
        if line[1] not in artists_dict.keys():
            artists_dict[line[1]] = line[0]

with open("reldates.csv") as reldates:
    reldates_dict = {}
    file = csv.reader(reldates)
    for line in file:
        if line[1] not in reldates_dict.keys():
            reldates_dict[line[1]] = line[0]

with open("datasource.csv") as source, open("connector.csv", 'w') as connector:
    writer = csv.writer(connector)
    reader = csv.reader(source)
    for line in reader:
        if line[0] == 'ID':
            continue
        album_id = albums_dict[line[1]]
        artist_id = artists_dict[line[2]]
        reldates_id = reldates_dict[line[3]]
        writer.writerow([album_id, artist_id, reldates_id])
