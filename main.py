from operator import truediv
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
import numpy as np
import pandas as pd
import csv
from collections import OrderedDict
import cv2
import glob


PRE_PRUNE_PATH = "bsauberman.csv"
POST_PRUNE_PATH = 'bsauberman_pruned.csv'

#curr_row = 0
df = pd.read_csv(POST_PRUNE_PATH)

def update_counts(curr_row):
    curr_date = df['DateTime'][curr_row][:-6]

    day = df['DateTime'][curr_row][:-6]
    artist = df['Artist'][curr_row]
    album = df['Album'][curr_row]
    song = df['Song'][curr_row]


    while artist and album and song and day and curr_date == day:
        if artist not in artists.keys():
            artists[artist] = 0
        if album not in albums.keys():
            albums[album] = 0
        if song not in songs.keys():
            songs[song] = 0
            #print(artist + ' added to keys with count of 0')
        artists[artist] = artists[artist] + 1
        albums[album] = albums[album] + 1
        songs[song] = songs[song] + 1

        #print(artist + ' count is now ' + str(artists[artist]))

        curr_row = curr_row - 1
        if curr_row > -1:
            day = df['DateTime'][curr_row][:-6]
            artist = df['Artist'][curr_row]
            album = df['Album'][curr_row]
            song = df['Song'][curr_row]

        else: break
    return curr_row, curr_date

def prune_csv():
    csvreader = csv.reader(open(PRE_PRUNE_PATH))
    csvwriter = csv.writer(open(POST_PRUNE_PATH, "w"))

    # Deal with the header
    header = next(csvreader)
    csvwriter.writerow(header)
    # Process data rows
    for row in csvreader:
        # if row[3]: row[3] = str(row[3])
        # if row[0]: row[0] = str(row[0])
        if not row[0] or not row[1] or not row[2] or not row[3]: 
            continue
        else:
            csvwriter.writerow(row)    
        

def get_top(n=10):

    top_artists = sorted(artists.items(), key=lambda x: x[1], reverse=True)[:n]
    top_albums = sorted(albums.items(), key=lambda x: x[1], reverse=True)[:n]
    top_songs = sorted(songs.items(), key=lambda x: x[1], reverse=True)[:n]

    return OrderedDict(top_artists), OrderedDict(top_albums), OrderedDict(top_songs)

def get_data():
    curr_row = len(df)-1
    while curr_row > -1:
        curr_row, curr_date = update_counts(curr_row)
        curr_top_artists, curr_top_albums, curr_top_songs = get_top(10)
    
        create_image('artists', curr_top_artists, curr_date)
        create_image('albums', curr_top_albums, curr_date)
        create_image('songs', curr_top_songs, curr_date)

        if check_if_new_year(change_date_format(curr_date)):
            export_curr_data(make_date_string(change_date_format(curr_date)), [curr_top_artists, curr_top_albums, curr_top_songs])          

def export_curr_data(curr_date, curr_tops):
    categories = ['artists', 'albums', 'songs']
    for i in range(len(categories)):
        csvwriter = csv.writer(open('new_year_totals/' + categories[i] + '_' + curr_date + '.csv', "w"))
        keys = list(curr_tops[i].keys())
        vals = [float(curr_tops[i][k]) for k in keys]
        for j in range(len(keys)):
            csvwriter.writerow([keys[j], vals[j]])


def change_date_format(date):
    months = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
        }
    day, month, year = date.split()
    month = months[month]
    return [year, month, day]

def make_date_string(date):
    return date[0] + "-" + date[1] + "-" + date[2]


def check_if_new_year(date):
    if date[1] == '01' and date[2] == '01':
        print("new year!")
        return True
    return False

def create_image(type, curr_top, curr_date):
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(40, 30))
    plt.rcParams.update({'font.size': 25})
    plt.title(curr_date)
    pal = sns.color_palette("rocket", 10000, as_cmap=True)

    keys = list(curr_top.keys())
    vals = [float(curr_top[k]) for k in keys]
    color_palette = []
    for rank in range(len(keys)):
        hash = 0
        for char in range(len(keys[rank])):
            hash += ord(keys[rank][char]) 
        hash %= 256
        color_palette.append(pal.colors[hash])


    #rank = np.array(vals).argsort().argsort()  # http://stackoverflow.com/a/6266510/1628638
    sns_plot = sns.barplot(x=vals, y=keys, palette = color_palette)
    #palette=np.array(pal[::-1])[rank]

    fig = sns_plot.get_figure()
    fig.savefig(type+"/"+ make_date_string(change_date_format(curr_date))+".png")
    print(curr_date)



def create_video(type):
    frameSize = (4000,3000)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('output.mp4', fourcc, 40, frameSize)
    count = 0

    for filename in sorted(glob.glob(type+'/*.png')):
        img = cv2.imread(filename)
        out.write(img)
        print(filename)
        count = count + 1
        #if count > 20: break

    out.release()
    print('released')

artists = {}
albums = {}
songs = {}
print("here we go!!")
#prune_csv()
get_data()
create_video(artists)
create_video(albums)
create_video(songs)
