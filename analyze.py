###Shivam Parikh###
#   Music analytics program to generate conclusions on music listening preferences
import matplotlib.pyplot as plt
import pickle
import numpy
from datetime import datetime

def load_pickle(fname):
    with open(fname, 'rb') as f:
        output = pickle.load(f)
    f.close()
    return output

o = load_pickle('recent_parsed.pkl')

def plot_years_made(compute=False, filter=None):
    if(compute):
        years = {}
        if(filter):
            f_songs = filter(o['songs'])
        else:
            f_songs = o['songs']
        for s in f_songs:
            val = s['Year']
            years[val] = years.get(val, 0) + 1
    else:
        years = o['year_made']
    plt.bar(years.keys(), years.values(), 0.5, color='b')
    plt.show()

def plot_years_added(compute=False, filter=None):
    if(compute):
        years = {}
        if(filter):
            f_songs = filter(o['songs'])
        else:
            f_songs = o['songs']
        for s in f_songs:
            val = s['Date Added'].year
            years[val] = years.get(val, 0) + 1
    else:
        years = o['year_added']
    plt.bar(years.keys(), years.values(), 0.5, color='g')
    plt.show()

def plot_play_count(list):
    # Take list of pickle files, take in their total_play_count and the dates
    ls = []
    for pkl in list:
        t = load_pickle(pkl)
        ls.append((t['file_info']['Date'], t['total_play_count']))
    ls = sorted(ls, key=lambda x:x[0])
    x = [l[0] for l in ls]
    y = [l[1] for l in ls]
    plt.plot(x, y, 'b-')
    plt.show()

def genre_pie(compute=False, filter=None):
    if(compute):
        genres = {}
        for s in songs:
            pass
    else:
        genres = o['genres']
    total = sum(genres.values())
    ls = sorted(list(genres.items()), key=lambda x: x[1])
    g = [x[0] for x in ls]
    p = [(x[1]*100)/total for x in ls]
    fig1, ax1 = plt.subplots()
    ax1.pie(p, labels=g, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')
    plt.show()

# plot_years_added()
# plot_years_made()
genre_pie()
