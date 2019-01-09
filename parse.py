###Shivam Parikh###
#   Music analytics program to generate conclusions on music listening preferences
import numpy as np
from lxml import etree as ET
import xml
from datetime import datetime
import time
import pickle

file = "recent.xml"
e = ET.parse(file)
r = e.getroot()
info = r[0]
strptime = datetime.strptime
def save_dict(dictionary, fname):
    out = fname.split(".")[-2] + '_parsed.pkl'
    with open(out, 'wb') as f:
        pickle.dump(dictionary, f)
    f.close()
# File Variables
file_info = dict() #metadata for the file being parsed
songs = [] #list of all songs as dictionaries
artists = dict() #counter for artists
albums = set() #unique albums
genres = dict() #counter for genres
year_added = dict() #counter for years added to library
year_made = dict() #counter for years songs written
total_play_count = 0

for i in range(0, len(info), 2):
    if(info[i+1].text):
        if(info[i].text == 'Date'):
            file_info[info[i].text] = strptime(info[i+1].text, "%Y-%m-%dT%H:%M:%SZ")
        else:
            file_info[info[i].text] = info[i+1].text
    if(info[i].text == 'Tracks'):
        t_index = i
        tracks = info[i+1]

for i in range(0, len(tracks), 2):
    if(tracks[i].tag=="key" and tracks[i+1].tag=="dict"):
        k = int(tracks[i].text)
        song = tracks[i+1]
        d = dict()
        add = True
        for j in range(0, len(song), 2):
            key = song[j].text
            value = song[j+1].text
            # d[key] = d[value]
            if(key=='Podcast' or key=='Movie' or key=='Audiobooks'):
                add = False
                break
            elif(key=='Album'):
                albums.add(value)
            elif(key=='Artist'):
                artists[value] = artists.get(value, 0) + 1
            elif(key=='Year'):
                value = int(value)
                year_made[value] = year_made.get(value, 0) + 1
            elif(key=='Track ID'):
                value = int(value)
            elif(key=='Total Time'):
                value = int(value)
            elif(key=='Size'):
                value = int(value)
            elif(key=='Genre'):
                genres[value] = genres.get(value, 0) + 1
            elif(key=='Explicit'):
                value = song[j+1].tag=="true"
            elif(key=='Date Modified'):
                try:
                    value = strptime(value, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    print("Mismatched date mod format for TrackID %s with datetime %s" % (k, value))
            elif(key=='Date Added'):
                try:
                    value = strptime(value, "%Y-%m-%dT%H:%M:%SZ")
                    year_added[value.year] = year_added.get(value.year, 0) + 1
                except ValueError:
                    print("Mismatched date add format for TrackID %s with datetime %s" % (k, value))
            elif(key=='Play Date UTC'):
                try:
                    value = strptime(value, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    print("Mismatched date play format for TrackID %s with datetime %s" % (k, value))
            elif(key=='Skip Date'):
                try:
                    value = strptime(value, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    print("Mismatched skip date format for TrackID %s with datetime %s" % (k, value))
            elif(key=='Skip Count'):
                value = int(value)
            elif(key=='Play Count'):
                value = int(value)
                total_play_count += value
            elif(key=='Bit Rate'):
                value = int(value)
            elif(key=='Sample Rate'):
                value = int(value)
            elif(key=='Rating'):
                value = int(value)
            elif(key=='Clean'):
                key = 'Explicit'
                value = song[j+1].tag!="true"
            elif(key=='Play Date'):
                value = int(value)
            d[key] = value
        if(add):
            songs.append(d)
    else:
        print("Encountered unordered pair")
        break

output = {"file_info": file_info, "songs": songs,
            "artists": artists, "albums":albums,
            "genres": genres, "year_added": year_added,
            "year_made": year_made, "total_play_count":total_play_count}
save_dict(output, file)
