###Shivam Parikh, Copyright 2019###
### Please do not share or copy without credit to the author.
#   Music analytics program to generate conclusions on music listening preferences
import matplotlib.pyplot as plt
import pickle
import numpy
from datetime import datetime
import os

def load_pickle(fname):
    with open(fname, 'rb') as f:
        output = pickle.load(f)
    f.close()
    return output

def load_all(dir):
    ls = []
    for file in os.listdir(dir):
        if file.endswith(".pkl"):
            ls.append(os.path.join(dir, file))
    print(ls)
    return ls

def plot_years_made(o, compute=False, filter=None):
    if(compute):
        years = {}
        if(filter):
            f_songs = filter(o['songs'])
        else:
            f_songs = o['songs']
        for s in f_songs:
            val = s.get('Year', -1)
            if(val == -1):
                print(s)
                continue
            years[val] = years.get(val, 0) + 1
    else:
        years = o['year_made']
    plt.bar(years.keys(), years.values(), 0.5, color='r')
    plt.show()

def plot_years_added(o, compute=False, filter=None):
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
    plt.plot(x, y, 'g-')
    plt.show()

def genre_pie(o, compute=False, filter=None):
    if(compute):
        genres = {}
        for s in o['songs']:
            if(s['Genre'] == 'Hip-Hop/Rap'):
                g = 'Hip Hop/Rap'
            else:
                g = s['Genre']
            if('Grouping' in s.keys()):
                g += "/" + s['Grouping']
            genres[g] = genres.get(g, 0) + 1
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

def single_filter(category, criteria, contains=False):
    def filter(songs):
        ls = []
        for s in songs:
            if(contains):
                if(criteria in s.get(category, '')):
                    ls.append(s)
            else:
                if(s.get(category, '') == criteria):
                    ls.append(s)
        return ls
    return filter

def multi_filter(category, criteria_list, contains=False):
    def filter(songs):
        ls = []
        if(contains):
            for s in songs:
                for c in criteria_list:
                    if(c in s.get(category, '')):
                        ls.append(s)
                        continue
        else:
            for s in songs:
                for c in criteria_list:
                    if(c == s.get(category, '')):
                        ls.append(s)
                        continue
        return ls
    return filter



o = load_pickle('recent_parsed.pkl')
# plot_years_added(o)
# plot_years_made(o)
plot_years_added(o, True, single_filter('Genre', 'Hip-Hop/Rap'))
# genre_pie(o, True)
# ls = load_all("./xml")
# plot_play_count(ls)
