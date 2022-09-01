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

        artists[artist] = artists[artist] + 1
        albums[album] = albums[album] + 1
        songs[song] = songs[song] + 1

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

    header = next(csvreader)
    csvwriter.writerow(header)

    for row in csvreader:
        if not row[0] or not row[1] or not row[2] or not row[3]: 
            continue
        else:
            csvwriter.writerow(row)    
        
def get_top(n=10):

    top_artists = sorted(artists.items(), key=lambda x: x[1], reverse=True)[:n]
    top_albums = sorted(albums.items(), key=lambda x: x[1], reverse=True)[:n]
    top_songs = sorted(songs.items(), key=lambda x: x[1], reverse=True)[:n]

    return OrderedDict(top_artists), OrderedDict(top_albums), OrderedDict(top_songs)

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

def get_data(year):
    curr_row = len(df)-1
    while change_date_format(df['DateTime'][curr_row][:-6])[0] != year:
        print(change_date_format(df['DateTime'][curr_row][:-6])[0], year)
        curr_row -= 1

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

def make_date_string(date):
    return date[0] + "-" + date[1] + "-" + date[2]

def check_if_new_year(date):
    if date[1] == '01' and date[2] == '01':
        print("Exported Current Top of Each Category to CSVs")
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

    sns_plot = sns.barplot(x=vals, y=keys, palette = color_palette)

    fig = sns_plot.get_figure()
    fig.savefig(type+"/"+ make_date_string(change_date_format(curr_date))+".png")
    print(curr_date)

def create_video(type):
    frameSize = (4000,3000)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('output.mp4', fourcc, 40, frameSize)

    for filename in sorted(glob.glob(type+'/*.png')):
        img = cv2.imread(filename)
        out.write(img)
        print(filename)

    out.release()
    print('released')

def load_data(year):
    artists_path = 'new_year_totals/artists_'+year+'-01-01.csv'
    albums_path = 'new_year_totals/albums_'+year+'-01-01.csv'
    songs_path = 'new_year_totals/songs_'+year+'-01-01.csv'
    with open(artists_path, 'r') as artists_file:
        reader = csv.reader(artists_file)
        for row in reader:
            artists[row[0]] = float(row[1])

    with open(albums_path, 'r') as albums_file:
        reader = csv.reader(albums_file)
        for row in reader:
            albums[row[0]] = float(row[1])

    with open(songs_path, 'r') as songs_file:
        reader = csv.reader(songs_file)
        for row in reader:
            songs[row[0]] = float(row[1])
artists = {}
albums = {}
songs = {}
print("here we go!!")
#prune_csv()
load_data('2020')
print(artists)
print(albums)
print(songs)
get_data('2020')
create_video('artists')
create_video('albums')
create_video('songs')
