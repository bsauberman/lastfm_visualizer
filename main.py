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
    curr_day = df['DateTime'][curr_row][:-6]

    day = df['DateTime'][curr_row][:-6]
    artist = df['Artist'][curr_row]

    while artist and day and curr_day == day:
        if artist not in artists.keys():
            artists[artist] = 0
            #print(artist + ' added to keys with count of 0')
        artists[artist] = artists[artist] + 1
        #print(artist + ' count is now ' + str(artists[artist]))

        curr_row = curr_row - 1
        if curr_row > -1:
            day = df['DateTime'][curr_row][:-6]
            artist = df['Artist'][curr_row]
        else: break
    return curr_row, artists, curr_day

def prune_csv():
    csvreader = csv.reader(open(PRE_PRUNE_PATH))
    csvwriter = csv.writer(open(POST_PRUNE_PATH, "w"))

    # Deal with the header
    header = next(csvreader)
    header.append('Passed')
    csvwriter.writerow(header)
    prev_row = next(csvreader)
    # Process data rows
    for row in csvreader:
        if row[3]: row[3] = str(row[3])
        if row[0]: row[0] = str(row[0])
        if not row[3]: row[3] = prev_row[3]
        if not row[0]: row[0] = prev_row[1]
        prev_row = row

        csvwriter.writerow(row)    
        

def get_top_artists(data, n=10, order=True):

    top_artists = sorted(data.items(), key=lambda x: x[1], reverse=True)[:n]
    if order:
        return OrderedDict(top_artists)
    return dict(top_artists)

def get_data():
    curr_row = len(df)-1
    while curr_row > -1:
        curr_row, artists, curr_day = update_counts(curr_row)
        curr_top_artists = get_top_artists(artists, 10, True)
    
        create_image(curr_top_artists, curr_row, curr_day)
    create_video()

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
    return year + "-" + month + "-" + day


def create_image(curr_top_artists, curr_row, curr_day):
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(40, 30))
    plt.rcParams.update({'font.size': 25})

    # Plot the total crashes
    sns.color_palette("rocket", as_cmap=True)
    keys = list(curr_top_artists.keys())
    # get values in the same order as keys, and parse percentage values
    vals = [float(curr_top_artists[k]) for k in keys]
    pal = sns.color_palette("rocket", len(vals))
    rank = np.array(vals).argsort().argsort()  # http://stackoverflow.com/a/6266510/1628638
    sns_plot = sns.barplot(x=vals, y=keys, palette=np.array(pal[::-1])[rank])

    plt.title(curr_day)

    fig = sns_plot.get_figure()
    fig.savefig("images/" +change_date_format(curr_day)+".png")
    print(curr_day)

def create_video():
    frameSize = (4000,3000)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, frameSize)
    count = 0

    for filename in sorted(glob.glob('images/*.png')):
        img = cv2.imread(filename)
        out.write(img)
        print(filename)
        count = count + 1
        #if count > 20: break

    out.release()
    print('released')

artists = {}
print("here we go!!")
#prune_csv()
get_data()
#create_visualizer()
