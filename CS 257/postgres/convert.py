'''convert.py'''

'''Authors:

    A.J. Ristino & Julian Bowers

'''

import csv

''' CONVERTING ALBUMS.CSV '''

with open("datasource.csv") as csv_file:
    file = csv.reader(csv_file)
    targets_found = set()
    desired_rows = []
    for line in file:
        idstring = line[0].strip('"')
        idstring2 = idstring.strip('.')
        id = int(idstring2)
        numratingsstring = line[7].strip('"')
        numratingsstring2 = numratingsstring.replace(',',"")
        numratings = int(numratingsstring2)
        if line[1] not in targets_found:#If the desired quality  isn't in the 'found' list . . .
            desired_rows.append([id,line[1],line[4],line[5],line[6],numratings,line[8]])#Add desired fields to 'desired' list . . .
            #Add the target quality into the 'found' list . . .
            targets_found.add(line[1])

with open("albums.csv", 'w') as new_file:
    writer = csv.writer(new_file)
    for row in desired_rows:
        writer.writerow(row)

''' CONVERTING ARTISTS.CSV '''

with open("datasource.csv") as csv_file:
    file = csv.reader(csv_file)
    targets_found = set()
    desired_rows = []
    for line in file:
        idstring = line[0].strip('"')
        idstring2 = idstring.strip('.')
        id = int(idstring2)
        artistname = line[2].strip(',')
        if line[2] not in targets_found:
            desired_rows.append([id,artistname])
            targets_found.add(line[2])

with open("artists.csv", 'w') as new_file:
    writer = csv.writer(new_file)
    for row in desired_rows:
        writer.writerow(row)

''' CONVERTING (RELEASE DATES)  RELDATES.CSV '''

with open("datasource.csv") as csv_file:
    file = csv.reader(csv_file)
    targets_found = set()
    desired_rows = []
    for line in file:
        if line[3] not in targets_found:
            idstring = line[0].strip('"')
            idstring2 = idstring.strip('.')
            id = int(idstring2)
            desired_rows.append([id,line[3]])
            targets_found.add(line[3])

with open("reldates.csv", 'w') as new_file:
    writer = csv.writer(new_file)
    for row in desired_rows:
        writer.writerow(row)


